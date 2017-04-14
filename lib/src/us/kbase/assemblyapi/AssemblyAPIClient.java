package us.kbase.assemblyapi;

import com.fasterxml.jackson.core.type.TypeReference;
import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import us.kbase.auth.AuthToken;
import us.kbase.common.service.JsonClientCaller;
import us.kbase.common.service.JsonClientException;
import us.kbase.common.service.RpcContext;
import us.kbase.common.service.UnauthorizedException;

/**
 * <p>Original spec-file module name: AssemblyAPI</p>
 * <pre>
 * A KBase module: AssemblyAPI
 * </pre>
 */
public class AssemblyAPIClient {
    private JsonClientCaller caller;
    private String serviceVersion = null;


    /** Constructs a client with a custom URL and no user credentials.
     * @param url the URL of the service.
     */
    public AssemblyAPIClient(URL url) {
        caller = new JsonClientCaller(url);
    }
    /** Constructs a client with a custom URL.
     * @param url the URL of the service.
     * @param token the user's authorization token.
     * @throws UnauthorizedException if the token is not valid.
     * @throws IOException if an IOException occurs when checking the token's
     * validity.
     */
    public AssemblyAPIClient(URL url, AuthToken token) throws UnauthorizedException, IOException {
        caller = new JsonClientCaller(url, token);
    }

    /** Constructs a client with a custom URL.
     * @param url the URL of the service.
     * @param user the user name.
     * @param password the password for the user name.
     * @throws UnauthorizedException if the credentials are not valid.
     * @throws IOException if an IOException occurs when checking the user's
     * credentials.
     */
    public AssemblyAPIClient(URL url, String user, String password) throws UnauthorizedException, IOException {
        caller = new JsonClientCaller(url, user, password);
    }

    /** Constructs a client with a custom URL
     * and a custom authorization service URL.
     * @param url the URL of the service.
     * @param user the user name.
     * @param password the password for the user name.
     * @param auth the URL of the authorization server.
     * @throws UnauthorizedException if the credentials are not valid.
     * @throws IOException if an IOException occurs when checking the user's
     * credentials.
     */
    public AssemblyAPIClient(URL url, String user, String password, URL auth) throws UnauthorizedException, IOException {
        caller = new JsonClientCaller(url, user, password, auth);
    }

    /** Get the token this client uses to communicate with the server.
     * @return the authorization token.
     */
    public AuthToken getToken() {
        return caller.getToken();
    }

    /** Get the URL of the service with which this client communicates.
     * @return the service URL.
     */
    public URL getURL() {
        return caller.getURL();
    }

    /** Set the timeout between establishing a connection to a server and
     * receiving a response. A value of zero or null implies no timeout.
     * @param milliseconds the milliseconds to wait before timing out when
     * attempting to read from a server.
     */
    public void setConnectionReadTimeOut(Integer milliseconds) {
        this.caller.setConnectionReadTimeOut(milliseconds);
    }

    /** Check if this client allows insecure http (vs https) connections.
     * @return true if insecure connections are allowed.
     */
    public boolean isInsecureHttpConnectionAllowed() {
        return caller.isInsecureHttpConnectionAllowed();
    }

    /** Deprecated. Use isInsecureHttpConnectionAllowed().
     * @deprecated
     */
    public boolean isAuthAllowedForHttp() {
        return caller.isAuthAllowedForHttp();
    }

    /** Set whether insecure http (vs https) connections should be allowed by
     * this client.
     * @param allowed true to allow insecure connections. Default false
     */
    public void setIsInsecureHttpConnectionAllowed(boolean allowed) {
        caller.setInsecureHttpConnectionAllowed(allowed);
    }

    /** Deprecated. Use setIsInsecureHttpConnectionAllowed().
     * @deprecated
     */
    public void setAuthAllowedForHttp(boolean isAuthAllowedForHttp) {
        caller.setAuthAllowedForHttp(isAuthAllowedForHttp);
    }

    /** Set whether all SSL certificates, including self-signed certificates,
     * should be trusted.
     * @param trustAll true to trust all certificates. Default false.
     */
    public void setAllSSLCertificatesTrusted(final boolean trustAll) {
        caller.setAllSSLCertificatesTrusted(trustAll);
    }
    
