rm *.json
scrapy crawl hu -o hu.json
scrapy crawl tu -o tu.json
scrapy crawl fu -o fu.json
scrapy crawl htw -o htw.json
scrapy crawl beuth -o beuth.json

python3 mergeSportsclasses.py

rm /home/knut/unisport/everything.db
python3 /home/knut/unisport/python/import.py
