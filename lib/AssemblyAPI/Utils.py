from Workspace.WorkspaceClient import Workspace


def _get_data_from_ws(workspaceURL, ref, included):
    ws = Workspace(workspaceURL)
    data = ws.get_objects2({'objects': [{'ref': ref, 'included': included}]})['data'][0]['data']
    if len(included) == 1:
        return data.get(included[0])
    return {k: data.get(k) for k in included}


def get_assembly_id(workspaceURL, ref):
    ws = Workspace(workspaceURL)
    return ws.get_object_info3({'objects': [{'ref': ref}]})['infos'][0][1]


def get_genome_annotations(workspaceURL, ref):
    ws = Workspace(workspaceURL)
    objects = ws.list_referencing_objects([{'ref': ref}])[0]
    return ['{}/{}/{}'.format(info[6], info[0], info[4]) for info in objects
            if info[2].split("-")[0] == 'KBaseGenomes.Genome'
            or info[2].split("-")[0] == 'KBaseGenomeAnnotations.GenomeAnnotation']


def get_external_source_info(workspaceURL, ref):
    return _get_data_from_ws(workspaceURL, ref, ['external_source', 'external_source_id',
                                                 'external_source_origination_date'])


def get_stats(workspaceURL, ref):
    return _get_data_from_ws(workspaceURL, ref, ['num_contigs', 'gc_content', 'dna_size'])


def get_number_contigs(workspaceURL, ref):
    return _get_data_from_ws(workspaceURL, ref, ['num_contigs'])


def get_gc_content(workspaceURL, ref):
    return _get_data_from_ws(workspaceURL, ref, ['gc_content'])


def get_dna_size(workspaceURL, ref):
    return _get_data_from_ws(workspaceURL, ref, ['dna_size'])


def get_contig_ids(workspaceURL, ref):
    ws = Workspace(workspaceURL)
    data = ws.get_objects2(
        {'objects': [{'ref': ref, 'included': ['contigs/*/contig_id']}]}
    )['data'][0]['data']
    return [x for x in data.get('contigs', {})]


def get_contig_lengths(workspaceURL, ref, contig_id_list):
    ws = Workspace(workspaceURL)
    included = ['contigs/{}/length'.format(cid) for cid in contig_id_list]
    data = ws.get_objects2({'objects': [{'ref': ref, 'included': included}]})['data'][0]['data']
    return {k: v.get('length') for k, v in data.get('contigs', {}).items()}


def get_contig_gc_content(workspaceURL, ref, contig_id_list):
    ws = Workspace(workspaceURL)
    included = ['contigs/{}/gc_content'.format(cid) for cid in contig_id_list]
    data = ws.get_objects2({'objects': [{'ref': ref, 'included': included}]})['data'][0]['data']
    return {k: v.get('gc_content') for k, v in data.get('contigs', {}).items()}


def get_contigs(workspaceURL, ref, contig_id_list):
    ws = Workspace(workspaceURL)
    included = ['contigs/' + cid for cid in contig_id_list]
    data = ws.get_objects2({'objects': [{'ref': ref, 'included': included}]})['data'][0]['data']
    return data.get('contigs')
