import os
import requests
import grequests
import pycookiecheat

"""
# name of the video
name = '123abc'
# .ts URL of the video, replace segment number with {0}
source_url = 'http://example.com/stream/ABC.mp4/seg-%s.ts'
"""

#  if not os.path.exists(name):
#    os.makedirs(name)

keys = []
urls = []

for i in range(5):
    f"{i:05}"
    keys.append(i)
    print(keys)


for x in range(1, 5):
    filename = '{0}/{1:04d}.ts'.format(name, x)
    if os.path.isfile(filename):
        print("skip"), x
        continue

    urls.append(source_url.format(x))
    keys.append(x)

print(urls)
print(keys)

print("hello")
