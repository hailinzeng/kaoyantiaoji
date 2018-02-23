import scrapy

class eolspider(scrapy.Spider):
    name = 'eol'
    start_urls = ['http://souky.eol.cn/school_recommended.php?&code=045108&province=%E5%85%A8%E5%9B%BD&page={}'.format(page) for page in range(1, 12)]
    host = 'http://souky.eol.cn'

    def parse(self, response):
        for name in response.css('.s_w_800'):
            school_page = self.host + name.css('a::attr(href)').extract_first()
            school_name = name.css('a ::text').extract_first()
            yield scrapy.Request(school_page, meta={'school': school_page, 'name': school_name}, callback=self.parse_school)

    def parse_school(self, response):
        school_page = response.meta['school']
        school_name = response.meta['name']
        for nav in response.css('.nav-gy'):
            nav_href = self.host + nav.css('a::attr(href)').extract_first()
            nav_text = nav.xpath('./a/text()').extract_first()
            if nav_text == '调剂信息':
                yield scrapy.Request(nav_href, meta={'school': school_page, 'name': school_name, 'nav': nav_href}, callback=self.parse_tjxx)

    def parse_tjxx(self, response):
        nav = response.meta['nav']
        school = response.meta['school']
        name = response.meta['name']
        for notice in response.css('.w_830'):
            text = notice.xpath('.//p//text()').extract()
            if "," in text:
                if "\"" in text:
                    text = text.replace("\"", "\"\"")
                text = "\"" + text + "\""

            yield {
                    '0_school_name': name,
                    '1_school_page' : school,
                    '2_tjxx_url': nav,
                    '3_notice': text
                  }
