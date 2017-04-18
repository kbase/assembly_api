
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
 * <p>Original spec-file type: AssemblyData</p>
 * <pre>
 * contig_id - id of the contig
 * description - description of the contig (description on fasta header rows)
 * length - (bp) length of the contig
 * gc - gc_content of the contig
 * is_circ - 0 or 1 value indicating if the contig is circular.  May be null
 *           if unknown
 * N_count - number of 'N' bases in the contig
 * md5 - md5 checksum of the sequence
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "contig_id",
    "description",
    "length",
    "gc",
    "is_circ",
    "N_count",
    "md5"
})
public class AssemblyData {

    @JsonProperty("contig_id")
    private String contigId;
    @JsonProperty("description")
    private String description;
    @JsonProperty("length")
    private Long length;
    @JsonProperty("gc")
    private Long gc;
    @JsonProperty("is_circ")
    private Long isCirc;
    @JsonProperty("N_count")
    private Long NCount;
    @JsonProperty("md5")
    private String md5;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("contig_id")
    public String getContigId() {
        return contigId;
    }

    @JsonProperty("contig_id")
    public void setContigId(String contigId) {
        this.contigId = contigId;
    }

    public AssemblyData withContigId(String contigId) {
        this.contigId = contigId;
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

    public AssemblyData withDescription(String description) {
        this.description = description;
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

    public AssemblyData withLength(Long length) {
        this.length = length;
        return this;
    }

    @JsonProperty("gc")
    public Long getGc() {
        return gc;
    }

    @JsonProperty("gc")
    public void setGc(Long gc) {
        this.gc = gc;
    }

    public AssemblyData withGc(Long gc) {
        this.gc = gc;
        return this;
    }

    @JsonProperty("is_circ")
    public Long getIsCirc() {
        return isCirc;
    }

    @JsonProperty("is_circ")
    public void setIsCirc(Long isCirc) {
        this.isCirc = isCirc;
    }

    public AssemblyData withIsCirc(Long isCirc) {
        this.isCirc = isCirc;
        return this;
    }

    @JsonProperty("N_count")
    public Long getNCount() {
        return NCount;
    }

    @JsonProperty("N_count")
    public void setNCount(Long NCount) {
        this.NCount = NCount;
    }

    public AssemblyData withNCount(Long NCount) {
        this.NCount = NCount;
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

    public AssemblyData withMd5(String md5) {
        this.md5 = md5;
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
        return ((((((((((((((((("AssemblyData"+" [contigId=")+ contigId)+", description=")+ description)+", length=")+ length)+", gc=")+ gc)+", isCirc=")+ isCirc)+", NCount=")+ NCount)+", md5=")+ md5)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
