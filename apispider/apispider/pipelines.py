# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from apispider.items import ApispiderItem

class ApispiderPipeline(object):

    def __init__(self):
        self.conn = pymysql.connect("localhost", "root", "daijiawei", "gd_database", use_unicode=True, charset='utf8')
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def process_item(self, item, spider):
        if isinstance(item, ApispiderItem):
            self.cursor.execute(
                "insert into api_data(name, apiEndpoint, apiPortal, primaryCategory, secondaryCategories, apiProvider, sslSupport, apiForum, twitterURL, interactiveConsoleURL, authenticationModel, termsOfServiceURL, isApiNonProprietary, scope, deviceSpecific, docsHomePageURL, architecturalStyle, supportedRequestFormats, supportedResponseFormats, isUnofficial, isHypermedia, restrictedAccess) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (item["name"], item["apiEndpoint"], item["apiPortal"], item["primaryCategory"],
                  item["secondaryCategories"], item["apiProvider"], item["sslSupport"], item["apiForum"],
                  item["twitterURL"], item["interactiveConsoleURL"], item["authenticationModel"],
                  item["termsOfServiceURL"], item["isApiNonProprietary"], item["scope"], item["deviceSpecific"],
                  item["docsHomePageURL"], item["architecturalStyle"], item["supportedRequestFormats"],
                  item["supportedResponseFormats"], item["isUnofficial"], item["isHypermedia"],
                  item["restrictedAccess"]))
            self.conn.commit()
        return item