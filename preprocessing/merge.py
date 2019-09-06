# 将所有的轨迹记录合并，并按照用户ID进行分组
import pandas as pd

data_merge = pd.DataFrame()

for i in range(1,13):
	#文件名
	if i < 10:
		file_name = 'DataTech_Public_Trace_0' + str(i)
	else:
		file_name = 'DataTech_Public_Trace_' + str(i)
	#读入文件
	data = pd.read_table(file_name,sep='|',names=['USER_ID','START_TIME','LONGITUDE','LATITUDE','date'])
	#数据合并
	data_merge = pd.concat([data_merge,data])
	print('the {}th dataset joined......'.format(i))


#以ID为基准进行分组
grouped = data_merge.groupby('USER_ID')
#储存每个ID对应的所有记录
for name,group in grouped:
	group = group.sort_values(by = ['START_TIME'])
	group.to_csv('cleaned_data/{}.csv'.format(name),index = False)
	print('User ID:{} completed......'.format(name))

print('Finished!!!')

