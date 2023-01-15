# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
 

class ApispiderItem(scrapy.Item):
    name = scrapy.Field()
    apiEndpoint = scrapy.Field()
    apiPortal = scrapy.Field()
    primaryCategory = scrapy.Field()
    secondaryCategories = scrapy.Field()
    apiProvider = scrapy.Field()
    sslSupport = scrapy.Field()
    apiForum = scrapy.Field()
    twitterURL = scrapy.Field()
    interactiveConsoleURL = scrapy.Field(default="")
    authenticationModel = scrapy.Field()
    termsOfServiceURL = scrapy.Field()
    isApiNonProprietary = scrapy.Field()
    scope = scrapy.Field()
    deviceSpecific = scrapy.Field()
    docsHomePageURL = scrapy.Field()
    architecturalStyle = scrapy.Field()
    supportedRequestFormats = scrapy.Field()
    supportedResponseFormats = scrapy.Field()
    isUnofficial = scrapy.Field()
    isHypermedia = scrapy.Field()
    restrictedAccess =  scrapy.Field()

    def setAll(self, value):
        for keys, _ in self.fields.items():
            self[keys] = value