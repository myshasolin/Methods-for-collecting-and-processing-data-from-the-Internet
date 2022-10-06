from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
import sys
from trainingproject.spiders.hhru import HhruSpider

if __name__ == '__main__':
    search = 'analitik-big-data'
    if len(sys.argv) != 1:
        search = ' '.join(sys.argv[1:])

    configure_logging()
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    runner.crawl(HhruSpider, search=search)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()
