package com.saltwater.module.microservice.service.impl;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.saltwater.module.microservice.dao.MicroServiceDao;
import com.saltwater.module.microservice.pojo.MicroService;
import com.saltwater.module.microservice.service.MicroServiceService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;

import java.io.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class MicroServiceServiceImpl implements MicroServiceService {

    @Autowired
    MicroServiceDao microServiceDao;

    @Override
    public Map<String, Object> findMicroServiceList(int pageSize, int pageOffset) {
        Page<MicroService> pages = microServiceDao.findAll(new PageRequest(pageOffset / pageSize, pageSize));
        List<MicroService> modPages = pages.getContent();
        for (MicroService ms : modPages) {
            String owlURL = ms.getMicroServiceOwlUrl();
            String owlsURL = ms.getMicroServiceOwlsUrl();
            ms.setMicroServiceOwlUrl(readFileToString(owlURL));
            ms.setMicroServiceOwlsUrl(readFileToString(owlsURL));
        }
        try {
            Map<String, Object> result = new HashMap<>();
            result.put("total", pages.getTotalElements());
            result.put("rows", pages.getContent());
            return result;
        } catch (Exception jpe) {
            jpe.printStackTrace();
        }
        return null;
    }

    private String readFileToString(String path) {
        String encoding = "UTF-8";
        String temp = Thread.currentThread().getContextClassLoader().getResource("").toString();
        String rootPath = temp.substring(temp.indexOf("file")+"file".length()+2).substring(0,temp.indexOf("target") - "target".length());
        File file = new File(rootPath + path);
        System.out.println();
        if (!file.exists()) {
            return "File not exist";
        }
        Long fileLength = file.length();
        byte[] fileContent = new byte[fileLength.intValue()];
        try {
            FileInputStream in = new FileInputStream(file);
            in.read(fileContent);
            in.close();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

        try {
            return new String(fileContent, encoding);
        } catch (UnsupportedEncodingException e) {
            return "Encoding not supported";
        }
    }
}
