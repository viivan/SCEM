package com.saltwater.module.user.controller;

import com.saltwater.module.user.pojo.SysUser;
import com.saltwater.module.user.service.SysUserService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.ModelAndView;

import javax.annotation.Resource;
import java.util.Date;
import java.util.List;

@Controller
@RequestMapping("/user")
public class SysUserController {
	 
	private static final Logger LOG = LoggerFactory.getLogger(SysUserController.class);
	
	@Autowired
	private SysUserService sysUserService;
	
	@RequestMapping("/login.do")
	@ResponseBody
	public boolean login(@RequestParam(value = "loginName", defaultValue = "") String loginName, @RequestParam(value = "loginPassword", defaultValue = "") String loginPassword) {
		return sysUserService.login(loginName,loginPassword);
	}
	
	
	@RequestMapping("/test-logback")
	@ResponseBody
	public Date testLogback() {
		LOG.trace("-----------------------------------trace");
		LOG.debug("-----------------------------------debug");
		LOG.info("-----------------------------------info");
		LOG.warn("-----------------------------------warn");
		LOG.error("-----------------------------------error");
		return new Date();
	}
	
	@RequestMapping(value = "/save-user", method = RequestMethod.POST)
	@ResponseBody
	public SysUser saveUser(SysUser sysUser) {
		if (sysUser != null) {
			sysUser.setSysUserRegisterDatetime(new Date());
			return sysUserService.saveAndUpdateSysUser(sysUser);
		}
		return null;
	}


	@RequestMapping("/test-no-ehcache/{userId}")
	@ResponseBody
	public SysUser findNoEhcache(@PathVariable("userId") Long userId) {
		//没有使用缓存，无论何时调用这个方法，控制台都会输出 sql 语句
		SysUser user = sysUserService.findBySysUserId(userId);
		return user;
	}
	
	
}
