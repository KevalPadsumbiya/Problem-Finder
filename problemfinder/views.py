import os
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from urllib.request import urlopen
import json
import hashlib
import requests
import time
import random

# url details :

# request url format : https://codeforces.com/api/problemset.problems?tags=tag_name&apiKey=key&time=1595263836&apiSig=123456<hash>
# apiSig = any 6 digit integer
# time is current time in unix format
# where <hash> = sha512Hex(123456/problemset.problems?apiKey=key&tags=tag_name&time=1595263836#secret)

# vars to be returned :

# change : if anything is requested(searched) then it will be Treu else False
# tag : it contains value whether user searched by tag or contestID...if by tag than tag=""...
# else tag=tag_name
# url :	it contains url used to request data from codeforces API
# n : apiSig(6 digit positive integer)
# details : contains output data for valid search otherwise it will be empty
# found : True for valid searches else False
# contestId : for searched related to tag contestId="" and for rest searched contestId=contest no

def index(request):

	if request.method=='POST':

		key = os.getenv("Problem_finder_key")		# fetching from environment variables	
		secret = os.getenv("Problem_finder_secret")	# fetching from environment variables

		n = random.randint(100000,999999)
		tag = request.POST['tag'] 
		url = "https://codeforces.com/api/problemset.problems?tags="
		url += tag
		url += "&apiKey="+key+"&time="+str(int(time.time()))+"&apiSig="+str(n)
		print(url)
		prefix=str(n)+"/problemset.problems?apiKey="+key+"&tags="+tag+"&time="
		suffix="#"+secret
		
		hash_url=prefix+str(int(time.time()))+suffix
		hashed_url = hashlib.sha512(hash_url.encode('utf-8')).hexdigest()

		url += hashed_url
		
		res = requests.get(url)
		data = res.json()

		details = []
		details1 = []
		submitbutton = request.POST.get('contest')

		# for search by contest no
		if submitbutton:

			contestId = int(request.POST['contestId'])
			for row in data['result']['problems']:
				sub = []
				if row['contestId'] == contestId:
					if 'rating' in row:
						sub.append(row['index']+" - "+row['name'])
						sub.append(str(row['rating']))
						details.append(sub)
					else:
						sub.append(row['index']+" - "+row['name'])
						sub.append("NA")
						details.append(sub)
					details1.append(str(row['contestId'])+"/"+row['index'])
			
			details.reverse()
			details1.reverse()
			
			found = False
			if len(details)>0:	# if contest id is invalid then len(details)=0
				found = True
			
			main = zip(details, details1)
			
			a={'change':True,'tag':'contest search','url':url,'details':main,'n':n,'found':found,'contestId':contestId}
			return render(request,"index.html",a)	

		# for search by tag
		c = 0	

		for row in data['result']['problems']:
			sub = []
			if 'rating' in row:
				sub.append(row['name'])
				sub.append(str(row['rating']))
				details.append(sub)
			else:
				sub.append(row['name'])
				sub.append("NA")
				details.append(sub)
			details1.append(str(row['contestId'])+"/"+row['index'])
			c+=1;
			# if c>50: # there can be hundreds of problems...but we are just taking first 50 
			# 	break
		
		details.reverse()	# because of we need in ascending alphabatical order(A,B....)
		details1.reverse()
		
		main = zip(details, details1)
		
		a={'change':True,'tag':tag,'url':url,'details':main,'n':n,'found':True,'contestId':""}
		return render(request,"index.html",a)	
	
	a={'change':False,'tag':'all'}
	return render(request,"index.html",a)