from collections import Counter

from installed_clients.WorkspaceClient import Workspace


def _calc_gc_content(sequence):
    bases = Counter(sequence)
    return sum(bases.get(x, 0) for x in ["G", "C", "g", "c"]) / sum(bases.values())


def _convert_contig_set(contig_set):
    total_len = 0
    total_gc = 0
    contigs = {}
    for v in contig_set['contigs']:
        gc = _calc_gc_content(v['sequence'])
        contigs[v['id']] = {
                'contig_id': v['id'],
                'name': v.get('name', v['id']),
                'description': '',
                'md5': v['md5'],
                'length': v['length'],
                'gc_content': gc,
            }
        total_len += v['length']
        total_gc += gc * v['length']
    return {
        'gc_content': total_gc / total_len,
        'dna_size': total_len,
        'num_contigs': len(contigs),
        'contigs': contigs,
        'external_source': contig_set['source'],
        'external_source_id': contig_set['source_id'],
        'external_source_origination_date': '',
    }


def _get_data_from_ws(workspace_url, ref, included):
    ws = Workspace(workspace_url)
    info = ws.get_object_info3({'objects': [{'ref': ref}]})['infos'][0]
    if info[2].split("-")[0] == 'KBaseGenomes.ContigSet':
        return _convert_contig_set(ws.get_objects2(
            {'objects': [{'ref': ref}]})['data'][0]['data'])
    return ws.get_objects2(
        {'objects': [{'ref': ref, 'included': included}]})['data'][0]['data']


def get_assembly_id(workspace_url, ref):
    ws = Workspace(workspace_url)
    return ws.get_object_info3({'objects': [{'ref': ref}]})['infos'][0][1]


def get_genome_annotations(workspace_url, ref):
    ws = Workspace(workspace_url)
    objects = ws.list_referencing_objects([{'ref': ref}])[0]
    return [f'{info[6]}/{info[0]}/{info[4]}' for info in objects
            if info[2].split("-")[0] == 'KBaseGenomes.Genome'
            or info[2].split("-")[0] == 'KBaseGenomeAnnotations.GenomeAnnotation']


def get_external_source_info(workspace_url, ref):
    included = ['external_source', 'external_source_id', 'external_source_origination_date']
    data = _get_data_from_ws(workspace_url, ref, included)
    return {k: data[k] for k in included}


def get_stats(workspace_url, ref):
    included = ['num_contigs', 'gc_content', 'dna_size']
    data = _get_data_from_ws(workspace_url, ref, included)
    return {k: data[k] for k in included}


def get_number_contigs(workspace_url, ref):
    return _get_data_from_ws(workspace_url, ref, ['num_contigs'])['num_contigs']


def get_gc_content(workspace_url, ref):
    return _get_data_from_ws(workspace_url, ref, ['gc_content'])['gc_content']


def get_dna_size(workspace_url, ref):
    return _get_data_from_ws(workspace_url, ref, ['dna_size'])['dna_size']


def get_contig_ids(workspace_url, ref):
    included = ['contigs/*/contig_id']
    data = _get_data_from_ws(workspace_url, ref, included)
    return [x for x in data.get('contigs', {})]


def get_contig_lengths(workspace_url, ref, contig_id_list):
    included = [f'contigs/{cid}/length' for cid in contig_id_list]
    data = _get_data_from_ws(workspace_url, ref, included)
    return {k: data['contigs'][k].get('length') for k in contig_id_list}


def get_contig_gc_content(workspace_url, ref, contig_id_list):
    included = [f'contigs/{cid}/gc_content' for cid in contig_id_list]
    data = _get_data_from_ws(workspace_url, ref, included)
    return {k: data['contigs'][k].get('gc_content') for k in contig_id_list}


def get_contigs(workspace_url, ref, contig_id_list):
    included = ['contigs/' + cid for cid in contig_id_list]
    data = _get_data_from_ws(workspace_url, ref, included)
    return {k: data['contigs'][k] for k in contig_id_list}
