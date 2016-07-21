
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
 * <p>Original spec-file type: AssemblyContig</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "contig_id",
    "sequence",
    "length",
    "gc_content",
    "md5",
    "name",
    "description",
    "is_complete",
    "is_circular"
})
public class AssemblyContig {

    @JsonProperty("contig_id")
    private String contigId;
    @JsonProperty("sequence")
    private String sequence;
    @JsonProperty("length")
    private Long length;
    @JsonProperty("gc_content")
    private Double gcContent;
    @JsonProperty("md5")
    private String md5;
    @JsonProperty("name")
    private String name;
    @JsonProperty("description")
    private String description;
    @JsonProperty("is_complete")
    private Long isComplete;
    @JsonProperty("is_circular")
    private Long isCircular;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("contig_id")
    public String getContigId() {
        return contigId;
    }

    @JsonProperty("contig_id")
    public void setContigId(String contigId) {
        this.contigId = contigId;
    }

    public AssemblyContig withContigId(String contigId) {
        this.contigId = contigId;
        return this;
    }

    @JsonProperty("sequence")
    public String getSequence() {
        return sequence;
    }

    @JsonProperty("sequence")
    public void setSequence(String sequence) {
        this.sequence = sequence;
    }

    public AssemblyContig withSequence(String sequence) {
        this.sequence = sequence;
        return this;
    }

    @JsonProperty("length")
    public Long getLength() {
        return length;
    }

    @JsonProperty("length")
    public void setLength(Long length) {
        this.length = length;
    }

    public AssemblyContig withLength(Long length) {
        this.length = length;
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

    public AssemblyContig withGcContent(Double gcContent) {
        this.gcContent = gcContent;
        return this;
    }

    @JsonProperty("md5")
    public String getMd5() {
        return md5;
    }

    @JsonProperty("md5")
    public void setMd5(String md5) {
        this.md5 = md5;
    }

    public AssemblyContig withMd5(String md5) {
        this.md5 = md5;
        return this;
    }

    @JsonProperty("name")
    public String getName() {
        return name;
    }

    @JsonProperty("name")
    public void setName(String name) {
        this.name = name;
    }

    public AssemblyContig withName(String name) {
        this.name = name;
        return this;
    }

    @JsonProperty("description")
    public String getDescription() {
        return description;
    }

    @JsonProperty("description")
    public void setDescription(String description) {
        this.description = description;
    }

    public AssemblyContig withDescription(String description) {
        this.description = description;
        return this;
    }

    @JsonProperty("is_complete")
    public Long getIsComplete() {
        return isComplete;
    }

    @JsonProperty("is_complete")
    public void setIsComplete(Long isComplete) {
        this.isComplete = isComplete;
    }

    public AssemblyContig withIsComplete(Long isComplete) {
        this.isComplete = isComplete;
        return this;
    }

    @JsonProperty("is_circular")
    public Long getIsCircular() {
        return isCircular;
    }

    @JsonProperty("is_circular")
    public void setIsCircular(Long isCircular) {
        this.isCircular = isCircular;
    }

    public AssemblyContig withIsCircular(Long isCircular) {
        this.isCircular = isCircular;
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
        return ((((((((((((((((((((("AssemblyContig"+" [contigId=")+ contigId)+", sequence=")+ sequence)+", length=")+ length)+", gcContent=")+ gcContent)+", md5=")+ md5)+", name=")+ name)+", description=")+ description)+", isComplete=")+ isComplete)+", isCircular=")+ isCircular)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
