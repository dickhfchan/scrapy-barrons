import pandas as pd
import sys
import io
from cassandra.cluster import Cluster

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
server = ['54.255.186.233']
cluster = Cluster(server)
session = cluster.connect('scrapy')
server1 = ['54.251.143.131']
cluster1 = Cluster(server1)
session1 = cluster1.connect('scrapy')
data = pd.DataFrame(session1.execute("select * from barrons_list"))
for res in data.index.values:
    row = data.loc[res,data.columns.values].to_dict()
    session.execute("""insert into barrons_list (url,title,date,subtitle)values(%s ,%s ,%s, %s)""",(str(row['url']),str(row['title']),str(row['date']),str(row['subtitle'])))

data1 = pd.DataFrame(session1.execute("select * from barrons"))
for res in data1.index.values:
    row = data1.loc[res,data1.columns.values].to_dict()
    session.execute("""insert into barrons (year,url,title,date,body,tags,company,subtitle,category)values(%s, %s ,%s ,%s, %s, %s ,%s ,%s, %s)""",(str(row['year']),row['url'],row['title'],str(row['date']),str(row['body']),str(row['tags']),str(row['company']),str(row['subtitle']),str(row['category'])))
