import gzip
import json
import logging
import os
import shutil
from collections import namedtuple

import requests

from installed_clients.WorkspaceClient import Workspace

Location = namedtuple('location', ['contig', 'start', 'strand', 'length'])
complements = str.maketrans({"G": "C", "C": "G", "A": "T", "T": "A"})


def _get_start(loc):
    """Get the starting location position of a feature in the contig (accounting for the strand)"""
    if loc.strand == '+':
        return loc.start
    if loc.strand == '-':
        st = loc.start - (loc.length - 1)
        if st < 0:
            raise ValueError(f'{loc} is not a valid location on this assembly')
        return st
    return 0


def _extract_sequence(assembly_dir, feature_locs):
    """Given a cached assembly directory extract a sequence for each of the supplied locations"""
    contig = None
    fragments = []
    for loc_tup in feature_locs:
        loc = Location(*loc_tup)
        if not contig or loc.contig != os.path.basename(contig.name):
            try:
                contig = gzip.open(os.path.join(assembly_dir, loc.contig))
            except FileNotFoundError:
                raise ValueError(f"{loc.contig} was not found in the cached assembly")
        contig.seek(_get_start(loc))  # finally have a use for .seek()!
        seq = contig.read(loc.length).decode().upper()
        # seek and read won't complain if the parameter passed would result in a location not in
        # the file so we need to make sure the sequence is the expected length
        if len(seq) != loc.length:
            raise ValueError(f'{loc} is not a valid location on this assembly')
        if loc.strand == '+':
            fragments.append(seq)
        if loc.strand == '-':
            fragments.append(seq.translate(complements)[::-1])  # reverse-complement for - strand
    return "".join(fragments)


class AssemblySequenceCache:
    def _cull_cache(self):
        """Ensure that cached assemblies do not proliferate"""
        list_of_files = os.listdir(self.cache_dir)
        while len(list_of_files) >= self.max_cached_objects:
            oldest_file = min(list_of_files, key=lambda x: os.path.getctime(
                os.path.join(self.cache_dir, x)))
            shutil.rmtree(os.path.join(self.cache_dir, oldest_file))

    @staticmethod
    def _fasta_to_contigs(filepath):
        """Generator function to extract contigs sequences from a fasta file. Returns a tuple of
        contig ID and sequence (as bytes)"""
        cid = None
        sequence = []
        with open(filepath, 'rb') as infile:
            for line in infile:
                if line.startswith(b">"):
                    if cid:
                        yield (cid, b"".join(sequence))
                    cid = line.decode().strip(">\n").split()[0]
                    sequence = []
                else:
                    sequence.append(line.strip())
        os.remove(filepath)
        yield (cid, b"".join(sequence))

    def _file_from_shock(self, token, shock_id, file_path):
        """Pulls a file out of shock and streams into a specified file location"""
        headers = {'Authorization': 'OAuth ' + token}
        node_url = f'{self.shock_url}/node/{shock_id}'
        logging.info(f'Downloading shock node {shock_id} into file: {file_path}')
        with open(file_path, 'wb') as fhandle:
            r = requests.get(node_url + '?download_raw', stream=True,
                             headers=headers, allow_redirects=True)
            if not r.ok:
                try:
                    err = json.loads(r.content)['error'][0]
                    raise RuntimeError(err)
                except:
                    # this means shock is down or not responding.
                    logging.error(f"Couldn't parse response error content from Shock: {r.content}")
                    r.raise_for_status()

            for chunk in r.iter_content(1024):
                if not chunk:
                    break
                fhandle.write(chunk)

        return file_path

    def _cache_assembly(self, ws, token, ref, assembly_dir):
        """Given a reference to an assembly or contig set pull the contigs out of Shock/WS and
        cache in a directory of compressed sequences"""
        logging.info(f'Caching {ref}')
        os.makedirs(assembly_dir)
        self._cull_cache()
        obj_data = ws.get_objects2(
            {'objects': [{'ref': ref, 'included': ['fasta_handle_info']}]})['data'][0]['data']

        if obj_data.get('fasta_handle_info'):  # is an assembly
            fh_info = obj_data['fasta_handle_info']
            fasta_path = self._file_from_shock(token, fh_info['shock_id'],
                                               os.path.join(assembly_dir, fh_info['node_file_name']))
            contigs = self._fasta_to_contigs(fasta_path)

        else:  # is a contig set
            contig_data = ws.get_objects2(
                {'objects': [{'ref': ref, 'included': ['contigs']}]})['data'][0]['data']['contigs']
            contigs = ((c['id'], c['sequence'].encode()) for c in contig_data)

        for cid, seq in contigs:
            with gzip.open(os.path.join(assembly_dir, cid), 'wb', compresslevel=1) as outfile:
                outfile.write(seq)

    def __init__(self, ws_url, shock_url, max_cached_objects=100, cache_dir="./assembly_cache"):
        self.ws_url = ws_url
        self.shock_url = shock_url
        self.max_cached_objects = max_cached_objects
        self.cache_dir = cache_dir
        self.valid_types = {'KBaseGenomes.ContigSet', 'KBaseGenomeAnnotations.Assembly'}

    def extract_dna_sequences(self, token, params):
        """Takes an assembly/contig set ref and one or more locations and returns the DNA sequence
        from the assembly at that location while caching the assembly for efficiency"""
        if not params.get('ref'):
            raise ValueError("'ref', a reference to an assembly must be provided")
        ref = params['ref']
        locs = params.get('locations', [])
        ws = Workspace(self.ws_url, token=token)
        # This is also a cheap way to ensure that the object exists and that the user has access
        obj_type = ws.get_object_info3({'objects': [{'ref': ref}]})['infos'][0][2]
        if obj_type.split('-')[0] not in self.valid_types:
            raise ValueError(f'{obj_type} is not a valid input type for this function')
        assembly_dir = os.path.join(self.cache_dir, ref.replace('/', ':'))
        if not os.path.exists(assembly_dir):
            self._cache_assembly(ws, token, ref, assembly_dir)
        return [_extract_sequence(assembly_dir, l) for l in locs]
