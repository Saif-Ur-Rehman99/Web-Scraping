import scrapy


class ScrapingSpider(scrapy.Spider):
    name = "scraping"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        books = response.css('article.product_pod')
        for book in books:
            yield {
                'name' : book.css('h3 a::text').get(),
                'price' : book.css('.product_price .price_color::text').get(),
                'url' : book.css('h3 a').attrib['href'],
            }
        
        nextpage = response.css('li.next a::attr(href)').get()

        # if url is not none that means there is another page
        if nextpage is not None:
            if 'catalogue/' in nextpage:
                nextpage_url = 'https://books.toscrape.com/' + nextpage
            else: # if url doesn't contain the catalogue/ we do have to have this
                nextpage_url = 'https://books.toscrape.com/catalogue/' + nextpage
            yield response.follow(nextpage_url, callback=self.parse)

