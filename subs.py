#!/usr/bin/python
# -*- coding: utf-8 -*-

from googleapiclient.discovery import build
from dataclasses import dataclass
import json
import prettytable as pt
import time
import matplotlib.pyplot as plt
import pandas as pd

### put your google api key in here
api_key = ''
### test pr template
@dataclass
class Vtuber:
	enName: str
	name: str
	gen: str
	ytId: str
	color: str
	subCount: int = 0

# {ytId : [enName,Gen,Color]}
nameIdList = {	'UCp6993wxpyDPHUpavwDFqgg':['Sora','0/E4','#bf8173'],			#0期生
				'UCDqI2jOz0weumE8s7paEk6g':['Roboco','0','#965452'],
				'UC5CwaMl1eIgY8h02uZw7u8A':['Suisei','X','#a0beeb'],			#外部合約生
				'UC-hM6YJuNYVAmUWxeIr9FeA':['Miko','X','#d46875'],
				'UC0TXe_LYZ4scaW2XMyi5_kw':['AZKi','X','#e4508a'],
				'UCD8HOxPs4Xvsm8H0ZxXGiBw':['Meru','1','#dead69'],				#1期生
				'UCdn5BQ06XqgXoAxIhbqw5Rg':['Fubuki','1','#a4e4ff'],
				'UC1CfXB_kRs3C-zaeTG3oGyg':['Haato','1','#ebbc99'],
				'UCQ0UDLQCjY0rmuxCDE38FGg':['Matsuri','1','#856063'],
				'UCFTLzh12_nrtzqBPsTCqenA':['Roze','1','#f7d9b1'],
				'UC1opHUrw8rvnsadT-iGp7Cg':['Aqua','2','#cf97c2'],				#2期生
				'UCXTpFs_3PqI41qX2d9tL2Rw':['Shion','2','#e7cfd5'],
				'UC7fk0CB07ly8oSl0aqKkqFg':['Ayame','2','#fbebee'],
				'UC1suqwovbL1kzsoaZgFZLKg':['Choco','2','#eecba1'],
				'UCvzGlP9oQwU--Y0r9id_jnA':['Subaru','2','#4e3b3e'],
				'UCp-5t9SrOQwXMU7iIjQfARg':['Mio','G','#322e2e'],				#Gamers 實質2.5期
				'UCvaTdHTWBGv3MKj3KVqJVCw':['Okayu','G','#ebd8e8'],
				'UChAnqc_AY5_I3Px5dig3X1Q':['Korone','G','#ab7669'],
				'UC1DCedRgGHBdm81E1llLhOQ':['Pekora','3','#acc0ef'],			#3期生
				'UCl_gCybOJRIgOXw6Qb4qJzQ':['Rushia','3','#d1dac7'],
				'UCdyqAaZDKHXg4Ahi7VENThQ':['Noeru','3','#ddd0d4'],
				'UCvInZx9h3jC2JzsIzoOebWg':['Flare','3','#f8d9a5'],
				'UCCzUftO8KOVkV4wQG1vkUvg':['Marine','3','#a14d61'],
				'UCZlDXzGoo7d44bwdNObFacg':['Kanata','4','#54a5db'],			#4期生
				'UCS9uQI-jC3DE0L4IpXyvr6w':['Coco','4','#d8794e'],
				'UCqm3BQLlJfvkTsX_hvm0UmA':['Watame','4','#efe6d2'],
				'UC1uv2Oq6kNxgATlCiez59hw':['Towa','4','#e8cdde'],
				'UCa9Y57gfeY0Zro_noHRVrnw':['Luna','4','#e4b9d4'],
				'UCFKOVgVbGmX65RxO3EtH3iw':['Lamy','5','#738db6'],				#5期生
				'UCAWSyEs_Io8MtpY3m-zqILA':['Nene','5','#feeab3'],
				'UCUKD-uaobj9jiqB-VXt71mA':['Botan','5','#e3d7d2'],
				'UCK9V2B22uJYu3N7eR_BT9QA':['Polka','5','#ee1517'],
				'UCoSrY_IQQVpmIRZ9Xf-y93g':['Gura','EN','#357498'],				#EN組
				'UCMwGHR0BTZuLsmjY_NT5Pwg':['Ninomae','EN','#50425a'],
				'UCL_qhgtOy0dy1Agp8vkySQg':['Mori','EN','#fccadf'],
				'UCHsx4Hqa-1ORjQTh9TYDhww':['Kiara','EN','#f19269'],
				'UCyl1z3jo3XHR1riLFKG5UAg':['Watson','EN','#ebd8cb'],
#				'UC4YaOt1yT-ZeyB0OmxHgolA':['AI','E4','#de99a5'],				#Elite 4
				'UCQYADFw7xEJ9oZSM5ZbqyBw':['Kaguya','E4','#f0e8e4'],
				'UCMYtONm441rBogWK_xPH9HA':['Mirai','E4','#f4ead8'],
				'UCLhUvJ_wO9hOvv_yYENu4fQ':['Siro','E4','#eae7e9'],
				'UCevD0wKzJFpfIkvHOiQsfLQ':['Hinata','E4','#efc5b9'],
				'UCD-miitqNY3nyukJ4Fnf4_A':['Mito','N','#E43F3B'],				#彩虹社
				'UCwQ9Uv-m8xkE5PzRc7Bqx3Q':['Era','N','#f5a863'],
				'UC_a1ZYZ8ZTXpjg9xUY9sj8w':['Ruru','N','#ebd6ce'],
				'UCZ1xuCK1kNmn5RzPYIZop3w':['Lize','N','#5dbcd2'],
				'UCHVXbQzkl3rDfsXWo8xi2qw':['Ange','N','#c13a4a'],
				'UCoztvTULBYd3WmStqYeoHcA':['Saku','NG','#EF9AAF'],
				'UC0g1AE0DOjBYnLhkgoRWN1w':['Himawari','NG','#d9a207'],
				'UC_4tXjqecqox5Uc05ncxpxg':['Yuika','NG','#eee6e6'],
				# 'UCFv2z4iM5vHrS8bZPq4fHQQ':['HimeHina','In','#f1d4da'],			#其他 爆了 一次最多50筆
				# 'UCy5lOmEQoivK5XK7QCaRKug':['Yumemi','ER','#e0d6d0'],
				# 'UCBePKUYNhoMcjBi-BRmjarQ':['Moe','ER','#6680a5'],
				# 'UC8NZiqKx6fsDT3AVcMiVFyA':['Tamaki','In/NR','#e7e6ec']
			}

