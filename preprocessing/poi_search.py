import requests

akeys = 'joLVEFit1SFGg6g1cgHzDZ1Dr9Up9D9H'
url = 'http://api.map.baidu.com/place/v2/search?query=医院&location=29.863626306675116,121.6157937789176&radius=1000&output=json&ak='+ akeys

r = requests.get(url)

response_dict = r.json()



result_trans = response_dict['results']

ans = []
for bank in result_trans:
	ans.append(bank['name'])

print(ans)
print(len(result_trans))
