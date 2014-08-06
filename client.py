import requests
import md5
import struct

url = "http://localhost:4242/api"

def flatten(req):
  res = ""
  for k, v in sorted(req.items()):
    res += k
    res += v
  return res

def pad_md5(l):
  length = struct.pack('<Q', l * 8)
  padding = '\x80'
  padding += '\x00' * ((64 - len(length) - (l + 1) % 64) % 64)
  padding += length
  print length
  return padding

data = {
    'method': 'vimeo.test.login',
    'api_key': raw_input("api_key: "),
    'api_sig': raw_input("api_sig: "),
}

flattened_req = flatten(data)
flattened_req += pad_md5(len(flattened_req))

# save current info in data
data[flattened_req[0]] = flattened_req[1:]

# craft the packet we want
data['video_id'] = '1337'
data['favorite'] = '1'
data['method'] = 'vimeo.videos.setFavorite'
data['api_sig'] = md5.MD5(data['api_sig']+flatten(data))

print data

r = requests.post(url, data=data)
print r.text
