import scrapy
from scrapy_playwright.page import PageMethod
from scrapy.loader import ItemLoader
from laptop.items import LaptopItem

class GetlpSpider(scrapy.Spider):
    name = "getlp"
    allowed_domains = ["www.flipkart.com"]
    start_urls = ["https://www.flipkart.com"]


    def start_requests(self):
        base_url = "https://www.flipkart.com/search?q=laptop&page={}"

        for page in range(1, 25):  # 1 to 24
            yield scrapy.Request(
            base_url.format(page),
            meta={
                "playwright": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_load_state", "networkidle"),
                ],
            },
            callback=self.parse,
        )

    # def start_requests(self):
    #     # GET request
    #     yield scrapy.Request(self.start_urls[0],
    #                           meta={
    #                               "playwright": True,
    #                               "playwright_page_methods": [
    #                                   PageMethod("wait_for_load_state", "domcontentloaded"),
    #                                   PageMethod("wait_for_timeout", 2000),
    #                                   PageMethod("click", "span[role='button'],b3wTlE"),
    #                                   PageMethod("wait_for_timeout", 2000),
    #                                   PageMethod("fill", "input.nw1UBF.v1zwn25", "laptop"),
    #                                   PageMethod("wait_for_timeout", 2000),
    #                                   PageMethod("click", "button.XFwMiH"),
    #                                   PageMethod("wait_for_timeout", 2000),
    #                                   PageMethod("wait_for_load_state", "networkidle"),
    #                                   PageMethod("wait_for_load_state", "domcontentloaded"),
    #                                   PageMethod("wait_for_load_state", "load"),
    #                                   PageMethod("screenshot", path="lp1.png", full_page=True),


    #                               ]
    #                               })
       
        

    def parse(self, response):
        laptops= response.css("div.lvJbLV.col-12-12 div.jIjQ8S")
         
        for laptop in laptops:
            laptopItemLoader = ItemLoader(item=LaptopItem(), selector=laptop)


            laptopItemLoader.add_css("name", "div.RG5Slk::text")
            laptopItemLoader.add_css("price", "div.hZ3P6w.DeU9vF::text")
            laptopItemLoader.add_css("rating", "div.ZFwe0M.row > div.col-7-12 .MKiFS6::text")
            laptopItemLoader.add_css("original_price", "div.kRYCnD.gxR4EY::text")
            laptopItemLoader.add_css("discount", "div.col.col-5-12.mao5dl div.HQe8jr span::text ")
            laptopItemLoader.add_css("details", "div.CMXw7N > ul > li::text")
            yield laptopItemLoader.load_item()
       
        # next_page = response.css("a._9QVEpD::attr(href)").get()

        # if next_page:
        #  yield response.follow(
        #     next_page,
        #     callback=self.parse,
        #     meta={
        #         "playwright": True,
        #         "playwright_page_methods": [
        #             PageMethod("wait_for_load_state", "networkidle"),
        #         ],
        #     },
        # )

        

    
