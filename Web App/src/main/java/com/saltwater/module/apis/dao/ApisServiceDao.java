package com.saltwater.module.apis.dao;

import com.saltwater.module.apis.pojo.Apis;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.repository.PagingAndSortingRepository;
import org.springframework.stereotype.Repository;
 
@Repository
public interface ApisServiceDao extends JpaRepository<Apis, Long>, PagingAndSortingRepository<Apis, Long> {

}
