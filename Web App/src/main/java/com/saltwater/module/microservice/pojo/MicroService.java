package com.saltwater.module.microservice.pojo;

import org.hibernate.annotations.Cache;
import org.hibernate.annotations.CacheConcurrencyStrategy;
import org.hibernate.annotations.GenericGenerator;

import javax.persistence.*;
 
@Cache(usage = CacheConcurrencyStrategy.READ_WRITE, region = "pojoCache")
@Cacheable(true)
@Entity
@Table(name = "service_data")
public class MicroService {

    @Id
    @GenericGenerator(name = "IdentifierGenerator2", strategy = "identity")
    @GeneratedValue(generator = "IdentifierGenerator2")
    @Column(name = "id", nullable = false)
    private long microServiceId;

    @Column(name = "service_key", nullable = false)
    private String microServiceKey;

    @Column(name = "service_name")
    private String microServiceName;

    @Column(name = "service_description")
    private String microServiceDesc;

    @Column(name = "service_host")
    private String microServiceHost;

    @Column(name = "owl_url")
    private String microServiceOwlUrl;

    @Column(name = "owls_url")
    private String microServiceOwlsUrl;

    public long getMicroServiceId() {
        return microServiceId;
    }

    public void setMicroServiceId(long microServiceId) {
        this.microServiceId = microServiceId;
    }

    public String getMicroServiceName() {
        return microServiceName;
    }

    public void setMicroServiceName(String microServiceName) {
        this.microServiceName = microServiceName;
    }

    public String getMicroServiceDesc() {
        return microServiceDesc;
    }

    public void setMicroServiceDesc(String microServiceDesc) {
        this.microServiceDesc = microServiceDesc;
    }

    public String getMicroServiceHost() {
        return microServiceHost;
    }

    public void setMicroServiceHost(String microServiceHost) {
        this.microServiceHost = microServiceHost;
    }

    public String getMicroServiceOwlUrl() {
        return microServiceOwlUrl;
    }

    public void setMicroServiceOwlUrl(String microServiceOwlUrl) {
        this.microServiceOwlUrl = microServiceOwlUrl;
    }

    public String getMicroServiceKey() {
        return microServiceKey;
    }

    public void setMicroServiceKey(String microServiceKey) {
        this.microServiceKey = microServiceKey;
    }

    public String getMicroServiceOwlsUrl() {

        return microServiceOwlsUrl;
    }

    public void setMicroServiceOwlsUrl(String microServiceOwlsUrl) {
        this.microServiceOwlsUrl = microServiceOwlsUrl;
    }
}
