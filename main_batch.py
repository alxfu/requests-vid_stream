# WORK IN PROGRESS

import subprocess
from os import path
import browser_cookie3
import requests
import string

alllinks = [
    [
        "Scaling Accessibility Testing",
        "https://video.app-eur.cvent.com/pr53/d720b6a7-36d6-4e27-bbf4-841a6e32dc5f/cb378920-e6fd-4fa7-8a99-ac5767910dcb/333a9c4e-25a1-40d3-b737-9a9b20e52684/converted-videos-1698228714/hls/video_1080_1920_0_3500kbps_00008.ts?Policy=eyJTdGF0ZW1lbnQiOiBbeyJSZXNvdXJjZSI6Imh0dHBzOi8vdmlkZW8uYXBwLWV1ci5jdmVudC5jb20vcHI1My9kNzIwYjZhNy0zNmQ2LTRlMjctYmJmNC04NDFhNmUzMmRjNWYvY2IzNzg5MjAtZTZmZC00ZmE3LThhOTktYWM1NzY3OTEwZGNiLzMzM2E5YzRlLTI1YTEtNDBkMy1iNzM3LTlhOWIyMGU1MjY4NC9jb252ZXJ0ZWQtdmlkZW9zLTE2OTgyMjg3MTQvaGxzLyoiLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE3MDAyMzU0NjV9fX1dfQ__&Signature=ZCdyYQIn1rNWgMQ6fUn8VEWFpo5T0zBC5EqJVpjxKB-cimWBnoVf6Z2h70Wq5RgtkYNghsbZ8IgKr1L7Mdg-geS-aWbSupz40d5MHCzVIkHMeZrF7sUT5Q2IanXLLsgsiZLUlwp8tHi1DHijnoHqoFFXELWjOjCJJEmXHUwRDo26dgM3uRRdcflE47~Oy~niL~E-2gpGX0PFXw~ZV86VNpeZiAaS~PlX9FwyHYxAXJu2uormiWeLbEHZw48B4Jo23unhHePk9LSknG7TIG9YXnXxr~llcItWohmIooay5sBKah9OExSGx0rsFl8NbV3hAe~OfyKoZ955ohHAHLrfEw__&Key-Pair-Id=K2TLR9K095SRQ3",
    ],
    [
        "Unlimited Potential in Automation",
        "https://video.app-eur.cvent.com/pr53/d720b6a7-36d6-4e27-bbf4-841a6e32dc5f/cb378920-e6fd-4fa7-8a99-ac5767910dcb/6ace494f-4bdf-440d-a467-1a8d4cc4bc7b/converted-videos-1698230974/hls/video_1080_1920_0_3500kbps_00005.ts?Policy=eyJTdGF0ZW1lbnQiOiBbeyJSZXNvdXJjZSI6Imh0dHBzOi8vdmlkZW8uYXBwLWV1ci5jdmVudC5jb20vcHI1My9kNzIwYjZhNy0zNmQ2LTRlMjctYmJmNC04NDFhNmUzMmRjNWYvY2IzNzg5MjAtZTZmZC00ZmE3LThhOTktYWM1NzY3OTEwZGNiLzZhY2U0OTRmLTRiZGYtNDQwZC1hNDY3LTFhOGQ0Y2M0YmM3Yi9jb252ZXJ0ZWQtdmlkZW9zLTE2OTgyMzA5NzQvaGxzLyoiLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE3MDAyNTI3MTB9fX1dfQ__&Signature=tmWzOXC-3P90Yke8JQs341SD4FVQGimyzLF4Osja643gJqDEekF0QfMdemzDVhbbbH1CmMku7Dzu-BoMwr~kk2TZ~zoiXor7o-W-WrYj2HzoW1QdAvW63siNpzn6etqyV3qQR6O~1pB6TaYD3GxWratD60RyEd9~jYXSAHkz8ggzlnDfNNubHI6ik5avfTC-WvL1toXuccSNWyP7ljMngO6m-ESwAPcSclTX20RFGysynseUC~UCRK9s2PPhQjXuhX9RTIRAckiqLaWeMatZT0k8ho4xFQmyRaVf98Zt~pQgPAFus1g0dZl-NTAfOEmqYzp5dyH0dWgl2a6UOxzZPQ__&Key-Pair-Id=K2TLR9K095SRQ3"
    ]
]

#  #########
#  constants
#  #########

#  Cookie Jar for requests
CJ = browser_cookie3.firefox()

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

#  initialize URL list
download_links = []


def create_dl_links(given_url):

    #  URL split and shortening
    url_split = given_url.split(".ts")
    size = len(url_split[0])
    url_split[0] = url_split[0][:size - 5]

    #  URL parts (missing the five last digits or element 0)
    first_path = url_split[0]
    second_path = url_split[1]

    #  generate URL list
    for i in range(1, 3000):

        download_links.append(
            first_path + str(f"{i:05}") + ".ts" + second_path)  # enter the number of digits behind the ":"




def get_filename(link: str) -> str:
    #  create a tmp filename from a URL leaving out HTTP, PATH, ending arguments e.g. "?2134452134&ewr5345"
    fragment_removed = link.split("#")[0]  # keep to left of first #
    query_string_removed = fragment_removed.split("?")[0]
    scheme_removed = query_string_removed.split("://")[-1].split(":")[-1]
    if scheme_removed.find("/") == -1:
        return ""
    return path.basename(scheme_removed)




"""
#  DEBUG SECTION
print(links[0])
print(url)
if  links[0] == url:
    print("same")
else:
    print("not the same")
"""

#  download files if HTTP GET OK
def download_files(name):

    for link in download_links:
        r = requests.get(link, headers=HEADERS, cookies=CJ)
        #  print(r.status_code)
        #  print(r.headers)
        if r.status_code == requests.codes.ok:
            filename = get_filename(link)
            open(filename, 'wb').write(r.content)
            print(filename + " - HTTP: " + str(r.status_code) + " - " + name) #  can be made optional is you dont like spam
        else:
            print("NOT OKAY")
            break


def clean_up():
    download_links.clear()
    subprocess.check_output("rm *.ts", shell=True, text=True)
    subprocess.check_output("rm mylist.txt", shell=True, text=True)


for name, url in alllinks:

    #  func1
    create_dl_links(url)

    #  func2
    get_filename(url)

    #  func3
    download_files(name)

    subprocess.check_output("printf 'file '%s'\n' *.ts > mylist.txt", shell=True, text=True)

    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in name if c in valid_chars)
    filename = filename.replace(' ', '_')  # I don't like spaces in filenames
    subprocess.check_output(f"ffmpeg -safe 0 -f concat -i mylist.txt -c copy /media/sf_Vidz_tmp/batch/{filename}.mp4", shell=True, text=True)

    clean_up()
    print("reached end of cleanup")
