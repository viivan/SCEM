package com.saltwater.module.microservice.controller;

import com.saltwater.module.microservice.pojo.MicroService;
import com.saltwater.module.microservice.service.MicroServiceService;
import com.saltwater.module.user.controller.SysUserController;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import java.util.Map;
 
@Controller
@RequestMapping("/service")
public class MicroServiceController {

    private static final Logger LOG = LoggerFactory.getLogger(SysUserController.class);

    @Autowired
    MicroServiceService microServiceService;

    @RequestMapping("/page.do")
    @ResponseBody
    public Map<String, Object> findServiceList(@RequestParam(name = "pageSize") int pageSize, @RequestParam(name = "pageOffset") int pageOffset) {
        return microServiceService.findMicroServiceList(pageSize, pageOffset);
    }

}