    /** Check if this client trusts all SSL certificates, including
     * self-signed certificates.
     * @return true if all certificates are trusted.
     */
    public boolean isAllSSLCertificatesTrusted() {
        return caller.isAllSSLCertificatesTrusted();
    }
    /** Sets streaming mode on. In this case, the data will be streamed to
     * the server in chunks as it is read from disk rather than buffered in
     * memory. Many servers are not compatible with this feature.
     * @param streamRequest true to set streaming mode on, false otherwise.
     */
    public void setStreamingModeOn(boolean streamRequest) {
        caller.setStreamingModeOn(streamRequest);
    }

    /** Returns true if streaming mode is on.
     * @return true if streaming mode is on.
     */
    public boolean isStreamingModeOn() {
        return caller.isStreamingModeOn();
    }

    public void _setFileForNextRpcResponse(File f) {
        caller.setFileForNextRpcResponse(f);
    }

    public String getServiceVersion() {
        return this.serviceVersion;
    }

    public void setServiceVersion(String newValue) {
        this.serviceVersion = newValue;
    }

    /**
     * <p>Original spec-file function name: search_contigs</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.assemblyapi.SearchAssemblyOptions SearchAssemblyOptions}
     * @return   parameter "result" of type {@link us.kbase.assemblyapi.SearchAssemblyResult SearchAssemblyResult}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public SearchAssemblyResult searchContigs(SearchAssemblyOptions params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<SearchAssemblyResult>> retType = new TypeReference<List<SearchAssemblyResult>>() {};
        List<SearchAssemblyResult> res = caller.jsonrpcCall("AssemblyAPI.search_contigs", args, retType, true, false, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_assembly_id</p>
     * <pre>
     * *
     * * Retrieve Assembly ID.
     * </pre>
     * @param   ref   instance of original type "ObjectReference" (Insert your typespec information here.)
     * @return   instance of String
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public String getAssemblyId(String ref, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(ref);
        TypeReference<List<String>> retType = new TypeReference<List<String>>() {};
        List<String> res = caller.jsonrpcCall("AssemblyAPI.get_assembly_id", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_genome_annotations</p>
     * <pre>
     * *
     * * Retrieve associated GenomeAnnotation objects.
     * *
     * * @return List of GenomeAnnotation object references
     * *
     * </pre>
     * @param   ref   instance of original type "ObjectReference" (Insert your typespec information here.)
     * @return   instance of list of original type "ObjectReference" (Insert your typespec information here.)
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public List<String> getGenomeAnnotations(String ref, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(ref);
        TypeReference<List<List<String>>> retType = new TypeReference<List<List<String>>>() {};
        List<List<String>> res = caller.jsonrpcCall("AssemblyAPI.get_genome_annotations", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_external_source_info</p>
     * <pre>
     * *
     * * Retrieve the external source information for this Assembly.
     * *
     * * @return Metadata about the external source
     * </pre>
     * @param   ref   instance of original type "ObjectReference" (Insert your typespec information here.)
     * @return   instance of type {@link us.kbase.assemblyapi.AssemblyExternalSourceInfo AssemblyExternalSourceInfo}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public AssemblyExternalSourceInfo getExternalSourceInfo(String ref, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(ref);
        TypeReference<List<AssemblyExternalSourceInfo>> retType = new TypeReference<List<AssemblyExternalSourceInfo>>() {};
        List<AssemblyExternalSourceInfo> res = caller.jsonrpcCall("AssemblyAPI.get_external_source_info", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_stats</p>
     * <pre>
     * *
     * * Retrieve the derived statistical information about this Assembly.
     * *
     * </pre>
     * @param   ref   instance of original type "ObjectReference" (Insert your typespec information here.)
     * @return   instance of type {@link us.kbase.assemblyapi.AssemblyStats AssemblyStats}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public AssemblyStats getStats(String ref, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(ref);
        TypeReference<List<AssemblyStats>> retType = new TypeReference<List<AssemblyStats>>() {};
        List<AssemblyStats> res = caller.jsonrpcCall("AssemblyAPI.get_stats", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_number_contigs</p>
     * <pre>
     * *
     * * Retrieve the number of contigs for this Assembly.
     * *
     * * @return Total number of contiguous sequences.
     * </pre>
     * @param   ref   instance of original type "ObjectReference" (Insert your typespec information here.)
     * @return   instance of Long
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public Long getNumberContigs(String ref, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(ref);
        TypeReference<List<Long>> retType = new TypeReference<List<Long>>() {};
        List<Long> res = caller.jsonrpcCall("AssemblyAPI.get_number_contigs", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_gc_content</p>
     * <pre>
     * *
     * * Retrieve the total GC content for this Assembly.
     * *
     * * @return Proportion of GC content, between 0 and 1.
     * </pre>
     * @param   ref   instance of original type "ObjectReference" (Insert your typespec information here.)
     * @return   instance of original type "double"
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public Double getGcContent(String ref, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(ref);
        TypeReference<List<Double>> retType = new TypeReference<List<Double>>() {};
        List<Double> res = caller.jsonrpcCall("AssemblyAPI.get_gc_content", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_dna_size</p>
     * <pre>
     * *
     * * Retrieve the total DNA size for this Assembly.
     * *
     * * @return Total DNA size
     * </pre>
     * @param   ref   instance of original type "ObjectReference" (Insert your typespec information here.)
     * @return   instance of Long
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public Long getDnaSize(String ref, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(ref);
        TypeReference<List<Long>> retType = new TypeReference<List<Long>>() {};
        List<Long> res = caller.jsonrpcCall("AssemblyAPI.get_dna_size", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_contig_ids</p>
     * <pre>
     * *
     * * Retrieve the contig identifiers for this Assembly.
     * *
     * * @return List of contig IDs.
     * </pre>
     * @param   ref   instance of original type "ObjectReference" (Insert your typespec information here.)
     * @return   instance of list of String
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public List<String> getContigIds(String ref, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(ref);
        TypeReference<List<List<String>>> retType = new TypeReference<List<List<String>>>() {};
        List<List<String>> res = caller.jsonrpcCall("AssemblyAPI.get_contig_ids", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_contig_lengths</p>
     * <pre>
     * *
     * * Retrieve the lengths of the contigs in this Assembly.
     * *
     * * @return Mapping of contig ID to contig length.
     * </pre>
     * @param   ref   instance of original type "ObjectReference" (Insert your typespec information here.)
     * @param   contigIdList   instance of list of String
     * @return   instance of mapping from String to Long
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public Map<String,Long> getContigLengths(String ref, List<String> contigIdList, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(ref);
        args.add(contigIdList);
        TypeReference<List<Map<String,Long>>> retType = new TypeReference<List<Map<String,Long>>>() {};
        List<Map<String,Long>> res = caller.jsonrpcCall("AssemblyAPI.get_contig_lengths", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_contig_gc_content</p>
     * <pre>
     * *
     * * Retrieve the gc content for contigs in this Assembly.
     * *
     * * @return Mapping of contig IDs to GC content proportion.
     * </pre>
     * @param   ref   instance of original type "ObjectReference" (Insert your typespec information here.)
     * @param   contigIdList   instance of list of String
     * @return   instance of mapping from String to original type "double"
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public Map<String,Double> getContigGcContent(String ref, List<String> contigIdList, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(ref);
        args.add(contigIdList);
        TypeReference<List<Map<String,Double>>> retType = new TypeReference<List<Map<String,Double>>>() {};
        List<Map<String,Double>> res = caller.jsonrpcCall("AssemblyAPI.get_contig_gc_content", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_contigs</p>
     * <pre>
     * *
     * * Retrieve all the data for the contigs in this Assembly.
     * *
     * * @return Mapping of contig ID to details for that contig.
     * </pre>
     * @param   ref   instance of original type "ObjectReference" (Insert your typespec information here.)
     * @param   contigIdList   instance of list of String
     * @return   instance of mapping from String to type {@link us.kbase.assemblyapi.AssemblyContig AssemblyContig}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public Map<String,AssemblyContig> getContigs(String ref, List<String> contigIdList, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(ref);
        args.add(contigIdList);
        TypeReference<List<Map<String,AssemblyContig>>> retType = new TypeReference<List<Map<String,AssemblyContig>>>() {};
        List<Map<String,AssemblyContig>> res = caller.jsonrpcCall("AssemblyAPI.get_contigs", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    public Map<String, Object> status(RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        TypeReference<List<Map<String, Object>>> retType = new TypeReference<List<Map<String, Object>>>() {};
        List<Map<String, Object>> res = caller.jsonrpcCall("AssemblyAPI.status", args, retType, true, false, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }
}
