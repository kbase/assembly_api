/*
A KBase module: AssemblyAPI
*/

module AssemblyAPI {
    /*
        Insert your typespec information here.
    */

typedef string ObjectReference;
typedef int i64;
typedef float double;
typedef int bool;

/**
 * Derived statistical information about an assembly.
 */
typedef structure {
    /** Total number of contiguous sequences. */
     i64 num_contigs;
    /** Total length of all dna sequences. */
     i64 dna_size;
    /** Proportion of guanine (G) and cytosine (C) content. */
     double gc_content;
}  AssemblyStats;

/**
 * Metadata about the external source of this Assembly.
 */
typedef structure {
    /** Name of the external source */
     string external_source;
    /** Identifier of external source */
     string external_source_id;
    /** Origination date of external source */
     string external_source_origination_date;
}  AssemblyExternalSourceInfo;

typedef structure {
    /** Contig ID */
     string contig_id;
    /** Actual contents of the sequence for this contig */
     string sequence;
    /** Length of the contig */
     i64 length;
    /** GC proportion for the contig */
     double gc_content;
    /** Hex-digest of MD5 hash of the contig's contents */
     string md5;
    /** Name of the contig */
     string name;
    /** Description of the contig */
     string description;
    /** True if this contig is complete, False otherwise */
     bool is_complete;
    /** True if this contig is circular, False otherwise */
     bool is_circular;
}  AssemblyContig;


    /**
     * Retrieve Assembly ID.
     */
     funcdef get_assembly_id( ObjectReference ref)  returns (string) authentication required;

    /**
     * Retrieve associated GenomeAnnotation objects.
     *
     * @return List of GenomeAnnotation object references
     *
     */
     funcdef get_genome_annotations( ObjectReference ref)  returns (list<ObjectReference>) authentication required;

    /**
     * Retrieve the external source information for this Assembly.
     *
     * @return Metadata about the external source
     */
     funcdef get_external_source_info( ObjectReference ref)  returns (AssemblyExternalSourceInfo) authentication required;

    /**
     * Retrieve the derived statistical information about this Assembly.
     *
     */
     funcdef get_stats( ObjectReference ref)  returns (AssemblyStats) authentication required;

    /**
     * Retrieve the number of contigs for this Assembly.
     *
     * @return Total number of contiguous sequences.
     */
     funcdef get_number_contigs( ObjectReference ref)  returns (int) authentication required;

    /**
     * Retrieve the total GC content for this Assembly.
     *
     * @return Proportion of GC content, between 0 and 1.
     */
     funcdef get_gc_content( ObjectReference ref)  returns (double) authentication required;

    /**
     * Retrieve the total DNA size for this Assembly.
     *
     * @return Total DNA size
     */
     funcdef get_dna_size( ObjectReference ref)  returns (int) authentication required;

    /**
     * Retrieve the contig identifiers for this Assembly.
     *
     * @return List of contig IDs.
     */
     funcdef get_contig_ids( ObjectReference ref)  returns (list<string>) authentication required;

    /**
     * Retrieve the lengths of the contigs in this Assembly.
     *
     * @return Mapping of contig ID to contig length.
     */
     funcdef get_contig_lengths( ObjectReference ref,
                    list<string> contig_id_list)  returns (mapping<string, int>) authentication required;

    /**
     * Retrieve the gc content for contigs in this Assembly.
     *
     * @return Mapping of contig IDs to GC content proportion.
     */
     funcdef get_contig_gc_content( ObjectReference ref,
                          list<string> contig_id_list)  returns (mapping<string, double>) authentication required;

    /**
     * Retrieve all the data for the contigs in this Assembly.
     *
     * @return Mapping of contig ID to details for that contig.
     */
     funcdef get_contigs( ObjectReference ref,
                        list<string> contig_id_list)  returns (mapping<string, AssemblyContig>) authentication required;
};
