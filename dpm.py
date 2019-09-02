import numpy as np
import math
#import matplotlib.pyplot as plt
#np.set_printoptions(precision=10)

#データの選択
temp=12
samp=22
sam=0.0
count=0

#テンプレート読み込み
for i in range(100):
	number01=i+1
	data01=np.loadtxt("./city0{0}/city0{0}_{1:03d}.txt".format(temp,number01),skiprows=3)
	frame01=data01.shape[0]
	dim01=data01.shape[1]
	#print(data01[0,0])
	
	if i==0:
		print("calculate_start")

#未知入力データ読み込み	
	for s in range(100):
		number02=s+1
		data02=np.loadtxt("./city0{0}/city0{0}_{1:03d}.txt".format(samp,number02),skiprows=3)
		frame02=data02.shape[0]
		dim02=data02.shape[1]
		#print("A{0} frame:{1} dimention:{2}".format(number01,frame01,dim01))
		#print("B{0} frame:{1} dimention:{2}".format(number02,frame02,dim02))
		#print(data02[0,0])
		podist0=np.arange(frame01*frame02).reshape(frame01,frame02)
		podist=podist0.astype(np.float16)
		grid=podist0.astype(np.float16)
		grid[0:,0:]=0.00
		#print("podist=",podist[0:3,0:3])
		
		
		
#局所距離計算
		for a in range(frame01):
			for b in range(frame02):
				sam=0.0
				for  dim in range(15):
					sam+=(data01[a,dim]-data02[b,dim])**2
				podist[a,b]=math.sqrt(sam)
				#print("podistres=",podist[a,b])

#格子点計算		
		grid[0,0]=podist[0,0]
		for a in range(frame01):
			grid[a,0]=grid[a-1,0]+podist[a,0]
		
		for b in range(frame02):
			grid[0,b]=grid[0,b-1]+podist[0,b]
		#print("grid=",grid[0:3,0:3])

#最小値計算		
		for a in range(1,frame01):
			for b in range(1,frame02):
				min=grid[a,b-1]+podist[a,b]
				if min>grid[a-1,b-1]+2.0*podist[a,b]:
					min=grid[a-1,b-1]+2.0*podist[a,b]
				if min>grid[a-1,b]+podist[a,b]:
					min=grid[a-1,b]+podist[a,b]
				grid[a,b]=min
		#print("mingrid=",grid[0:3,0:3])
	
#単語間距離計算		
		wdist=grid[frame01-1,frame02-1]/(frame01+frame02)
		
#最も単語間距離が短いデータの保存		
		if s==0:
			save_w=wdist
			save_n=s
		if save_w>wdist:
			save_w=wdist
			save_n=s
		
#認識率計算
	if save_n==i:
		count+=1
		print("data{0}:o".format(i+1))
		print("単語間最短距離＝",round(save_w,4))
	else:
		print("data{0}:x".format(i+1))
		print("単語間最短距離＝",round(save_w,4))
	if (i+1)%10==0 or (i+1)%100==0:
		print("calculated{0}%".format(i+1))

print("認識率={0}%".format(count))
