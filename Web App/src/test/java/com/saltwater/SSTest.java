package com.saltwater;

import com.saltwater.module.apis.service.ApisService;
import com.saltwater.module.microservice.service.MicroServiceService;
import com.saltwater.module.user.pojo.SysUser;
import com.saltwater.module.user.service.SysUserService;
import org.junit.Ignore;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

import javax.annotation.Resource;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

@Ignore
@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(locations = {"classpath*:spring/applicationContext*.xml"})
public class SSTest {
	
	
	@Autowired
	private SysUserService sysUserService;

	@Autowired
	private MicroServiceService microServiceService;

	@Autowired
	private  ApisService apisService;
	
	@Test
	public void testRunnable() {
		//System.out.println("FUCK:" + microServiceService.findMicroServiceList());
		System.out.println("FUCK:" + apisService.findPage(0,20));
	}

}
