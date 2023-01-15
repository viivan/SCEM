import scrapy

from apispider.items import ApispiderItem

class ApiSpider(scrapy.Spider):

    # 爬虫名称
    name = "apispider"
    # 页计数
    count = 202
    # 最大爬取页数(从0开始计数)
    maxCount = 700
    # root页面
    rootPage = "https://www.programmableweb.com"
    # api页面
    apiPage = "https://www.programmableweb.com/category/all/apis?page="

    def __init__(self, *args, **kwargs):
        pass

    def start_requests(self):
        urls = [
            self.apiPage + str(self.count)
        ]
        for url in urls:
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        # 获取api链接
        links = response.xpath('//td[@class="views-field views-field-title col-md-3"]//a/@href').extract()
        # 补全api链接
        for i in range(len(links)):
            links[i] = self.rootPage + links[i]
        # 将链接添加至待爬取列表中
        for link in links:
            yield scrapy.Request(link, self.sub_parse)
        # 爬取下一页
        self.count += 1
        if self.count <= self.maxCount:
            yield scrapy.Request(self.apiPage + str(self.count), self.parse)


    def sub_parse(self, response):
        # 获取所有class=field的div中的label
        labels = response.xpath('//div[@class="field"]//label//text()').extract()
        # 获取所有class=field的div中的span
        texts = response.xpath('//div[@class="field"]//span//text()').extract()
        # 获取API名称
        name = response.xpath('//div[@class="node-header"]//h1//text()').extract()
        # 长度检测
        if len(labels) != len(texts):
            return
        # 组装为dict 方便操作
        dicts = {}
        for i in range(len(labels)):
            dicts.update({labels[i]: texts[i]})
        # 组装item
        item = ApispiderItem()
        item.setAll("")
        # 设置API名称
        if len(name) > 0:
            item["name"] = name[0]
        # 设置其他属性
        for key,value in dicts.items():
            if key == "API Endpoint":
                item["apiEndpoint"] = value
            elif key == "API Portal / Home Page":
                item["apiPortal"] = value
            elif key == "Primary Category":
                item["primaryCategory"] = value
            elif key == "Secondary Categories":
                item["secondaryCategories"] = value
            elif key == "API Provider":
                item["apiProvider"] = value
            elif key == "SSL Support":
                item["sslSupport"] = value
            elif key == "API Forum / Message Boards":
                item["apiForum"] = value
            elif key == "Twitter URL":
                item["twitterURL"] = value
            elif key == "Interactive Console URL":
                item["interactiveConsoleURL"] = value
            elif key == "Authentication Model":
                item["authenticationModel"] = value
            elif key == "Terms Of Service URL":
                item["termsOfServiceURL"] = value
            elif key == "Is the API Design/Description Non-Proprietary ?":
                item["isApiNonProprietary"] = value
            elif key == "Scope":
                item["scope"] = value
            elif key == "Device Specific":
                item["deviceSpecific"] = value
            elif key == "Docs Home Page URL":
                item["docsHomePageURL"] = value
            elif key == "Architectural Style":
                item["architecturalStyle"] = value
            elif key == "Supported Request Formats":
                item["supportedRequestFormats"] = value
            elif key == "Supported Response Formats":
                item["supportedResponseFormats"] = value
            elif key == "Is This an Unofficial API?":
                item["isUnofficial"] = value
            elif key == "Is This a Hypermedia API?":
                item["isHypermedia"] = value
            elif key == "Restricted Access ( Requires Provider Approval )":
                item["restrictedAccess"] = value

        yield item





