package com.saltwater.module.user.service.impl;

import com.saltwater.module.user.dao.SysUserDao;
import com.saltwater.module.user.pojo.SysUser;
import com.saltwater.module.user.service.SysUserService;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;

@Service
public class SysUserServiceImpl implements SysUserService {
	
	@Resource
	private SysUserDao sysUserDao;

	@Override
	public boolean login(String loginName, String loginPassword) {
		SysUser result = sysUserDao.findBySysUserLoginName(loginName);
		if (result != null && result.getSysUserLoginPassword().equals(loginPassword)) {
			return true;
		} else {
			return false;
		}
	}

	@Override
	public SysUser saveAndUpdateSysUser(SysUser sysUser) {
		return sysUserDao.save(sysUser);
	}

	@Override
	public void deleteBySysUserId(Long sysUserId) {
		sysUserDao.deleteBySysUserId(sysUserId);
	}
	
	@Override
	public SysUser findBySysUserId(Long sysUserId) {
		return sysUserDao.findBySysUserId(sysUserId);
	}
	
	@Override
	public SysUser findBySysUserLoginName(String sysUserLoginName) {
		return sysUserDao.findBySysUserLoginName(sysUserLoginName);
	}
	

}
