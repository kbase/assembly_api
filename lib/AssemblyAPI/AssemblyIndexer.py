# -*- coding: utf-8 -*-
import os
import subprocess
import tempfile
import time
import traceback

from AssemblyAPI.CombinedLineIterator import CombinedLineIterator
from installed_clients.WorkspaceClient import Workspace as Workspace


class AssemblyIndexer:

    def __init__(self, config):
        self.assembly_column_props_map = {
            "contig_id": {"col": 1, "type": ""},
            "description": {"col": 2, "type": ""},
            "length": {"col": 3, "type": "n"},
            "gc": {"col": 4, "type": "n"},
            "is_circ": {"col": 5, "type": "n"},
            "N_count": {"col": 6, "type": "n"},
            "md5": {"col": 7, "type": ""}
        }

        self.ASSEMBLY_SUFFIX = '_assembly'
        self.ws_url = config["workspace-url"]
        self.assembly_index_dir = config["assembly-index-dir"]
        if not os.path.isdir(self.assembly_index_dir):
            os.makedirs(self.assembly_index_dir)
        self.debug = "debug" in config and config["debug"] == "1"
        self.max_sort_mem_size = 250000
        self.unicode_comma = "\uFF0C"

    def search_contigs(self, token, ref, query, sort_by, start, limit, num_found):
        if query is None:
            query = ""
        if start is None:
            start = 0
        if limit is None:
            limit = 50
        if self.debug:
            print(f"Search: Assembly={ref}, query=[{query}], "
                  f"sort-by=[{self.get_sorting_code(self.assembly_column_props_map, sort_by)}],"
                  f" start={start}, limit={limit}")
            t1 = time.time()
        inner_chsum = self.check_assembly_cache(ref, token)
        index_iter = self.get_assembly_sorted_iterator(inner_chsum, sort_by)
        ret = self.filter_contigs_query(index_iter, query, start, limit, num_found)
        if self.debug:
            print(f"    (overall-time={time.time() - t1})")
        return ret

    def to_text(self, mapping, key):
        if key not in mapping or mapping[key] is None:
            return ""
        value = mapping[key]
        if type(value) is list:
            return ",".join(str(x) for x in value if x)
        return str(value)

    def save_assembly_tsv(self, contigs, inner_chsum):
        outfile = tempfile.NamedTemporaryFile(dir=self.assembly_index_dir,
                                              prefix=inner_chsum + self.ASSEMBLY_SUFFIX,
                                              suffix=".tsv", delete=False)
        with outfile:
            for contig_data in contigs:

                contig_id = self.to_text(contig_data, 'contig_id')
                description = self.to_text(contig_data, 'description')
                length = ''
                if 'length' in contig_data:
                    length = str(contig_data['length'])
                gc = ''
                if 'gc_content' in contig_data:
                    gc = str(contig_data['gc_content'])
                is_circ = ''
                if 'is_circ' in contig_data:
                    is_circ = str(contig_data['is_circ'])
                N_count = ''
                if 'Ncount' in contig_data:
                    N_count = str(contig_data['Ncount'])
                md5 = self.to_text(contig_data, 'md5')

                line = "\t".join(x for x in [contig_id, description, length, gc, is_circ, N_count,
                                             md5]) + "\n"
                outfile.write(line.encode("utf-8"))

        subprocess.Popen(["gzip", outfile.name],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait()
        os.rename(outfile.name + ".gz", os.path.join(self.assembly_index_dir,
                                                     inner_chsum + self.ASSEMBLY_SUFFIX + ".tsv.gz"))

    def check_assembly_cache(self, ref, token):
        ws = Workspace(self.ws_url, token=token)
        info = ws.get_object_info3({"objects": [{"ref": ref}]})['infos'][0]
        inner_chsum = info[8]
        index_file = os.path.join(self.assembly_index_dir, inner_chsum + self.ASSEMBLY_SUFFIX + ".tsv.gz")
        if not os.path.isfile(index_file):
            if self.debug:
                print("    Loading WS object...")
                t1 = time.time()

            if 'KBaseGenomeAnnotations.Assembly' in info[2]:
                included = ["/contigs"]
                assembly_data = ws.get_objects2(
                    {'objects': [{'ref': ref, 'included': included}]})['data'][0]['data']
                contigs = list(assembly_data['contigs'].values())
                self.save_assembly_tsv(contigs, inner_chsum)

            elif 'KBaseGenomes.ContigSet' in info[2]:
                included = ["/contigs/[*]/id",
                            "/contigs/[*]/length",
                            "/contigs/[*]/md5",
                            "/contigs/[*]/description"]
                cs_data = ws.get_objects2(
                    {'objects': [{'ref': ref, 'included': included}]})['data'][0]['data']
                contigs = []
                for c in cs_data['contigs']:
                    this_contig_data = {'contig_id': ''}
                    if 'id' in c:
                        this_contig_data['contig_id'] = c['id']
                    if 'md5' in c:
                        this_contig_data['md5'] = c['md5']
                    if 'length' in c:
                        this_contig_data['length'] = c['length']
                    if 'description' in c:
                        this_contig_data['description'] = c['description']
                    contigs.append(this_contig_data)

                self.save_assembly_tsv(contigs, inner_chsum)
            else:
                raise ValueError('The "ref" is not an Assembly or ContigSet data object. '
                                 'It was a ' + info[2])

            if self.debug:
                print(f"    (time={time.time() - t1})")
        return inner_chsum

    def get_column_props(self, column_props_map, col_name):
        if col_name not in column_props_map:
            raise ValueError("Unknown column name '" + col_name + "', " +
                             "please use one of " + str(list(column_props_map.keys())))
        return column_props_map[col_name]

    def get_sorting_code(self, column_props_map, sort_by):
        ret = ""
        if sort_by is None or len(sort_by) == 0:
            return ret
        for column_sorting in sort_by:
            col_name = column_sorting[0]
            col_props = self.get_column_props(column_props_map, col_name)
            col_pos = str(col_props["col"])
            ascending_order = column_sorting[1]
            ret += col_pos + ('a' if ascending_order else 'd')
        return ret

    def get_assembly_sorted_iterator(self, inner_chsum, sort_by):
        return self.get_sorted_iterator(inner_chsum, sort_by, self.ASSEMBLY_SUFFIX,
                                        self.assembly_column_props_map)

    def get_sorted_iterator(self, inner_chsum, sort_by, item_type, column_props_map):
        input_file = os.path.join(self.assembly_index_dir, inner_chsum + item_type + ".tsv.gz")
        if not os.path.isfile(input_file):
            raise ValueError("File not found: " + input_file)
        if sort_by is None or len(sort_by) == 0:
            return CombinedLineIterator(input_file)
        cmd = "gunzip -c \"" + input_file + "\" | sort -f -t\\\t"
        for column_sorting in sort_by:
            col_name = column_sorting[0]
            col_props = self.get_column_props(column_props_map, col_name)
            col_pos = str(col_props["col"])
            ascending_order = column_sorting[1]
            sort_arg = "-k" + col_pos + "," + col_pos + col_props["type"]
            if not ascending_order:
                sort_arg += "r"
            cmd += " " + sort_arg
        fname = (inner_chsum + "_" + item_type + "_" +
                 self.get_sorting_code(column_props_map, sort_by))
        final_output_file = os.path.join(self.assembly_index_dir, fname + ".tsv.gz")
        if not os.path.isfile(final_output_file):
            if self.debug:
                print("    Sorting...")
                t1 = time.time()
            need_to_save = os.path.getsize(input_file) > self.max_sort_mem_size
            if need_to_save:
                outfile = tempfile.NamedTemporaryFile(dir=self.assembly_index_dir,
                                                      prefix=fname + "_", suffix=".tsv.gz", delete=False)
                outfile.close()
                output_file = outfile.name
                cmd += " | gzip -c > \"" + output_file + "\""
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            if not need_to_save:
                if self.debug:
                    print(f"    (time={time.time() - t1})")
                return CombinedLineIterator(p)
            else:
                p.wait()
                os.rename(output_file, final_output_file)
                if self.debug:
                    print(f"    (time={time.time() - t1})")
        return CombinedLineIterator(final_output_file)

    def filter_contigs_query(self, index_iter, query, start, limit, num_found):
        query_words = str(query).lower().translate(str.maketrans("\r\n\t,", "    ")).split()
        if self.debug:
            print("    Filtering...")
            t1 = time.time()
        fcount = 0
        contigs = []
        with index_iter:
            for line in index_iter:
                if all(word in line.lower() for word in query_words):
                    if fcount >= start and fcount < start + limit:
                        contigs.append(self.unpack_bin(line.rstrip('\n')))
                    fcount += 1
                    if num_found is not None and fcount >= start + limit:
                        # Having shortcut when real num_found was already known
                        fcount = num_found
                        break
        if self.debug:
                print(f"    (time={time.time() - t1})")
        return {"num_found": fcount, "start": start, "contigs": contigs,
                "query": query}

    def unpack_bin(self, line, items=None):
        try:
            if items is None:
                items = line.split('\t')

            contig_id = items[0]
            description = items[1]

            length = None
            if items[2]:
                length = int(items[2])

            gc = None
            if items[3]:
                gc = float(items[3])

            is_circ = None
            if items[4]:
                is_circ = int(items[4])

            N_count = None
            if items[5]:
                N_count = int(items[5])

            md5 = items[6]

            return {'contig_id': contig_id,
                    'description': description,
                    'length': length,
                    'gc': gc,
                    'is_circ': is_circ,
                    'N_count': N_count,
                    'md5': md5
                    }
        except:
            raise ValueError("Error parsing contig from: [" + line + "]\n" +
                             "Cause: " + traceback.format_exc())
