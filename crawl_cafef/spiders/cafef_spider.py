import scrapy
from datetime import datetime, time
from crawl_cafef.items import NewItem
from elasticsearch import Elasticsearch
import hashlib


class CafefSpiderSpider(scrapy.Spider):
    name = "cafef_spider"
    allowed_domains = ["cafef.vn"]
    start_urls = ["https://cafef.vn"]
    crawl_from = datetime.combine(datetime.now(), time.min)
    print(crawl_from)
    start_crawl_at = datetime.now()

    # Your Elasticsearch credentials
    ELASTICSEARCH_USER = 'elastic'
    ELASTICSEARCH_PASS = 'WgLVWv0vE*Z+Xv8L50Mr'

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse_category)

    def parse_category(self, response):
        categories = response.css('li.acvmenu')
        categories.pop(0)
        url = "https://cafef.vn/%s"
        for category in categories:
            category_url = category.css('li.acvmenu a').attrib['href']
            replaceUrl = url % (category_url)
            # print(replaceUrl)
            yield scrapy.Request(url=replaceUrl, callback=self.parse)

    def parse(self, response):
        news = response.css('div.tlitem')
        category = response.css('h1.zone-title a').attrib['title']

        # Elasticsearch configuration with authentication
        es = Elasticsearch(
            hosts=[{'host': 'localhost', 'port': 9200, 'scheme': 'http'}],
            http_auth=(self.ELASTICSEARCH_USER, self.ELASTICSEARCH_PASS)  # Add authentication credentials
        )
        index_name = "news"

        # Mapping for index
        mapping = {
            "mappings": {
                "properties": {
                    "Category": {"type": "keyword"},
                    "Created": {"type": "date", "format": "dd-MM-yyyy - hh:mm a"},
                    "Link": {"type": "keyword"},
                    "Title": {"type": "text"},
                }
            }
        }

        # Create the index with the mapping (ignore if it already exists)
        es.indices.create(index=index_name, ignore=400, body=mapping)

        for new in news:
            created = datetime.strptime(str(new.css('span.time-ago').attrib['title']), "%Y-%m-%dT%H:%M:%S")
            if created >= self.crawl_from:
                new_item = NewItem()

                new_item['Link'] = "https://cafef.vn" + new.css('div.tlitem h3 a').attrib['href']
                new_item['Title'] = new.css('div.tlitem h3 a::text').get()
                new_item['Category'] = category
                new_item['Created'] = created.strftime("%d-%m-%Y - %I:%M %p")

                yield new_item
                # Save data to Elasticsearch
                self.save_to_elasticsearch(es, index_name, new_item)

    def generate_document_id(self, item):
        # Use the MD5 hash function to generate a unique ID for the document
        unique_id = hashlib.md5(item["Link"].encode()).hexdigest()
        return unique_id

    def save_to_elasticsearch(self, es, index_name, item):
        # Document to be indexed
        doc = {
            "Link": item["Link"],
            "Title": item["Title"],
            "Category": item["Category"],
            "Created": item["Created"]
        }

        # Generate a unique document ID using the MD5 hash function
        doc_id = self.generate_document_id(item)

        # Check if the document with the same ID already exists in the index
        if not es.exists(index=index_name, id=doc_id):
            # Use the 'index' method to index the document with the generated ID
            response = es.index(index=index_name, id=doc_id, body=doc)

            # Check the response for any errors
            if response.get("result") == "created":
                self.logger.info("Document indexed successfully.")
            else:
                self.logger.error("Error indexing the document.")
                self.logger.error(response)

            # Refresh the index (optional, for testing purposes)
            es.indices.refresh(index=index_name)
        else:
            self.logger.info("Document already exists in the index. Skipping indexing.")
