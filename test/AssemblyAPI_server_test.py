import unittest
import os
import json
import time
import shutil

from AssemblyUtil.AssemblyUtilClient import AssemblyUtil

from os import environ
try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

from pprint import pprint

from biokbase.workspace.client import Workspace as workspaceService
from AssemblyAPI.AssemblyAPIImpl import AssemblyAPI
from AssemblyAPI.AssemblyAPIServer import MethodContext


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

        cls.obj_name = "7989/489/2"
        cls.contigs = [u'NZ_ALQT01000016']

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
        pprint(contigset_data)
        saveData = {
            'type': 'KBaseGenomes.ContigSet',
            'data': contigset_data,
            'name': 'contigset'
        }
        cls.contig_set_info = cls.wsClient.save_objects({'workspace': cls.wsName, 'objects': [saveData]})[0]
        pprint(cls.contig_set_info)
        cls.contig_set_ref = str(cls.contig_set_info[6]) + '/' + str(cls.contig_set_info[0]) + '/' + str(cls.contig_set_info[4])
        print('ContigSet1:' + cls.contig_set_ref)


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
        ret = self.getImpl().search_contigs(self.getContext(), search_params)[0]
        self.assertEquals(ret['num_found'], 41)
        self.assertEquals(ret['query'], '')
        self.assertEquals(ret['start'], 0)
        self.assertEquals(len(ret['contigs']), 41)
        self.assertEquals(ret['contigs'][0]['contig_id'], 'k41_1')
        self.assertEquals(ret['contigs'][0]['gc'], None)
        self.assertEquals(ret['contigs'][0]['description'], 'k41_1 flag=0 multi=10.6142 len=2628')
        self.assertEquals(ret['contigs'][1]['contig_id'], 'k41_3')

        search_params = {'ref': self.contig_set_ref, 'sort_by': [['gc', 1]]}
        ret = self.getImpl().search_contigs(self.getContext(), search_params)[0]
        self.assertEquals(ret['num_found'], 41)
        self.assertEquals(ret['query'], '')
        self.assertEquals(ret['start'], 0)
        self.assertEquals(len(ret['contigs']), 41)

    def test_search_assembly(self):
        # no query
        search_params = {'ref': self.assembly_ref_1}
        ret = self.getImpl().search_contigs(self.getContext(), search_params)[0]
        self.assertEquals(ret['num_found'], 15)
        self.assertEquals(ret['query'], '')
        self.assertEquals(ret['start'], 0)
        self.assertEquals(len(ret['contigs']), 15)
        self.assertEquals(ret['contigs'][0]['contig_id'], 'NZ_ALQT01000009')
        self.assertEquals(ret['contigs'][0]['gc'], 0.30286)
        self.assertEquals(ret['contigs'][0]['description'], 'blah')
        self.assertEquals(ret['contigs'][1]['contig_id'], 'NZ_ALQT01000008')
        self.assertEquals(ret['contigs'][2]['contig_id'], 'NZ_ALQT01000014')

        # with query
        search_params = {'ref': self.assembly_ref_1, 'query': 'ALQT01000015'}
        ret = self.getImpl().search_contigs(self.getContext(), search_params)[0]
        self.assertEquals(ret['num_found'], 1)
        self.assertEquals(ret['query'], 'ALQT01000015')
        self.assertEquals(ret['start'], 0)
        self.assertEquals(len(ret['contigs']), 1)
        self.assertEquals(ret['contigs'][0]['contig_id'], 'NZ_ALQT01000015')
        self.assertEquals(ret['contigs'][0]['description'], 'this is a description')

        # with limit
        search_params = {'ref': self.assembly_ref_1, 'limit': 2}
        ret = self.getImpl().search_contigs(self.getContext(), search_params)[0]
        self.assertEquals(ret['num_found'], 15)
        self.assertEquals(ret['query'], '')
        self.assertEquals(ret['start'], 0)
        self.assertEquals(len(ret['contigs']), 2)
        self.assertEquals(ret['contigs'][0]['contig_id'], 'NZ_ALQT01000009')
        self.assertEquals(ret['contigs'][1]['contig_id'], 'NZ_ALQT01000008')

        # with limit
        search_params = {'ref': self.assembly_ref_1, 'start': 2, 'limit': 2}
        ret = self.getImpl().search_contigs(self.getContext(), search_params)[0]
        self.assertEquals(ret['num_found'], 15)
        self.assertEquals(ret['query'], '')
        self.assertEquals(ret['start'], 2)
        self.assertEquals(len(ret['contigs']), 2)
        self.assertEquals(ret['contigs'][0]['contig_id'], 'NZ_ALQT01000014')
        self.assertEquals(ret['contigs'][1]['contig_id'], 'NZ_ALQT01000015')

        # sort by gc
        search_params = {'ref': self.assembly_ref_1, 'limit': 5, 'sort_by': [['gc', 0]]}
        ret = self.getImpl().search_contigs(self.getContext(), search_params)[0]
        self.assertEquals(ret['num_found'], 15)
        self.assertEquals(ret['query'], '')
        self.assertEquals(ret['start'], 0)
        self.assertEquals(len(ret['contigs']), 5)
        self.assertEquals(ret['contigs'][0]['contig_id'], 'NZ_ALQT01000010')
        self.assertEquals(ret['contigs'][1]['contig_id'], 'NZ_ALQT01000004')

        search_params = {'ref': self.assembly_ref_1, 'sort_by': [['gc', 1]]}
        ret = self.getImpl().search_contigs(self.getContext(), search_params)[0]
        self.assertEquals(ret['num_found'], 15)
        self.assertEquals(ret['query'], '')
        self.assertEquals(ret['start'], 0)
        self.assertEquals(len(ret['contigs']), 15)
        self.assertEquals(ret['contigs'][0]['contig_id'], 'NZ_ALQT01000009')
        self.assertEquals(ret['contigs'][1]['contig_id'], 'NZ_ALQT01000003')
        self.assertEquals(ret['contigs'][2]['contig_id'], 'NZ_ALQT01000005')



    def test_get_assembly_id(self):
        ret = self.getImpl().get_assembly_id(self.getContext(), self.obj_name)
        self.assertEqual(ret[0],u'GCF_000288855.1_assembly')

    def test_get_genome_annotations(self):
        ret = self.getImpl().get_genome_annotations(self.getContext(), self.obj_name)
        self.assertEqual(ret[0],['7989/498/2'])

    def test_get_external_source_info(self):
        ret = self.getImpl().get_external_source_info(self.getContext(), self.obj_name)
        self.assertEqual(ret[0],{u'external_source': u'unknown_source', u'external_source_id': u'GCF_000288855.1_2016_07_17_13_53_33.fa', u'external_source_origination_date': u'21-AUG-2015'})

