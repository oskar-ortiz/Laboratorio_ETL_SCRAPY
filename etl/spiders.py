import scrapy


class BooksSpider(scrapy.Spider):
    name = "books_etl"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/catalogue/page-1.html"]

    def parse(self, response):
        for book in response.css("article.product_pod"):
            detail_url = response.urljoin(book.css("h3 a::attr(href)").get())
            yield response.follow(detail_url, self.parse_book)

        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_book(self, response):
        rating = response.css("div.product_main p.star-rating::attr(class)").get("")
        availability = response.css("div.product_main p.instock::text").getall()
        description = response.css("#product_description + p::text").get("")

        yield {
            "fuente": "Books to Scrape",
            "tipo": "libro",
            "nombre": response.css("div.product_main h1::text").get(""),
            "precio": response.css("div.product_main p.price_color::text").get(""),
            "calificacion": rating.replace("star-rating", "").strip(),
            "url": response.url,
            "categoria": response.css("ul.breadcrumb li:nth-child(3) a::text").get(""),
            "disponibilidad": " ".join(value.strip() for value in availability),
            "descripcion": description,
        }


class LaptopsSpider(scrapy.Spider):
    name = "laptops_etl"
    allowed_domains = ["webscraper.io"]
    start_urls = [
        "https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops"
    ]

    def parse(self, response):
        for product in response.css("div.card.thumbnail"):
            yield {
                "fuente": "Web Scraper Test Sites",
                "tipo": "tecnologia",
                "nombre": product.css("a.title::attr(title)").get(""),
                "precio": product.css("h4.price span[itemprop='price']::text").get(""),
                "calificacion": product.css("div.ratings p::attr(data-rating)").get(""),
                "url": response.urljoin(product.css("a.title::attr(href)").get("")),
                "categoria": "Laptops",
                "disponibilidad": "",
                "descripcion": product.css("p.description::text").get(""),
            }

        next_page = response.css("ul.pagination li a::attr(href)").getall()
        if next_page:
            current_page = response.url
            following_pages = [response.urljoin(url) for url in next_page]
            for page in following_pages:
                if page != current_page:
                    yield response.follow(page, self.parse)
