import numpy as np
from tqdm.auto import tqdm
import math
import heapq

def average(rating):
	return np.mean([int(x) for x in rating if x != '0'])

def tani_cos_sim(train, rating, movies):
	tan_sims=[]
	for i in range(len(train)):
		num =0.0
		denom1=0.0
		denom2=0.0
		denom3=0.0
		counter=0
		for x in range(len(rating)):
			if int(train[i][int(rating[x])-1])==0:
				continue
			num+= (int(rating[x])) * (int(train[i][int(movies[x])-1]))
			denom1+=(int(rating[x]))**(2)
			denom2+=int(train[i][int(rating[x])-1])**(2)
			denom3+=(int(rating[x])) * (int(train[i][int(movies[x])-1]))
			counter += 1
		if denom2==0.0 and denom1==0.0 and denom3==0.0 or counter==1:
			tan_sims.append(0)
		else:
			tan_sims.append(((num/(((math.sqrt(denom1))**2)+(math.sqrt(denom2)**2)))-denom3)*(num/(math.sqrt(denom1)*math.sqrt(denom2))))
	return tan_sims

def predict(avg_r,avg_train_r,sims,train,movie):
	num = 0.0
	denom = 0.0
	k_users = heapq.nlargest(50, range(len(sims)), sims.__getitem__)
	for i in range(len(k_users)):
		weight=(float(sims[k_users[i]]))
		if int(train[k_users[i]][int(movie)-1]) ==0:
			continue
		num += (int(train[k_users[i]][int(movie)-1])-avg_train_r[k_users[i]]) * weight
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
			sim_list.append(tani_cos_sim(train,test_r,movies))
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

in_f = ["data\\test5.txt", "data\\test10.txt", "data\\test20.txt"]
out_f = ["data\\result5.txt", "data\\result10.txt", "data\\result20.txt"]
test_num =[5, 10, 20]

for x in range(len(in_f)):
	tester(in_f[x], out_f[x], test_num[x])