tStart = time.time()

youtube = build('youtube', 'v3', developerKey = api_key)
request = youtube.channels().list(
		part= ['snippet','statistics'],
#		forUsername='bittranslate'
		id = list(nameIdList.keys())
)
response = request.execute()

data = {}
data_wo_class = {}

for vtuber in response['items']:
	data[nameIdList[vtuber['id']][0]] = Vtuber(	nameIdList[vtuber['id']][0],
												#list(nameList.keys())[list(nameList.values()).index(vtuber['id'])],
												vtuber['snippet']['title'],
												nameIdList[vtuber['id']][1],
												vtuber['id'],
												nameIdList[vtuber['id']][2],
												vtuber['statistics']['subscriberCount'])
	data_wo_class[nameIdList[vtuber['id']][0]] = {	'enName':nameIdList[vtuber['id']][0],
												#list(nameList.keys())[list(nameList.values()).index(vtuber['id'])],
												'name':vtuber['snippet']['title'],
												'gen':nameIdList[vtuber['id']][1],
												'ytId':vtuber['id'],
												'color':nameIdList[vtuber['id']][2],
												'subCount':int(vtuber['statistics']['subscriberCount'])}

#print(data)

# sorted_data : { id : Vtuber }
sorted_data = {k: v for k, v in sorted(data.items(), key=lambda item : int(item[1].subCount), reverse=True)}

### TABLE_PART_START

table = pt.PrettyTable()
table.field_names = ['No.','YTer','Group','Ch. Name','totalSubs']

i = 0
for key, value in sorted_data.items():
	table.add_row([	'%02d'%(i+1),
					key,
					value.gen,
					value.name,
					value.subCount])
	i += 1


print(table)

### TABLE_PART_END


### BAR_PART_START

# dataFrame = pd.DataFrame(data_wo_class.values())
# dataFrame = dataFrame.sort_values('subCount',ascending= False)

# #print(list([v[2] for k,v in nameIdList.items()]))

# plt.bar(dataFrame['enName'],
# 		dataFrame['subCount'],
# 		color = dataFrame['color'])
# plt.xticks(rotation='vertical')

# plt.show()

### BAR_PART_END

### SYS LOG
tEnd = time.time()

print('It cost %f sec' % (tEnd - tStart))

print('Now time: %s' %(time.strftime("%Y-%m-%d %X",time.localtime())))

