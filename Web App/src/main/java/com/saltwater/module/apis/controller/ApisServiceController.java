package com.saltwater.module.apis.controller;

import com.saltwater.module.apis.service.ApisService;
import com.saltwater.module.user.controller.SysUserController;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import java.util.Map;

@Controller
@RequestMapping("/apis")
public class ApisServiceController {
    private static final Logger LOG = LoggerFactory.getLogger(ApisServiceController.class);
 
    @Autowired
    ApisService apisService;

    @RequestMapping("/pageCount.do")
    @ResponseBody
    public String findPageCount() {
        return apisService.findPageCount().toString();
    }

    @RequestMapping("/page.do")
    @ResponseBody
    public Map<String, Object> findPage(@RequestParam(name = "pageSize") int pageSize, @RequestParam(name = "pageOffset") int pageOffset) {
        return apisService.findPage(pageSize, pageOffset);
    }
}
