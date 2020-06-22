import numpy as np
from tqdm.auto import tqdm
import math
import heapq
import warnings


def average(rating):
	return np.mean([int(x) for x in rating if x != '0'])

def cos_sim(train, rating,movies, avg_train_r,avg_r):
	sims=[]
	for i in range(len(rating)):
		num =0.0
		denom1=0.0
		denom2=0.0
		counter=0
		for x in range(len(rating)):
			if int(train[i][int(rating[x])-1])==0:
				continue
			num+= (int(rating[x])- avg_r) * (int(train[int(movies[x])-1][i])- avg_train_r[i])
			denom1+=(int(rating[x])- avg_r)**(2)
			denom2+=(int(train[i][int(rating[x])-1])-avg_train_r[i])**(2)
			counter += 1
		if denom2==0.0 or denom1==0.0 or counter==1:
			sims.append(0)
		else:
			sims.append(num/(math.sqrt(denom1)*math.sqrt(denom2)))
	return sims

def predict(avg_r,avg_train_r,sims,train,movie):
	num = 0.0
	denom = 0.0
	k_items = heapq.nlargest(50, range(len(sims)), sims.__getitem__)
	for i in range(len(k_items)):
		weight=(float(sims[k_items[i]]))
		if int(train[int(movie)-1][k_items[i]]) ==0:
			continue
		num += (int(train[int(movie)-1][k_items[i]])-avg_train_r[k_items[i]]) * weight
		denom += weight
	if denom == 0.0:
		p = avg_r  
	else:
		p = avg_r + (num/denom)
	if p > 5:
		p = 5  
	elif p < 1:
		p = 1
	return p
	

def tester(input, output, test_num):
	file = open("data\\train.txt","r")
	train = [line . split('\t') for line in file]
	file.close()
	file = open('%s' % input,"r")
	test = [line.split(" ") for line in file]
	file.close()
	train=list(map(list, zip(*train)))
	test_r = []
	avg_test_r = []
	train_r = []
	avg_train_r = [average(x) for x in train]
	test_num = test_num
	sim_list=[]
	movies =[]
	avg_count = 0
	rated_movies = []
	results=[]
	user=0

	for x in range(len(test)):
		counter = 0
		if int(test[x][2])!= 0:
			test_r.append(int(test[x][2]))
			counter+=1
		if len(test_r)==test_num:
			avg_test_r.append(average(test_r))
			test_r.clear()
			counter=0
	for x in range(len(test)):
		counter=0
		if int(test[x][2]) != 0:
			test_r.append(int(test[x][2]))
			movies.append(int(test[x][1]))
			counter+=1
		if len(test_r)==test_num:
			sim_list.append(cos_sim(train,test_r,movies,avg_train_r,avg_test_r[avg_count]))
			test_r.clear()
			counter=0
			avg_count+=1

	for x in tqdm(range(len(test))):
		if int(test[x][2]) !=0:
			if len(rated_movies) == test_num:
				rated_movies.clear()
				user+=1
			rated_movies.append(int(test[x][1]))
		elif int(test[x][2]) ==0:
			p = predict(avg_test_r[user],avg_train_r,sim_list[user],train,int(test[x][1]))
			p = int(round(p))
			test[x][2] = str(p)+ '\n'
			results.append(test[x][0] + ' ' + test[x][1] + ' ' + test[x][2])

	with open('%s' % output, 'w+') as f:
		for i in range(len(results)):
			f.writelines(results[i])

warnings.filterwarnings('ignore')
in_f = ["data\\test5.txt", "data\\test10.txt", "data\\test20.txt"]
out_f = ["data\\result5.txt", "data\\result10.txt", "data\\result20.txt"]
test_num =[5, 10, 20]

for x in range(len(in_f)):
	tester(in_f[x], out_f[x], test_num[x])