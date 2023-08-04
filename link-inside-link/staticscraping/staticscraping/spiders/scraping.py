import scrapy


class ScrapingSpider(scrapy.Spider):
    name = "scraping"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        books = response.css('article.product_pod')

        for book in books:
            book_url = response.css('h3 a ::attr(href)').get()

            if 'calalogue/' in book_url:
                book_info = 'https://books.toscrape.com/' + book_url
            else:
                book_info =  'https://books.toscrape.com/catalogue/' + book_url
            
            yield response.follow(book_info, callback=self.parse_book_page) 

        next_page = response.css('li.next a ::attr(href)').get()
        if next_page is not None:
            if 'calalogue/' in next_page:
                nextpage_url = 'https://books.toscrape.com/' + next_page
            else:
                nextpage_url =  'https://books.toscrape.com/catalogue/' + next_page
            
            yield response.follow(nextpage_url, callback=self.parse)

    def parse_book_page(self, response):
        
        table_rows = response.css("table tr")

        yield {
            'url' : response.book_url,
            'title' : response.css('.product_main h1::text').get(),
            'price': response.css('p.price_color ::text'),
            'product_type' : table_rows[1].css('td ::text').get(),
            'price_excluding_tax' : table_rows[2].css('td ::text').get(),
            'price_including_tax' : table_rows[3].css('td ::text').get(),
            'tax' : table_rows[4].css('td ::text').get(),
            'availability' : table_rows[5].css('td ::text').get(),
            'rating' : response.css("p.star-rating").attrib['class'],
            'category' : response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get(),
            'book_description': response.xpath("//div[@id='product_description']/following-sibling::p/text()").get(),
        }