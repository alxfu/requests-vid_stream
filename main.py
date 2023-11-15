from os import path
import requests
#  TBD import grequests
import browser_cookie3

#  hard-copy of browser's headers
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Accept": "*/*",
    "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Host": "video.app-eur.cvent.com",
    "Origin": "https://web-eur.cvent.com",
    "Referer": "https://web-eur.cvent.com/",
    "DNT": "1",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache"
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
firstpath = "https://video.app-eur.cvent.com/pr53/d720b6a7-36d6-4e27-bbf4-841a6e32dc5f/cb378920-e6fd-4fa7-8a99-ac5767910dcb/c5c61198-4e41-4417-8021-4b4fb70c55ee/converted-videos-1699895593/hls/master_1080_1920_0_3500kbps_"  # isssing 5 digits
secondpath = ".ts?Policy=eyJTdGF0ZW1lbnQiOiBbeyJSZXNvdXJjZSI6Imh0dHBzOi8vdmlkZW8uYXBwLWV1ci5jdmVudC5jb20vcHI1My9kNzIwYjZhNy0zNmQ2LTRlMjctYmJmNC04NDFhNmUzMmRjNWYvY2IzNzg5MjAtZTZmZC00ZmE3LThhOTktYWM1NzY3OTEwZGNiL2M1YzYxMTk4LTRlNDEtNDQxNy04MDIxLTRiNGZiNzBjNTVlZS9jb252ZXJ0ZWQtdmlkZW9zLTE2OTk4OTU1OTMvaGxzLyoiLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE3MDAwNjI4NzB9fX1dfQ__&Signature=DFlIrSpgFH7kfJJqZSDNPQXZSfp317dkCCD22E0xHYScTjbO65Xg3P4ymXaLxNSasfqmp84YbuAhapWOt6rGrr-SPzspUBfdxNKtVs0hM7P6h~8-VYUPKylHI4RUBDmx7ieLH7PGG024VQgiyxrhDjOjLi6ggBxQLggN2tz-nuXC-urymF5Hhwke-jdFpqcomxd1WVcjqSHdy4NyEonHptoqbZ3Xj6liw2edi2axzuOnzXpkn34MgJunzip9noLmBQl~qpCudSWZDo0w9nhUFWx0jx0uXL8N20g3k0nLZNHUuEg-d25nCwLNqlH7sQyaqGpe~ypCsdTUTWeZPDqFmQ__&Key-Pair-Id=K2TLR9K095SRQ3"

#  URL list
links = []


def get_filename(url):
    #  create a filename from a URL leaving out HTTP, PATH, ending arguments e.g. "?2134452134&ewr5345"
    fragment_removed = url.split("#")[0]  # keep to left of first #
    query_string_removed = fragment_removed.split("?")[0]
    scheme_removed = query_string_removed.split("://")[-1].split(":")[-1]
    if scheme_removed.find("/") == -1:
        return ""
    return path.basename(scheme_removed)


#  generate URL list
for i in range(1, 3000):
    # enter the number of digits behind the ":"
    links.append(firstpath + str(f"{i:05}") + secondpath)  # enter the number of digits behind the ":"
    print(firstpath + str(f"{i:05}") + secondpath)

#  download files if HTTP GET OK
for url in links:
    r = requests.get(url, headers=HEADERS, cookies=cj)
    print(r.status_code)
    if r.status_code == requests.codes.ok:
        filename = get_filename(url)
        open(filename, 'wb').write(r.content)
    else:
        print("NOT OKAY")
