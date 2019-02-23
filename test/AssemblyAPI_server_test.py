import json
import os
import shutil
import time
import unittest
from configparser import ConfigParser  # py3
from os import environ
from pprint import pprint

from AssemblyAPI.AssemblyAPIImpl import AssemblyAPI
from AssemblyAPI.AssemblyAPIServer import MethodContext
from installed_clients.AssemblyUtilClient import AssemblyUtil
from installed_clients.WorkspaceClient import Workspace as workspaceService


class AssemblyAPITest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = environ.get('KB_AUTH_TOKEN', None)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'provenance': [
                            {'service': 'AssemblyAPI',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('AssemblyAPI'):
            cls.cfg[nameval[0]] = nameval[1]
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = workspaceService(cls.wsURL, token=token)
        cls.serviceImpl = AssemblyAPI(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']

        suffix = int(time.time() * 1000)
        cls.wsName = "test_kb_maxbin_" + str(suffix)
        cls.ws_info = cls.wsClient.create_workspace({'workspace': cls.wsName})

        cls.obj_ref = "7989/489/2"
        cls.contigs = ['NZ_ALQT01000016']

        # create an example Assembly
        cls.au = AssemblyUtil(cls.callback_url)
        assembly_filename = 'test.fa'
        cls.assembly_fasta_file_path = os.path.join(cls.scratch, assembly_filename)
        shutil.copy(os.path.join("data", assembly_filename), cls.assembly_fasta_file_path)

        assembly_params = {
            'file': {'path': cls.assembly_fasta_file_path},
            'workspace_name': cls.wsName,
            'assembly_name': 'MyAssembly'
        }
        cls.assembly_ref_1 = cls.au.save_assembly_from_fasta(assembly_params)
        print('Assembly1:' + cls.assembly_ref_1)

        # create a test legacy contigset
        with open('data/contigset1.json') as file:
            contigset_data = json.load(file)
        saveData = {
            'type': 'KBaseGenomes.ContigSet',
            'data': contigset_data,
            'name': 'contigset'
        }
        info = cls.wsClient.save_objects(
            {'workspace': cls.wsName, 'objects': [saveData]})[0]
        cls.contig_set_ref = f'{info[6]}/{info[0]}/{info[4]}'
        print('ContigSet1:' + cls.contig_set_ref)

        # create a test legacy contigset
        with open('data/contigset2.json') as file:
            contigset_data = json.load(file)
        saveData = {
            'type': 'KBaseGenomes.ContigSet',
            'data': contigset_data,
            'name': 'contigset'
        }
        info = cls.wsClient.save_objects(
            {'workspace': cls.wsName, 'objects': [saveData]})[0]
        cls.contig_set_ref_2 = f'{info[6]}/{info[0]}/{info[4]}'
        print('ContigSet2:' + cls.contig_set_ref_2)


    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def getWsClient(self):
        return self.__class__.wsClient

    def getWsName(self):
        if hasattr(self.__class__, 'wsName'):
            return self.__class__.wsName
        suffix = int(time.time() * 1000)
        wsName = "test_AssemblyAPI_" + str(suffix)
        ret = self.getWsClient().create_workspace({'workspace': wsName})
        self.__class__.wsName = wsName
        return wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    def test_search_legacy_contigset(self):
        # no query
        search_params = {'ref': self.contig_set_ref}
        ret = self.getImpl().search_contigs(self.ctx, search_params)[0]
        self.assertEqual(ret['num_found'], 41)
        self.assertEqual(ret['query'], '')
        self.assertEqual(ret['start'], 0)
        self.assertEqual(len(ret['contigs']), 41)
        self.assertEqual(ret['contigs'][0]['contig_id'], 'k41_1')
        self.assertEqual(ret['contigs'][0]['gc'], None)
        self.assertEqual(ret['contigs'][0]['description'], 'k41_1 flag=0 multi=10.6142 len=2628')
        self.assertEqual(ret['contigs'][1]['contig_id'], 'k41_3')

        search_params = {'ref': self.contig_set_ref, 'sort_by': [['gc', 1]]}
        ret = self.getImpl().search_contigs(self.ctx, search_params)[0]
        self.assertEqual(ret['num_found'], 41)
        self.assertEqual(ret['query'], '')
        self.assertEqual(ret['start'], 0)
        self.assertEqual(len(ret['contigs']), 41)

    def test_search_assembly(self):
        # no query
        search_params = {'ref': self.assembly_ref_1}
        ret = self.getImpl().search_contigs(self.ctx, search_params)[0]
        self.assertEqual(ret['num_found'], 15)
        self.assertEqual(ret['query'], '')
        self.assertEqual(ret['start'], 0)
        self.assertEqual(len(ret['contigs']), 15)
        self.assertEqual(ret['contigs'][0]['contig_id'], 'NZ_ALQT01000001')
        self.assertEqual(ret['contigs'][0]['gc'], 0.37309)
        self.assertEqual(ret['contigs'][0]['description'], '')
        self.assertEqual(ret['contigs'][1]['contig_id'], 'NZ_ALQT01000002')
        self.assertEqual(ret['contigs'][2]['contig_id'], 'NZ_ALQT01000003')

        # with query
        search_params = {'ref': self.assembly_ref_1, 'query': 'ALQT01000015'}
        ret = self.getImpl().search_contigs(self.ctx, search_params)[0]
        self.assertEqual(ret['num_found'], 1)
        self.assertEqual(ret['query'], 'ALQT01000015')
        self.assertEqual(ret['start'], 0)
        self.assertEqual(len(ret['contigs']), 1)
        self.assertEqual(ret['contigs'][0]['contig_id'], 'NZ_ALQT01000015')
        self.assertEqual(ret['contigs'][0]['description'], 'this is a description')

        # with limit
        search_params = {'ref': self.assembly_ref_1, 'limit': 2}
        ret = self.getImpl().search_contigs(self.ctx, search_params)[0]
        self.assertEqual(ret['num_found'], 15)
        self.assertEqual(ret['query'], '')
        self.assertEqual(ret['start'], 0)
        self.assertEqual(len(ret['contigs']), 2)
        self.assertEqual(ret['contigs'][0]['contig_id'], 'NZ_ALQT01000001')
        self.assertEqual(ret['contigs'][1]['contig_id'], 'NZ_ALQT01000002')

        # with limit
        search_params = {'ref': self.assembly_ref_1, 'start': 2, 'limit': 2}
        ret = self.getImpl().search_contigs(self.ctx, search_params)[0]
        self.assertEqual(ret['num_found'], 15)
        self.assertEqual(ret['query'], '')
        self.assertEqual(ret['start'], 2)
        self.assertEqual(len(ret['contigs']), 2)
        self.assertEqual(ret['contigs'][0]['contig_id'], 'NZ_ALQT01000003')
        self.assertEqual(ret['contigs'][1]['contig_id'], 'NZ_ALQT01000004')

        # sort by gc
        search_params = {'ref': self.assembly_ref_1, 'limit': 5, 'sort_by': [['gc', 0]]}
        ret = self.getImpl().search_contigs(self.ctx, search_params)[0]
        self.assertEqual(ret['num_found'], 15)
        self.assertEqual(ret['query'], '')
        self.assertEqual(ret['start'], 0)
        self.assertEqual(len(ret['contigs']), 5)
        self.assertEqual(ret['contigs'][0]['contig_id'], 'NZ_ALQT01000010')
        self.assertEqual(ret['contigs'][1]['contig_id'], 'NZ_ALQT01000004')

        search_params = {'ref': self.assembly_ref_1, 'sort_by': [['gc', 1]]}
        ret = self.getImpl().search_contigs(self.ctx, search_params)[0]
        self.assertEqual(ret['num_found'], 15)
        self.assertEqual(ret['query'], '')
        self.assertEqual(ret['start'], 0)
        self.assertEqual(len(ret['contigs']), 15)
        self.assertEqual(ret['contigs'][0]['contig_id'], 'NZ_ALQT01000009')
        self.assertEqual(ret['contigs'][1]['contig_id'], 'NZ_ALQT01000003')
        self.assertEqual(ret['contigs'][2]['contig_id'], 'NZ_ALQT01000005')

    def test_get_assembly_id(self):
        ret = self.getImpl().get_assembly_id(self.ctx, self.obj_ref)
        self.assertEqual(ret[0], 'GCF_000288855.1_assembly')

    def test_get_genome_annotations(self):
        ret = self.getImpl().get_genome_annotations(self.ctx, self.obj_ref)
        self.assertEqual(ret[0], ['7989/498/2'])

    def test_get_external_source_info(self):
        ret = self.getImpl().get_external_source_info(self.ctx, self.obj_ref)
        self.assertEqual(ret[0], {'external_source': 'unknown_source',
                                  'external_source_id': 'GCF_000288855.1_2016_07_17_13_53_33.fa',
                                  'external_source_origination_date': '21-AUG-2015'})

    def test_get_stats(self):
        ret = self.getImpl().get_stats(self.ctx, self.obj_ref)
        self.assertEqual(ret[0], {'num_contigs': 21,
                                  'gc_content': 0.35178740497572963,
                                  'dna_size': 2097622})

    def test_get_number_contigs(self):
        ret = self.getImpl().get_number_contigs(self.ctx, self.obj_ref)
        self.assertEqual(ret[0], 21)

    def test_get_gc_content(self):
        ret = self.getImpl().get_gc_content(self.ctx, self.obj_ref)
        self.assertEqual(ret[0], 0.35178740497572963)

    def test_get_dna_size(self):
        ret = self.getImpl().get_dna_size(self.ctx, self.obj_ref)
        self.assertEqual(ret[0], 2097622)

    def test_get_contig_ids(self):
        ret = self.getImpl().get_contig_ids(self.ctx, self.obj_ref)
        self.assertCountEqual(ret[0], ['NZ_ALQT01000016', 'NZ_ALQT01000020', 'NZ_ALQT01000021',
                                       'NZ_ALQT01000017', 'NZ_ALQT01000018', 'NZ_ALQT01000019',
                                       'NZ_ALQT01000009', 'NZ_ALQT01000008', 'NZ_ALQT01000014',
                                       'NZ_ALQT01000015', 'NZ_ALQT01000012', 'NZ_ALQT01000013',
                                       'NZ_ALQT01000010', 'NZ_ALQT01000011', 'NZ_ALQT01000001',
                                       'NZ_ALQT01000003', 'NZ_ALQT01000002', 'NZ_ALQT01000005',
                                       'NZ_ALQT01000004', 'NZ_ALQT01000007', 'NZ_ALQT01000006'])

    def test_get_contig_lengths(self):
        ret = self.getImpl().get_contig_lengths(self.ctx, self.obj_ref, self.contigs)
        self.assertEqual(ret[0], {'NZ_ALQT01000016': 53554})

    def test_get_contig_gc_content(self):
        ret = self.getImpl().get_contig_gc_content(self.ctx, self.obj_ref, self.contigs)
        self.assertEqual(ret[0], {'NZ_ALQT01000016': 0.35366172461440787})

    def test_get_contigs(self):
        ret = self.getImpl().get_contigs(self.ctx, self.obj_ref, self.contigs)
        self.assertCountEqual(ret[0][u'NZ_ALQT01000016'],
                              ['gc_content', 'length', 'md5', 'name', 'Ncount', 'start_position',
                               'contig_id', 'description', 'is_circular', 'num_bytes'])

    def test_get_stats_contig_set(self):
        ret = self.getImpl().get_stats(self.ctx, self.contig_set_ref_2)
        self.assertEqual(ret[0], {'num_contigs': 2,
                                  'gc_content': 0.4588930869871599,
                                  'dna_size': 5131424})

    def test_get_number_contigs_contig_set(self):
        ret = self.getImpl().get_number_contigs(self.ctx, self.contig_set_ref_2)
        self.assertEqual(ret[0], 2)

    def test_get_gc_content_contig_set(self):
        ret = self.getImpl().get_gc_content(self.ctx, self.contig_set_ref_2)
        self.assertEqual(ret[0], 0.4588930869871599)

    def test_get_dna_size_contig_set(self):
        ret = self.getImpl().get_dna_size(self.ctx, self.contig_set_ref_2)
        self.assertEqual(ret[0], 5131424)

    def test_get_contig_ids_contig_set(self):
        ret = self.getImpl().get_contig_ids(self.ctx, self.contig_set_ref_2)
        self.assertCountEqual(ret[0], ['NC_004347', 'NC_004349'])

    def test_get_contig_lengths_contig_set(self):
        ret = self.getImpl().get_contig_lengths(self.ctx, self.contig_set_ref_2, ['NC_004349'])
        self.assertEqual(ret[0], {'NC_004349': 161613})

    def test_get_contig_gc_content_contig_set(self):
        ret = self.getImpl().get_contig_gc_content(self.ctx, self.contig_set_ref_2, ['NC_004349'])
        self.assertEqual(ret[0], {'NC_004349': 0.436883171527043})

    def test_get_contigs_contig_set(self):
        ret = self.getImpl().get_contigs(self.ctx, self.contig_set_ref_2, ['NC_004349'])
        self.assertCountEqual(ret[0][u'NC_004349'],
                              ['gc_content', 'length', 'contig_id', 'md5', 'name', 'description'])

