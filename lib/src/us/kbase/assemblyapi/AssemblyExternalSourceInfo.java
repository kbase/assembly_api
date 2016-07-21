
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
 * <p>Original spec-file type: AssemblyExternalSourceInfo</p>
 * <pre>
 * *
 * * Metadata about the external source of this Assembly.
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "external_source",
    "external_source_id",
    "external_source_origination_date"
})
public class AssemblyExternalSourceInfo {

    @JsonProperty("external_source")
    private String externalSource;
    @JsonProperty("external_source_id")
    private String externalSourceId;
    @JsonProperty("external_source_origination_date")
    private String externalSourceOriginationDate;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("external_source")
    public String getExternalSource() {
        return externalSource;
    }

    @JsonProperty("external_source")
    public void setExternalSource(String externalSource) {
        this.externalSource = externalSource;
    }

    public AssemblyExternalSourceInfo withExternalSource(String externalSource) {
        this.externalSource = externalSource;
        return this;
    }

    @JsonProperty("external_source_id")
    public String getExternalSourceId() {
        return externalSourceId;
    }

    @JsonProperty("external_source_id")
    public void setExternalSourceId(String externalSourceId) {
        this.externalSourceId = externalSourceId;
    }

    public AssemblyExternalSourceInfo withExternalSourceId(String externalSourceId) {
        this.externalSourceId = externalSourceId;
        return this;
    }

    @JsonProperty("external_source_origination_date")
    public String getExternalSourceOriginationDate() {
        return externalSourceOriginationDate;
    }

    @JsonProperty("external_source_origination_date")
    public void setExternalSourceOriginationDate(String externalSourceOriginationDate) {
        this.externalSourceOriginationDate = externalSourceOriginationDate;
    }

    public AssemblyExternalSourceInfo withExternalSourceOriginationDate(String externalSourceOriginationDate) {
        this.externalSourceOriginationDate = externalSourceOriginationDate;
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
        return ((((((((("AssemblyExternalSourceInfo"+" [externalSource=")+ externalSource)+", externalSourceId=")+ externalSourceId)+", externalSourceOriginationDate=")+ externalSourceOriginationDate)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