#     funcdef get_genome_annotations( ObjectReference ref)  returns (list<ObjectReference>) authentication required;
#     funcdef get_external_source_info( ObjectReference ref)  returns (AssemblyExternalSourceInfo) authentication required;
#     funcdef get_stats( ObjectReference ref)  returns (AssemblyStats) authentication required;
    def test_get_stats(self):
        ret = self.getImpl().get_stats(self.getContext(), self.obj_name)
        self.assertEqual(ret[0],{u'num_contigs': 21, u'gc_content': 0.35178740497572963, u'dna_size': 2097622})

#     funcdef get_number_contigs( ObjectReference ref)  returns (int) authentication required;
    def test_get_number_contigs(self):
        ret = self.getImpl().get_number_contigs(self.getContext(), self.obj_name)
        self.assertEqual(ret[0],21)

#     funcdef get_gc_content( ObjectReference ref)  returns (double) authentication required;
    def test_get_gc_content(self):
        ret = self.getImpl().get_gc_content(self.getContext(), self.obj_name)
        self.assertEqual(ret[0],0.35178740497572963)

#     funcdef get_dna_size( ObjectReference ref)  returns (int) authentication required;
    def test_get_dna_size(self):
        ret = self.getImpl().get_dna_size(self.getContext(), self.obj_name)
        self.assertEqual(ret[0], 2097622)

#     funcdef get_contig_ids( ObjectReference ref)  returns (list<string>) authentication required;
    def test_get_contig_ids(self):
        ret = self.getImpl().get_contig_ids(self.getContext(), self.obj_name)
        self.assertEqual(ret[0], [u'NZ_ALQT01000016', u'NZ_ALQT01000020', u'NZ_ALQT01000021', u'NZ_ALQT01000017', u'NZ_ALQT01000018', u'NZ_ALQT01000019', u'NZ_ALQT01000009', u'NZ_ALQT01000008', u'NZ_ALQT01000014', u'NZ_ALQT01000015', u'NZ_ALQT01000012', u'NZ_ALQT01000013', u'NZ_ALQT01000010', u'NZ_ALQT01000011', u'NZ_ALQT01000001', u'NZ_ALQT01000003', u'NZ_ALQT01000002', u'NZ_ALQT01000005', u'NZ_ALQT01000004', u'NZ_ALQT01000007', u'NZ_ALQT01000006'])

#     funcdef get_contig_lengths( ObjectReference ref,
    def test_get_contig_lengths(self):
        ret = self.getImpl().get_contig_lengths(self.getContext(), self.obj_name,self.contigs)
        self.assertEqual(ret[0], 0)

#     funcdef get_contig_gc_content( ObjectReference ref,
    def test_get_contig_lengths(self):
        ret = self.getImpl().get_contig_gc_content(self.getContext(), self.obj_name,self.contigs)
        self.assertEqual(ret[0], {u'NZ_ALQT01000016': 0.35366172461440787})

#     funcdef get_contigs( ObjectReference ref,
    def test_get_contigs(self):
        ret = self.getImpl().get_contigs(self.getContext(), self.obj_name,self.contigs)
        self.assertEqual(ret[0][u'NZ_ALQT01000016']['length'], 53554)

