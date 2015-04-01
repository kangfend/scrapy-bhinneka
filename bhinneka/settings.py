# -*- coding: utf-8 -*-

# Scrapy settings for bhinneka project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'bhinneka'

SPIDER_MODULES = ['bhinneka.spiders']
NEWSPIDER_MODULE = 'bhinneka.spiders'
BASE_URL = 'http://www.bhinneka.com'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'bhinneka (+http://www.yourdomain.com)'
