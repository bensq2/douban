pip install scrapy
新建项目
scrapy startproject douban
新建爬虫
scrapy genspider douban_spider mouvie.douban.com

运行scrapy:
scrapy crawl douban_spider




导出：
scrapy crawl douban_spider　-o abc.json
scrapy crawl douban_spider　-o abc.csv



# 双向爬取
scrapy genspider -t crawl easy web



scrapy genspider instagram https://www.instagram.com/explore/tags/pishposh/?__a=1