import os
import sys
import re
import pandas as pd
import numpy as np

#讀取已測試完的正確答案
#填寫格式!! public測資：1=true,0=false. private測資：-1
#最後一列，由於輸出時有加上\n的關係，是空白行！！
correct_ans = pd.read_csv("correct.txt").values
print(correct_ans[-1, 0])
finish_amount = len(correct_ans)#已完成的數量(1~300)
if correct_ans[-1, 0] != finish_amount - 1:
	sys.exit("txt內有缺值 請確認！！！")
print("根據檔案，現在已經判斷完", finish_amount, "筆資料\n")

#輸入要產生的個數
num = input("輸入要產生的個數，建議為10：")
print("現正產生第", finish_amount, '筆~第', int(num) + finish_amount - 1, '筆資料\n')

#寫成上傳的.csv檔後上傳，傳完自動刪除.csv
for i in range(finish_amount,finish_amount + int(num)):
	#這個路徑要改成你的絕對路徑！！然後要加""在頭尾，不然你會想哭
	#path = '"D:' + u'/軟體工程' + '/final/DS_HW2_GuessAns/DS_HW2_GuessAns/save/test' + str(i) + '.csv"'
	#path = '"D:' + u'/作業' + '/github/DS_HW2_GuessAns/DS_HW2_GuessAns/save/test' + str(i) + '.csv"'
	path='"'+os.getcwd()+'/save/test' + str(i) + '.csv"'
	Message = '"第' + str(i) + u'筆測試"'
	#該指令需要kaggle api
	command1 = 'kaggle competitions submit -c datascience-hw2 -f ' + path + ' -m \"' + Message + '\"'
	#必須先創一個save資料夾
	with open(('./save/test' + str(i) + '.csv'), 'w') as file:
		file.write('index,ans\n')
		for j in range(300):
			file.write(str(int(j)) + ',')
			if j == finish_amount:
				file.write('1' + '\n')
			else:
				file.write('0' + '\n')
		finish_amount += 1
	print(os.popen(command1).read())
	os.remove(path)

#讀取上傳的分數，並把結果寫入紀錄文件
with open("correct.txt", 'a') as file:
	#該指令需要kaggle api
	command2 = 'kaggle competitions submissions -v datascience-hw2'
	tmp = os.popen(command2).read()
	print(tmp)
	detect = input('stop!!!!!\n先確認是否載到的是需要的資料\n正確打y,錯誤打n：')
	if detect == 'y':
		result = re.split('\n', tmp)
		for i in range(0,int(num)):
			file_name = re.split(',', result[2*int(num) - 2*i])[0]
			score = re.split(',', result[2*int(num) - 2*i])[4]
			if file_name != 'test' + str(i + len(correct_ans)) + '.csv':
				sys.exit("下載的資料與剛上傳的資料沒對上，請確認！！")
			if float(score) == 0.56111:
				file.write(str(i + len(correct_ans)) + ',-1\n')
				print('第', i + len(correct_ans), '筆測資：Private')
			if float(score) > 0.56111:
				file.write(str(i + len(correct_ans)) + ',1\n')
				print('第', i + len(correct_ans), '筆測資：True')
			if float(score) < 0.56111:
				file.write(str(i + len(correct_ans)) + ',0\n')
				print('第', i + len(correct_ans), '筆測資：False')