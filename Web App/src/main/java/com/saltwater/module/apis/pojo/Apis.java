package com.saltwater.module.apis.pojo;

import org.hibernate.annotations.Cache;
import org.hibernate.annotations.CacheConcurrencyStrategy;

import javax.persistence.*;
 
@Cache(usage = CacheConcurrencyStrategy.READ_WRITE, region = "pojoCache")
@Cacheable(true)
@Entity
@Table(name = "api_data")
public class Apis {
    @Id
    @Column(name = "id", nullable = false)
    private long apiServiceId;

    @Column(name = "name")
    private String name;

    @Column(name = "apiEndpoint")
    private String apiEndpoint;

    @Column(name = "apiPortal")
    private String apiPortal;

    @Column(name = "primaryCategory")
    private String primaryCategory;

    @Column(name = "secondaryCategories")
    private String secondaryCategories;

    @Column(name = "apiProvider")
    private String apiProvider;

    @Column(name = "sslSupport")
    private String sslSupport;

    @Column(name = "apiForum")
    private String apiForum;

    @Column(name = "twitterURL")
    private String twitterURL;

    @Column(name = "interactiveConsoleURL")
    private String interactiveConsoleURL;

    @Column(name = "authenticationModel")
    private String authenticationModel;

    @Column(name = "termsOfServiceURL")
    private String termsOfServiceURL;

    @Column(name = "isApiNonProprietary")
    private String isApiNonProprietary;

    @Column(name = "scope")
    private String scope;

    @Column(name = "deviceSpecific")
    private String deviceSpecific;

    @Column(name = "docsHomePageURL")
    private String docsHomePageURL;

    @Column(name = "architecturalStyle")
    private String architecturalStyle;

    @Column(name = "supportedRequestFormats")
    private String supportedRequestFormats;

    @Column(name = "supportedResponseFormats")
    private String supportedResponseFormats;

    @Column(name = "isUnofficial")
    private String isUnofficial;

    @Column(name = "isHypermedia")
    private String isHypermedia;

    @Column(name = "restrictedAccess")
    private String restrictedAccess;

    public long getApiServiceId() {
        return apiServiceId;
    }

    public void setApiServiceId(long apiServiceId) {
        this.apiServiceId = apiServiceId;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getApiEndpoint() {
        return apiEndpoint;
    }

    public void setApiEndpoint(String apiEndpoint) {
        this.apiEndpoint = apiEndpoint;
    }

    public String getApiPortal() {
        return apiPortal;
    }

    public void setApiPortal(String apiPortal) {
        this.apiPortal = apiPortal;
    }

    public String getPrimaryCategory() {
        return primaryCategory;
    }

    public void setPrimaryCategory(String primaryCategory) {
        this.primaryCategory = primaryCategory;
    }

    public String getSecondaryCategories() {
        return secondaryCategories;
    }

    public void setSecondaryCategories(String secondaryCategories) {
        this.secondaryCategories = secondaryCategories;
    }

    public String getApiProvider() {
        return apiProvider;
    }

    public void setApiProvider(String apiProvider) {
        this.apiProvider = apiProvider;
    }

    public String getSslSupport() {
        return sslSupport;
    }

    public void setSslSupport(String sslSupport) {
        this.sslSupport = sslSupport;
    }

    public String getApiForum() {
        return apiForum;
    }

    public void setApiForum(String apiForum) {
        this.apiForum = apiForum;
    }

    public String getTwitterURL() {
        return twitterURL;
    }

    public void setTwitterURL(String twitterURL) {
        this.twitterURL = twitterURL;
    }

    public String getInteractiveConsoleURL() {
        return interactiveConsoleURL;
    }

    public void setInteractiveConsoleURL(String interactiveConsoleURL) {
        this.interactiveConsoleURL = interactiveConsoleURL;
    }

    public String getAuthenticationModel() {
        return authenticationModel;
    }

    public void setAuthenticationModel(String authenticationModel) {
        this.authenticationModel = authenticationModel;
    }

    public String getTermsOfServiceURL() {
        return termsOfServiceURL;
    }

    public void setTermsOfServiceURL(String termsOfServiceURL) {
        this.termsOfServiceURL = termsOfServiceURL;
    }

    public String getIsApiNonProprietary() {
        return isApiNonProprietary;
    }

    public void setIsApiNonProprietary(String isApiNonProprietary) {
        this.isApiNonProprietary = isApiNonProprietary;
    }

    public String getScope() {
        return scope;
    }

    public void setScope(String scope) {
        this.scope = scope;
    }

    public String getDeviceSpecific() {
        return deviceSpecific;
    }

    public void setDeviceSpecific(String deviceSpecific) {
        this.deviceSpecific = deviceSpecific;
    }

    public String getDocsHomePageURL() {
        return docsHomePageURL;
    }

    public void setDocsHomePageURL(String docsHomePageURL) {
        this.docsHomePageURL = docsHomePageURL;
    }

    public String getArchitecturalStyle() {
        return architecturalStyle;
    }

    public void setArchitecturalStyle(String architecturalStyle) {
        this.architecturalStyle = architecturalStyle;
    }

    public String getSupportedRequestFormats() {
        return supportedRequestFormats;
    }

    public void setSupportedRequestFormats(String supportedRequestFormats) {
        this.supportedRequestFormats = supportedRequestFormats;
    }

    public String getSupportedResponseFormats() {
        return supportedResponseFormats;
    }

    public void setSupportedResponseFormats(String supportedResponseFormats) {
        this.supportedResponseFormats = supportedResponseFormats;
    }

    public String getIsUnofficial() {
        return isUnofficial;
    }

    public void setIsUnofficial(String isUnofficial) {
        this.isUnofficial = isUnofficial;
    }

    public String getIsHypermedia() {
        return isHypermedia;
    }

    public void setIsHypermedia(String isHypermedia) {
        this.isHypermedia = isHypermedia;
    }

    public String getRestrictedAccess() {
        return restrictedAccess;
    }

    public void setRestrictedAccess(String restrictedAccess) {
        this.restrictedAccess = restrictedAccess;
    }
}

