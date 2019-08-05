## How to run barrons crawler?
```sh
cd scrapy_barrons/barron/barron/
# Get url, title, date for each article to generate output.csv file
scrapy crawl barronlist
# Get url, title, date, body, company, etc. of each article to generate articles.csv file
scrapy crawl barronfetch
```

## How to run barrons spider under crontab?
```sh
# run barronlist at 00:05:00
05 0 * * * cd /home/ubuntu/scrapy_barrons/barron/barron/ && scrapy crawl barronlist > /home/ubuntu/scrapy_barrons/barron/barron/out.log 2>&1 &
# run barronfetch at 00:10:00
10 0 * * * cd /home/ubuntu/scrapy_barrons/barron/barron/ && scrapy crawl barronfetch > /home/ubuntu/scrapy_barrons/barron/barron/art.log 2>&1 &
# Save the output.csv file into the barron_link table
15 0 * * * python3 /home/ubuntu/scrapy_barrons/rw_barron/rw_out.py > /home/ubuntu/rw_reuter/out.log 2>&1 &
# Save the articles.csv file into the barron table
20 0 * * * python3 /home/ubuntu/scrapy_barrons/rw_barron/rw_art.py > /home/ubuntu/rw_reuter/art.log 2>&1 &
```
