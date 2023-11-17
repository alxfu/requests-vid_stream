import subprocess
from os import path
import browser_cookie3
import requests

# URL - paste in "url" line. check quotes!
#  url = "https://video.app-eur.cvent.com/pr53/d720b6a7-36d6-4e27-bbf4-841a6e32dc5f/cb378920-e6fd-4fa7-8a99-ac5767910dcb/eb309209-338e-48e9-a9e0-46045e100582/converted-videos-1696943810/hls/video_1080_1728_0_3500kbps_00008.ts?Policy=eyJTdGF0ZW1lbnQiOiBbeyJSZXNvdXJjZSI6Imh0dHBzOi8vdmlkZW8uYXBwLWV1ci5jdmVudC5jb20vcHI1My9kNzIwYjZhNy0zNmQ2LTRlMjctYmJmNC04NDFhNmUzMmRjNWYvY2IzNzg5MjAtZTZmZC00ZmE3LThhOTktYWM1NzY3OTEwZGNiL2ViMzA5MjA5LTMzOGUtNDhlOS1hOWUwLTQ2MDQ1ZTEwMDU4Mi9jb252ZXJ0ZWQtdmlkZW9zLTE2OTY5NDM4MTAvaGxzLyoiLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE3MDAxNTQzOTV9fX1dfQ__&Signature=bZVQUC-38bhnyQocl9GFq9qOzZACWF2k9oxstNKbXugujrU4~EDRY6RUwVZvIC8r1fib71T4CBa-Wq-LlA8fwOnO8M1KL7Sbjc-TWk4Sdsq9FgQBB5j5Thpu3NUZt0WTItQQIT8aHl3LyzV4juX5SmLVpr957Vt3jlSmitowTKAsfZLA~5FzH34~vnb2IJXEU9kBMskhzYSRfqvsFybaRzPxKXd5paoCae-DKya5otgsGDo1UZ2U2F5xXM7fb4qINmcJvwXJiWUfiwc2s20Z8-2mP5Xyx-CUjSjwcy~Om8xuiT~CPb0a7alUS6cUqQzjuMFOkg0tmyEpYCBlgfNSMw__&Key-Pair-Id=K2TLR9K095SRQ3"
url = input()
# ENABLE ONLY ONE OF THE ABOVE LINES

#  URL modifications
url_split = url.split(".ts")
size = len(url_split[0])
url_split[0] = url_split[0][:size - 5]

#  URL parts (missing the five last digits or element 0)
firstpath = url_split[0]
secondpath = url_split[1]

#  hard-copy of browser's headers
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Accept": "*/*",
    "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Host": "video.app-eur.cvent.com",
    "Origin": "https://web-eur.cvent.com",
    "Referer": "https://web-eur.cvent.com/",
    "Sec-Fetch-Dest": "",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "TE": "trailers",
    #  "Pragma": "no-cache",
    #  "Cache-Control": "no-cache"
}

#  Cookie Jar for requests
cj = browser_cookie3.firefox()

"""
Manual split of URL leaving out (in this case) the five digit counter. e.g. file_00001.ts would be "file_" & ".ts"

ROOM TO SPLIT URL
https://video.app-eur.cvent.com/pr53/d720b6a7-36d6-4e27-bbf4-841a6e32dc5f/cb378920-e6fd-4fa7-8a99-ac5767910dcb/c5c61198-4e41-4417-8021-4b4fb70c55ee/converted-videos-1699895593/hls/master_1080_1920_0_3500kbps_00111
.ts?Policy=eyJTdGF0ZW1lbnQiOiBbeyJSZXNvdXJjZSI6Imh0dHBzOi8vdmlkZW8uYXBwLWV1ci5jdmVudC5jb20vcHI1My9kNzIwYjZhNy0zNmQ2LTRlMjctYmJmNC04NDFhNmUzMmRjNWYvY2IzNzg5MjAtZTZmZC00ZmE3LThhOTktYWM1NzY3OTEwZGNiL2M1YzYxMTk4LTRlNDEtNDQxNy04MDIxLTRiNGZiNzBjNTVlZS9jb252ZXJ0ZWQtdmlkZW9zLTE2OTk4OTU1OTMvaGxzLyoiLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE3MDAwNjI4NzB9fX1dfQ__&Signature=DFlIrSpgFH7kfJJqZSDNPQXZSfp317dkCCD22E0xHYScTjbO65Xg3P4ymXaLxNSasfqmp84YbuAhapWOt6rGrr-SPzspUBfdxNKtVs0hM7P6h~8-VYUPKylHI4RUBDmx7ieLH7PGG024VQgiyxrhDjOjLi6ggBxQLggN2tz-nuXC-urymF5Hhwke-jdFpqcomxd1WVcjqSHdy4NyEonHptoqbZ3Xj6liw2edi2axzuOnzXpkn34MgJunzip9noLmBQl~qpCudSWZDo0w9nhUFWx0jx0uXL8N20g3k0nLZNHUuEg-d25nCwLNqlH7sQyaqGpe~ypCsdTUTWeZPDqFmQ__&Key-Pair-Id=K2TLR9K095SRQ3
ROOM TO SPLIT URL
"""

#  initialize URL list
links = []


def get_filename(myurl: str) -> str:
    #  create a filename from a URL leaving out HTTP, PATH, ending arguments e.g. "?2134452134&ewr5345"
    fragment_removed = myurl.split("#")[0]  # keep to left of first #
    query_string_removed = fragment_removed.split("?")[0]
    scheme_removed = query_string_removed.split("://")[-1].split(":")[-1]
    if scheme_removed.find("/") == -1:
        return ""
    return path.basename(scheme_removed)


#  generate URL list
for i in range(1, 3000):
    # enter the number of digits behind the ":"
    links.append(firstpath + str(f"{i:05}") + ".ts" + secondpath)  # enter the number of digits behind the ":"

"""
DEBUG SECTION

print(links[0])
print(url)
if  links[0] == url:
    print("same")
else:
    print("not the same")
"""

#  download files if HTTP GET OK
for url in links:
    r = requests.get(url, headers=HEADERS, cookies=cj)
    #  print(r.status_code)
    #  print(r.headers)
    if r.status_code == requests.codes.ok:
        filename = get_filename(url)
        open(filename, 'wb').write(r.content)
        print(filename + " - HTTP: " + str(r.status_code)) #  can be made optional is you dont like spam
    else:
        print("NOT OKAY")
        break

#  EXPERIMENTAL:
#  create a list of the *.ts files

#  WINDOWS - not working
#  subprocess.run(['(for %i in (*.ts) do @echo file '%i') > mylist.txt'], stdout=subprocess.PIPE).stdout.decode('utf-8')
#  subprocess.check_output("(for %i in (*.ts) do @echo file '%i') > mylist.txt", shell=True, text=True)

#  OPTIONAL Linux shenanigans
subprocess.check_output("printf 'file '%s'\n' *.ts > mylist.txt", shell=True, text=True)
subprocess.check_output("ffmpeg -safe 0 -f concat -i mylist.txt -c copy output.mp4", shell=True, text=True)
subprocess.check_output("rm *.ts", shell=True, text=True)
subprocess.check_output("rm mylist.txt", shell=True, text=True)
subprocess.check_output("mv output.mp4 /media/sf_Vidz_tmp", shell=True, text=True)
