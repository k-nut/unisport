cd scrapers
#rm $UNISPORT_JSON_PATH/*.json
#$UNISPORT_SCRAPY_COMMAND crawl hu -o $UNISPORT_JSON_PATH/hu.json
#$UNISPORT_SCRAPY_COMMAND crawl tu -o $UNISPORT_JSON_PATH/tu.json
#$UNISPORT_SCRAPY_COMMAND crawl fu -o $UNISPORT_JSON_PATH/fu.json
#$UNISPORT_SCRAPY_COMMAND crawl htw -o $UNISPORT_JSON_PATH/htw.json
#$UNISPORT_SCRAPY_COMMAND crawl beuth -o $UNISPORT_JSON_PATH/beuth.json

python3 mergeSportsclasses.py
cd ..
