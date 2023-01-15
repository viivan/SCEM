package com.saltwater.module.microservice.service;

import org.springframework.stereotype.Service;

import java.util.Map;


public interface MicroServiceService {
    Map<String, Object> findMicroServiceList(int pageSize, int pageOffset);
}
