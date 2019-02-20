from installed_clients.WorkspaceClient import Workspace


def _get_data_from_ws(workspace_url, ref, included):
    ws = Workspace(workspace_url)
    data = ws.get_objects2({'objects': [{'ref': ref, 'included': included}]})['data'][0]['data']
    if len(included) == 1:
        return data.get(included[0])
    return {k: data.get(k) for k in included}


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
    return _get_data_from_ws(workspace_url, ref, ['external_source', 'external_source_id',
                                                 'external_source_origination_date'])


def get_stats(workspace_url, ref):
    return _get_data_from_ws(workspace_url, ref, ['num_contigs', 'gc_content', 'dna_size'])


def get_number_contigs(workspace_url, ref):
    return _get_data_from_ws(workspace_url, ref, ['num_contigs'])


def get_gc_content(workspace_url, ref):
    return _get_data_from_ws(workspace_url, ref, ['gc_content'])


def get_dna_size(workspace_url, ref):
    return _get_data_from_ws(workspace_url, ref, ['dna_size'])


def get_contig_ids(workspace_url, ref):
    ws = Workspace(workspace_url)
    data = ws.get_objects2(
        {'objects': [{'ref': ref, 'included': ['contigs/*/contig_id']}]}
    )['data'][0]['data']
    return [x for x in data.get('contigs', {})]


def get_contig_lengths(workspace_url, ref, contig_id_list):
    ws = Workspace(workspace_url)
    included = [f'contigs/{cid}/length' for cid in contig_id_list]
    data = ws.get_objects2({'objects': [{'ref': ref, 'included': included}]})['data'][0]['data']
    return {k: v.get('length') for k, v in list(data.get('contigs', {}).items())}


def get_contig_gc_content(workspace_url, ref, contig_id_list):
    ws = Workspace(workspace_url)
    included = [f'contigs/{cid}/gc_content' for cid in contig_id_list]
    data = ws.get_objects2({'objects': [{'ref': ref, 'included': included}]})['data'][0]['data']
    return {k: v.get('gc_content') for k, v in list(data.get('contigs', {}).items())}


def get_contigs(workspace_url, ref, contig_id_list):
    ws = Workspace(workspace_url)
    included = ['contigs/' + cid for cid in contig_id_list]
    data = ws.get_objects2({'objects': [{'ref': ref, 'included': included}]})['data'][0]['data']
    return data.get('contigs')
