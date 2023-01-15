package com.saltwater.module.apis.service.impl;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.saltwater.module.apis.dao.ApisServiceDao;
import com.saltwater.module.apis.pojo.Apis;
import com.saltwater.module.apis.service.ApisService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class ApisServiceImpl implements ApisService {

    public static int ITEMS_PER_PAGE = 30;

    @Autowired
    ApisServiceDao apisServiceDao;

    @Override
    public Integer findPageCount() {
        return apisServiceDao.findAll().size() / ITEMS_PER_PAGE;
    }

    @Override
    public Map<String, Object> findPage(int pageSize, int pageOffset) {
        if (pageSize < 0) {
            return null;
        }
        Page<Apis> pages = apisServiceDao.findAll(new PageRequest(pageOffset / pageSize, pageSize));
        ObjectMapper objectMapper = new ObjectMapper();
        String result = null;
        try {
            Map resultMap = new HashMap();
            resultMap.put("total", pages.getTotalElements());
            resultMap.put("rows", pages.getContent());
            return resultMap;
        } catch (Exception jpe) {
            jpe.printStackTrace();
        }

        return null;
    }
}
