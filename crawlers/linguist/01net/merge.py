import os
import pandas as pd



root_dir = "./archive_data/"

month_dirs = os.listdir(root_dir)

df_list = list()

for month_dir in month_dirs:
	path = root_dir + month_dir + '/'
	result_name = "result_" + month_dir + ".csv"

	if not os.path.isfile(path + result_name):
		print(result_name + " is not found!")
		continue

	print("merging... %s" % result_name)
	df_list.append(pd.read_csv(path + result_name, sep='|'))

df_all = pd.concat(df_list)

df_all.to_csv('result_all_20180110.csv', sep='|', encoding='utf-8', index=False)

print("Job's done!")
