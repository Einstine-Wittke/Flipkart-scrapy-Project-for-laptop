from urllib import response

import scrapy
from scrapy_playwright.page import PageMethod
from scrapy.loader import ItemLoader
from laptop.items import LaptopItem

class GetlpSpider(scrapy.Spider):
    name = "getlp"
    allowed_domains = ["www.flipkart.com"]
    start_urls = ["https://www.flipkart.com"]


    def start_requests(self):
        # GET request
        yield scrapy.Request(self.start_urls[0],
                              meta={
                                  "playwright": True,
                                  "playwright_include_page": True,
                                  "playwright_page_methods": [
                                      PageMethod("wait_for_load_state", "domcontentloaded"),
                                      PageMethod("wait_for_timeout", 2000),
                                      PageMethod("click", "span[role='button'],b3wTlE"),
                                      PageMethod("wait_for_timeout", 2000),
                                      PageMethod("fill", "input[name='q']", "laptop"),
                                      PageMethod("wait_for_timeout", 2000),
                                      PageMethod("click", "button.XFwMiH"),
                                      PageMethod("wait_for_timeout", 2000),
                                      PageMethod("wait_for_load_state", "networkidle"),
                                      PageMethod("wait_for_load_state", "domcontentloaded"),
                                      PageMethod("wait_for_load_state", "load"),
                                      PageMethod("screenshot", path="lp1.png", full_page=True),


                                  ]
                                  })
       
        

    # def parse(self, response):
    #     laptops= response.css("div.lvJbLV.col-12-12 div.jIjQ8S")
         
    #     for laptop in laptops:
    #         laptopItemLoader = ItemLoader(item=LaptopItem(), selector=laptop)


    #         laptopItemLoader.add_css("name", "div.RG5Slk::text")
    #         laptopItemLoader.add_css("price", "div.hZ3P6w.DeU9vF::text")
    #         laptopItemLoader.add_css("rating", "div.ZFwe0M.row > div.col-7-12 .MKiFS6::text")
    #         laptopItemLoader.add_css("original_price", "div.kRYCnD.gxR4EY::text")
    #         laptopItemLoader.add_css("discount", "div.col.col-5-12.mao5dl div.HQe8jr span::text ")
    #         laptopItemLoader.add_css("details", "div.CMXw7N > ul > li::text")
    #         yield laptopItemLoader.load_item()
       
        # next_page = response.css("a.jgg0SZ span::attr(href)").get()

    # async def parse(self, response):

    #     page = response.meta["playwright_page"]

    #     laptops = response.css("div.lvJbLV.col-12-12 div.jIjQ8S")

    #     for laptop in laptops:
    #         laptopItemLoader = ItemLoader(item=LaptopItem(), selector=laptop)

    #         laptopItemLoader.add_css("name", "div.RG5Slk::text")
    #         laptopItemLoader.add_css("price", "div.hZ3P6w.DeU9vF::text")
    #         laptopItemLoader.add_css("rating", "div.ZFwe0M.row > div.col-7-12 .MKiFS6::text")
    #         laptopItemLoader.add_css("original_price", "div.kRYCnD.gxR4EY::text")
    #         laptopItemLoader.add_css("discount", "div.col.col-5-12.mao5dl div.HQe8jr span::text")
    #         laptopItemLoader.add_css("details", "div.CMXw7N > ul > li::text")

    #         yield laptopItemLoader.load_item()

    # # NEXT PAGE BUTTON
    #     next_button = await page.query_selector("a.jgg0SZ ")

    #     if next_button:
    #         self.logger.info("Going to next page...")

    #         await next_button.click()
    #         await page.wait_for_load_state("networkidle")
    #         await page.wait_for_timeout(2000)

    #     else:
    #         self.logger.info("Last page reached")
    #         breakpoint()

    #     await page.close()

    
    async def parse(self, response):

        page = response.meta["playwright_page"]

        page_number = 1

        while True:

            self.logger.info(f"Scraping page {page_number}")

            html = await page.content()
            response = response.replace(body=html)

            laptops = response.css("div.lvJbLV.col-12-12 div.jIjQ8S")

            for laptop in laptops:

                laptopItemLoader = ItemLoader(item=LaptopItem(), selector=laptop)

                laptopItemLoader.add_css("name", "div.RG5Slk::text")
                laptopItemLoader.add_css("price", "div.hZ3P6w.DeU9vF::text")
                laptopItemLoader.add_css("rating", "div.ZFwe0M.row > div.col-7-12 .MKiFS6::text")
                laptopItemLoader.add_css("original_price", "div.kRYCnD.gxR4EY::text")
                laptopItemLoader.add_css("discount", "div.col.col-5-12.mao5dl div.HQe8jr span::text")
                laptopItemLoader.add_css("details", "div.CMXw7N > ul > li::text")

                yield laptopItemLoader.load_item()

        # NEXT BUTTON
            next_button = await page.query_selector("a.jgg0SZ:has-text('Next')")

            if not next_button:
                self.logger.info("Last Page Reached")
                break

            await next_button.click()
            await page.wait_for_load_state("domcontentloaded")

            page_number += 1

        await page.close()