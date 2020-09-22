import json
import hashlib
import requests
import time

print(int(time.time()))

key = os.getenv("Problem_finder_key")		# fetching from environment variables	
secret = os.getenv("Problem_finder_secret")	# fetching from environment variables

main="https://codeforces.com/api/problemset.problems?tags=math&apiKey="+key+"&time="+str(int(time.time()))+"&apiSig=123456"

prefix="123456/problemset.problems?apiKey="+key+"&tags=math&time="
suffix="#"+secret

hash_url=prefix+str(int(time.time()))+suffix

hash=hashlib.sha512(hash_url.encode('utf-8')).hexdigest()

main += hash

resp = requests.get(main)
data = resp.json()
print(data)

