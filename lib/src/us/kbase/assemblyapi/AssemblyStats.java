
package us.kbase.assemblyapi;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: AssemblyStats</p>
 * <pre>
 * *
 * * Derived statistical information about an assembly.
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "num_contigs",
    "dna_size",
    "gc_content"
})
public class AssemblyStats {

    @JsonProperty("num_contigs")
    private Long numContigs;
    @JsonProperty("dna_size")
    private Long dnaSize;
    @JsonProperty("gc_content")
    private Double gcContent;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("num_contigs")
    public Long getNumContigs() {
        return numContigs;
    }

    @JsonProperty("num_contigs")
    public void setNumContigs(Long numContigs) {
        this.numContigs = numContigs;
    }

    public AssemblyStats withNumContigs(Long numContigs) {
        this.numContigs = numContigs;
        return this;
    }

    @JsonProperty("dna_size")
    public Long getDnaSize() {
        return dnaSize;
    }

    @JsonProperty("dna_size")
    public void setDnaSize(Long dnaSize) {
        this.dnaSize = dnaSize;
    }

    public AssemblyStats withDnaSize(Long dnaSize) {
        this.dnaSize = dnaSize;
        return this;
    }

    @JsonProperty("gc_content")
    public Double getGcContent() {
        return gcContent;
    }

    @JsonProperty("gc_content")
    public void setGcContent(Double gcContent) {
        this.gcContent = gcContent;
    }

    public AssemblyStats withGcContent(Double gcContent) {
        this.gcContent = gcContent;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((((((("AssemblyStats"+" [numContigs=")+ numContigs)+", dnaSize=")+ dnaSize)+", gcContent=")+ gcContent)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
