import scrapy

from scrapy.loader import ItemLoader

from ..items import AlmasrafaeItem
from itemloaders.processors import TakeFirst


class AlmasrafaeSpider(scrapy.Spider):
	name = 'almasrafae'
	start_urls = ['https://www.almasraf.ae/']

	def parse(self, response):
		post_links = response.xpath('//h5/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/a/text()').get()
		description = response.xpath('//div[@class="text"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//ul[@class="info"]/li/text()[normalize-space()]').get()

		item = ItemLoader(item=AlmasrafaeItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
