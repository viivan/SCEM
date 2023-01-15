package com.saltwater.module.user.service;

import com.saltwater.module.user.pojo.SysUser;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;

import java.util.List;
 
public interface SysUserService {

	boolean login(String loginName, String loginPassword);

	SysUser saveAndUpdateSysUser(SysUser sysUser);

	SysUser findBySysUserId(Long sysUserId);
	
	SysUser findBySysUserLoginName(String sysUserLoginName);
	
	void deleteBySysUserId(Long sysUserId);
}
