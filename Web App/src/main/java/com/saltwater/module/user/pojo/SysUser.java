package com.saltwater.module.user.pojo;

import com.fasterxml.jackson.annotation.JsonFormat;
import org.hibernate.annotations.Cache;
import org.hibernate.annotations.CacheConcurrencyStrategy;
import org.hibernate.annotations.GenericGenerator;

import javax.persistence.Cacheable;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.Table;
import javax.persistence.Temporal;
import javax.persistence.TemporalType;
import java.io.Serializable;
import java.util.Date;

//region = pojoCache，表示：指定缓存的区域，这个是配置在 ehcache.xml 中 
//CacheConcurrencyStrategy 资料可以看：http://www.iteye.com/problems/49111
//READ_WRITE：严格读写缓存。用于对数据同步要求严格的情况，对于经常被读、较少修改的数据，可以采用此策略缓存。不支持分布式缓存。实际应用最广泛的缓存策略。
@Cache(usage = CacheConcurrencyStrategy.READ_WRITE, region = "pojoCache")
@Cacheable(true)
@Entity
@Table(name = "sys_user")
public class SysUser implements Serializable {
	
	@Id
	@GenericGenerator(name = "IdentifierGenerator", strategy = "identity")
	@GeneratedValue(generator = "IdentifierGenerator")
	@Column(name = "sys_user_id", nullable = false)
	private Long sysUserId;
	
	@Column(name = "sys_user_login_name", nullable = false)
	private String sysUserLoginName;
	
	@Column(name = "sys_user_login_password", nullable = false)
	private String sysUserLoginPassword;
	
	@Column(name = "sys_user_register_datetime", nullable = false)
	@Temporal(TemporalType.TIMESTAMP)
	private Date sysUserRegisterDatetime;
	
	@Column(name = "sys_user_email", nullable = false)
	private String sysUserEmail;
	
	@Column(name = "sys_user_mobile", nullable = false)
	private String sysUserMobile;
	
	public Long getSysUserId() {
		return sysUserId;
	}
	
	public void setSysUserId(Long sysUserId) {
		this.sysUserId = sysUserId;
	}
	
	public String getSysUserLoginName() {
		return sysUserLoginName;
	}
	
	public void setSysUserLoginName(String sysUserLoginName) {
		this.sysUserLoginName = sysUserLoginName;
	}
	
	public String getSysUserLoginPassword() {
		return sysUserLoginPassword;
	}
	
	public void setSysUserLoginPassword(String sysUserLoginPassword) {
		this.sysUserLoginPassword = sysUserLoginPassword;
	}
	
	//由于 spring-mvc.xml 配置了日期的统一格式：yyyy-MM-dd HH:mm:ss，如果你不想要使用默认格式，可以自己定义
	@JsonFormat(pattern = "yyyy-MM-dd", timezone = "GMT+8")
	public Date getSysUserRegisterDatetime() {
		return sysUserRegisterDatetime;
	}
	
	public void setSysUserRegisterDatetime(Date sysUserRegisterDatetime) {
		this.sysUserRegisterDatetime = sysUserRegisterDatetime;
	}
	
	public String getSysUserEmail() {
		return sysUserEmail;
	}
	
	public void setSysUserEmail(String sysUserEmail) {
		this.sysUserEmail = sysUserEmail;
	}
	
	public String getSysUserMobile() {
		return sysUserMobile;
	}
	
	public void setSysUserMobile(String sysUserMobile) {
		this.sysUserMobile = sysUserMobile;
	}
	
	@Override
	public String toString() {
		return "SysUser{" +
				"sysUserId=" + sysUserId +
				", sysUserLoginName='" + sysUserLoginName + '\'' +
				", sysUserLoginPassword='" + sysUserLoginPassword + '\'' +
				", sysUserRegisterDatetime=" + sysUserRegisterDatetime +
				", sysUserEmail='" + sysUserEmail + '\'' +
				", sysUserMobile='" + sysUserMobile + '\'' +
				'}';
	}
}