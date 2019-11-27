import pandas as pd
from cassandra.cluster import Cluster
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
server = ['54.255.186.233']
cluster = Cluster(server)
session = cluster.connect('scrapy')
date = pd.read_csv('/home/ubuntu/scrapy-barrons/barron/barron/articles.csv',sep = '~')
data = []
for res in date.index.values:
        row = date.ix[res,date.columns.values].to_dict()
        cql = 'select * from barrons where year = {} and date = {} and url = {}'.format("'" + str(row['year']) + "'","'" + str(row['date']) + "'","'" + str(row['url']) + "'")
        result = pd.DataFrame(list(session.execute(cql)))
        if len(result):
            pass
        else:
            data.append(row)
            session.execute("""insert into barrons (year,url,title,date,body,tags,company,subtitle,category)values(%s, %s ,%s ,%s, %s, %s ,%s ,%s, %s)""",(str(row['year']),row['url'],row['title'],str(row['date']),str(row['body']),str(row['tags']),str(row['company']),str(row['subtitle']),str(row['category'])))
print(len(data))
files = open('/home/ubuntu/scrapy-barrons/barron/barron/art.log')
results = files.readlines()
datess = results[0]
localdate = datess.strip()[:10]
locatime = datess.strip()[:19]
print(localdate)
print(locatime)
session.execute("insert into manage_new (date,new_source,createtime,download_number) values (%s, %s, %s, %s)" ,(localdate,'barrons',locatime,str(len(data))))
