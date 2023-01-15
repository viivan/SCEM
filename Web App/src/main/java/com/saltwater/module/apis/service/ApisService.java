package com.saltwater.module.apis.service;

import java.util.Map;
 
public interface ApisService {

    public Integer findPageCount();

    public Map<String, Object> findPage(int page, int pageOffset);

}
