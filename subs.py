#!/usr/bin/python
# -*- coding: utf-8 -*-

from googleapiclient.discovery import build
from dataclasses import dataclass
import json
import prettytable as pt

### put your google api key in here
api_key = ''

@dataclass
class Vtuber:
	enName: str
	name: str
	ytId: str
	subCount: int = 0

nameIdList = {	'UCp6993wxpyDPHUpavwDFqgg':['Sora','0'],						#0期生
				'UCDqI2jOz0weumE8s7paEk6g':['Roboco','0'],
				'UC5CwaMl1eIgY8h02uZw7u8A':['Suisei','X'],						#外部合約生
				'UC-hM6YJuNYVAmUWxeIr9FeA':['Miko','X'],
				'UC0TXe_LYZ4scaW2XMyi5_kw':['AZKi','X'],
				'UCD8HOxPs4Xvsm8H0ZxXGiBw':['Meru','1'],						#1期生
				'UCdn5BQ06XqgXoAxIhbqw5Rg':['Fubuki','1'],
				'UC1CfXB_kRs3C-zaeTG3oGyg':['Haato','1'],
				'UCQ0UDLQCjY0rmuxCDE38FGg':['Matsuri','1'],
				'UCFTLzh12_nrtzqBPsTCqenA':['Roze','1'],
				'UC1opHUrw8rvnsadT-iGp7Cg':['Aqua','2'],						#2期生
				'UCXTpFs_3PqI41qX2d9tL2Rw':['Shion','2'],
				'UC7fk0CB07ly8oSl0aqKkqFg':['Ayame','2'],
				'UC1suqwovbL1kzsoaZgFZLKg':['Choco','2'],
				'UCvzGlP9oQwU--Y0r9id_jnA':['Subaru','2'],
				'UCp-5t9SrOQwXMU7iIjQfARg':['Mio','G'],							#Gamers 實質2.5期
				'UCvaTdHTWBGv3MKj3KVqJVCw':['Okayu','G'],
				'UChAnqc_AY5_I3Px5dig3X1Q':['Korone','G'],
				'UC1DCedRgGHBdm81E1llLhOQ':['Pekora','3'],						#3期生
				'UCl_gCybOJRIgOXw6Qb4qJzQ':['Rushia','3'],
				'UCdyqAaZDKHXg4Ahi7VENThQ':['Noeru','3'],
				'UCvInZx9h3jC2JzsIzoOebWg':['Flare','3'],
				'UCCzUftO8KOVkV4wQG1vkUvg':['Marine','3'],
				'UCZlDXzGoo7d44bwdNObFacg':['Kanata','4'],						#4期生
				'UCS9uQI-jC3DE0L4IpXyvr6w':['Coco','4'],
				'UCqm3BQLlJfvkTsX_hvm0UmA':['Watame','4'],
				'UC1uv2Oq6kNxgATlCiez59hw':['Towa','4'],
				'UCa9Y57gfeY0Zro_noHRVrnw':['Luna','4'],
				'UCFKOVgVbGmX65RxO3EtH3iw':['Lamy','5'],						#5期生
				'UCAWSyEs_Io8MtpY3m-zqILA':['Nene','5'],
				'UCUKD-uaobj9jiqB-VXt71mA':['Botan','5'],
				'UCK9V2B22uJYu3N7eR_BT9QA':['Polka','5'],
				'UCoSrY_IQQVpmIRZ9Xf-y93g':['Gura','EN'],						#EN組
				'UCMwGHR0BTZuLsmjY_NT5Pwg':['Ninomae','EN'],
				'UCL_qhgtOy0dy1Agp8vkySQg':['Mori','EN'],
				'UCHsx4Hqa-1ORjQTh9TYDhww':['Kiara','EN'],
				'UCyl1z3jo3XHR1riLFKG5UAg':['Watson','EN'],
				'UC4YaOt1yT-ZeyB0OmxHgolA':['AI','E4'],							#Elite 4
				'UCQYADFw7xEJ9oZSM5ZbqyBw':['Kaguya','E4'],
				'UCMYtONm441rBogWK_xPH9HA':['Mirai','E4'],
				'UCLhUvJ_wO9hOvv_yYENu4fQ':['Siro','E4']
			}

youtube = build('youtube', 'v3', developerKey = api_key)
request = youtube.channels().list(
		part= ['snippet','statistics'],
#		forUsername='bittranslate'
		id = list(nameIdList.keys())
)
response = request.execute()

data = {}

for vtuber in response['items']:
	data[nameIdList[vtuber['id']][0]] = Vtuber(	nameIdList[vtuber['id']][0],
												#list(nameList.keys())[list(nameList.values()).index(vtuber['id'])],
												vtuber['snippet']['title'],
												vtuber['id'],
												vtuber['statistics']['subscriberCount'])

#print(data)

sorted_data = {k: v for k, v in sorted(data.items(), key=lambda item : int(item[1].subCount), reverse=True)}
### sorted_data : { id : Vtuber }

table = pt.PrettyTable()
table.field_names = ['No.','YTer','Gen','Ch. Name','totalSubs']

i = 0
for key, value in sorted_data.items():
	table.add_row([	'%02d'%(i+1),
					key,
					nameIdList[value.ytId][1],
					value.name,
					value.subCount])
	i += 1

print(table)
