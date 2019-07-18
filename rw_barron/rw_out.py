import pandas as pd
from cassandra.cluster import Cluster
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
server = ['52.76.70.227']
cluster = Cluster(server)
session = cluster.connect('scrapy')
date = pd.read_csv('/home/ubuntu/barron/barron/output.csv',sep = '~')
data = []
for res in date.index.values:
    row = date.ix[res,date.columns.values].to_dict()
    data.append(row)
    session.execute("""insert into barrons_list (url,title,date,subtitle)values(%s ,%s ,%s, %s)""",(str(row['url']),str(row['title']),str(row['date']),str(row['subtitle'])))
print('output file data',len(data))
