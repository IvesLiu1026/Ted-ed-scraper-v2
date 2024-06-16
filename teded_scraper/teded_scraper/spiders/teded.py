import scrapy

class TedEdSpider(scrapy.Spider):
    name = "teded"
    start_urls = [
        'https://ed.ted.com/lessons',
    ]

    def parse(self, response):
        # Log the initial page response
        self.logger.info("Parsing lesson list page: %s", response.url)
        
        # Extract links to individual lesson pages
        lesson_links = response.css('article a::attr(href)').getall()
        self.logger.info("Found %d lesson links", len(lesson_links))
        
        # Debugging: Print the lesson links
        for link in lesson_links:
            self.logger.info("Lesson link: %s", link)
            yield response.follow(link, self.parse_lesson)
        
        # Pagination
        next_page = response.css('a.pagination__next::attr(href)').get()
        if next_page:
            self.logger.info("Found next page link: %s", next_page)
            yield response.follow(next_page, self.parse)
        else:
            self.logger.info("No more pages found")

    def parse_lesson(self, response):
        title = response.css('h1.lesson-title::text').get()
        transcript = response.css('div.talk-transcript__body p::text').getall()
        questions = []

        for question in response.css('div.question'):
            question_text = question.css('div.question__text::text').get()
            options = question.css('div.answer label::text').getall()
            questions.append({
                'question': question_text,
                'options': options
            })

        # Debugging output
        self.logger.info(f"Title: {title}")
        self.logger.info("Transcript:")
        for paragraph in transcript:
            self.logger.info(paragraph)
        self.logger.info("Questions and Options:")
        for q in questions:
            self.logger.info(f"Question: {q['question']}")
            for option in q['options']:
                self.logger.info(f"Option: {option}")
            self.logger.info("-" * 40)

        yield {
            'title': title,
            'transcript': transcript,
            'questions': questions,
        }
