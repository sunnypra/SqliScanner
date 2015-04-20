#!/bin/bash
#python sqli_appfinal4.py
#python step3.py
#python phase4.py
scrapy crawl sqli44 > dump
scrapy crawl step3 -s LOG_ENABLED=0
