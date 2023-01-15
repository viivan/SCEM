package com.saltwater.module.microservice.dao;

import com.saltwater.module.microservice.pojo.MicroService;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
 

@Repository
public interface MicroServiceDao extends JpaRepository<MicroService, Long> {
}
