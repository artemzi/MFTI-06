import scrapy

# run it in scrapy project with
# scrapy crawl deal64 -o deal64.json
# do not forget to add `FEED_EXPORT_ENCODING = 'utf-8'` for russian letters
class QuotesSpider(scrapy.Spider):
    name = "deal64"
    start_urls = [
        'http://deal64.ga/',
        'http://deal64.ga/mobile/',
    ]

    def parse(self, response):
        # follow review
        for href in response.css('ul.ilink a::attr(href)'):
            yield response.follow(href, callback=self.parse_review)

        # follow phones
        for href in response.css('div.products div.entry div.text a::attr(href)'):
            yield response.follow(href, callback=self.parse)

        # follow pagination links
        for href in response.css('div.paging a::attr(href)'):
            yield response.follow(href, callback=self.parse)

    def parse_review(self, response):
        for entry in response.css('div.reviews div.entry div.text'):
            text_list = entry.css('*::text').extract()
            data = [] # текущий элемент, в нем может быть либо отзыв За или Против, оценка, или отзыв без оценки
            for item in text_list:
                if item != ' ': # в блоке с Оценкой избавляемся от пустого элемента
                    data.append(item)
            if len(data) == 2: # здесь будут либо отзывы с оценками (+/-), либо числовой рейтинг.
                if data[0] == 'Оценка:': # если число, сохраним, чтобы использовать там, где нет оценки к отзыву.
                    current_rate = data
                else:
                    yield {
                        data[0]: data[1] # просто пишем в json За/Против: текст отзыва.
                    }
            elif len(data) == 1: # это общий отзыв пользователя, которой он разметил после "Против", без метки оценки
                if int(current_rate[1]) > 3: # добавим оценку на основе числового рейтинга
                    review = 'За:'
                else:
                    review = 'Против:'
                yield {
                    review: data[0] # просто пишем в json За/Против: текст отзыва.
                }
