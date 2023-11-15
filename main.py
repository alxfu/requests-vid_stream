""" download segmented mpeg video (.ts files) from streaming websites """
import sys
import os
import requests

M3URL = "https://video.app-eur.cvent.com/pr53/d720b6a7-36d6-4e27-bbf4-841a6e32dc5f/cb378920-e6fd-4fa7-8a99-ac5767910dcb/d547fcf2-9240-4d5d-a632-694b56571262/converted-videos-1699954733/hls/master_1080_1920_0_3500kbps.m3u8?Policy=eyJTdGF0ZW1lbnQiOiBbeyJSZXNvdXJjZSI6Imh0dHBzOi8vdmlkZW8uYXBwLWV1ci5jdmVudC5jb20vcHI1My9kNzIwYjZhNy0zNmQ2LTRlMjctYmJmNC04NDFhNmUzMmRjNWYvY2IzNzg5MjAtZTZmZC00ZmE3LThhOTktYWM1NzY3OTEwZGNiL2Q1NDdmY2YyLTkyNDAtNGQ1ZC1hNjMyLTY5NGI1NjU3MTI2Mi9jb252ZXJ0ZWQtdmlkZW9zLTE2OTk5NTQ3MzMvaGxzLyoiLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE2OTk5OTQ3Nzh9fX1dfQ__&Signature=JAa-sJl7u9r6nJUqAfhp-x8tA9ksSmU6vzcNG8MDfeojRqLvXV6wVXeADh9zjXsL44dsFP-oTJI1n4Hh-7kOX9MUVLyqaa2SGJIf9K5R8ITQlE2GZ02TigPz2C4orfsorYtgynXCe0UypbXmdbB~96bqAXiBAEDxR3mXLLOkA0yEEiI1cTPbIzKGtOpzjGaxb5tNsaFEtqw3kr2vUxDQ86rbvTHGKnEg1hZk5IPQfdNz7t-Fs1nH3XYdyCv-pRXa110x3dbFp0PwMlF55uyZ5iu6XzUiIIFcZftLjCCnuF4QvVCRXxAG2yvE-yaigN8mDQEoDOATjLqsSotWDYawOA__&Key-Pair-Id=K2TLR9K095SRQ3"  # fill in: .m3u8 file url
SEG1URL = "https://video.app-eur.cvent.com/pr53/d720b6a7-36d6-4e27-bbf4-841a6e32dc5f/cb378920-e6fd-4fa7-8a99-ac5767910dcb/d547fcf2-9240-4d5d-a632-694b56571262/converted-videos-1699954733/hls/master_1080_1920_0_3500kbps_00001.ts?Policy=eyJTdGF0ZW1lbnQiOiBbeyJSZXNvdXJjZSI6Imh0dHBzOi8vdmlkZW8uYXBwLWV1ci5jdmVudC5jb20vcHI1My9kNzIwYjZhNy0zNmQ2LTRlMjctYmJmNC04NDFhNmUzMmRjNWYvY2IzNzg5MjAtZTZmZC00ZmE3LThhOTktYWM1NzY3OTEwZGNiL2Q1NDdmY2YyLTkyNDAtNGQ1ZC1hNjMyLTY5NGI1NjU3MTI2Mi9jb252ZXJ0ZWQtdmlkZW9zLTE2OTk5NTQ3MzMvaGxzLyoiLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE2OTk5OTQ3OTh9fX1dfQ__&Signature=ttXnXe9ptPPpU1-cyUDJB9Ntw1hDJGFy4-ycpK~4h3zkziz~NB9RRyqhhgCMjNH-RMjYESvKqkYhFQB83qwtoM5G63KFHTciGzsjtvdSooGbc9GDZeksxpCmS3dnb9I3bEWUjr8WLm9PbIVhrdvr6qCjM2HJaQdANgoCKUgY186LyEwvENq03u9noj3K~808Uh5dTml7XGzhwJ0G4n9aEYQA39b3-zjksKgFsOXrimteqYsTo7xOqslnCRHpI7y~LIdsOVgARziRHYV-d46-N4EPnM1rDWISbTGk6IFZTyTkAb3bD6kWwV2q-R3CBXs1N-EzxoWshRJiXn26TrtbqQ__&Key-Pair-Id=K2TLR9K095SRQ3"  # fill in: first ts segment file url
REFERER = "https://web-eur.cvent.com/"  # fill in: some websites require a specific referer website to allow the request

OUTNAME = 'video.ts'  # default output file name
LOC = ""  # default save location

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Accept": "*/*",
    "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": REFERER,
    "DNT": "1",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache"
}


def getSegsNum(m3):
    """ figure out how many segments there are using the m3u8 file """
    lines = m3.text.split('\n')
    nsegs = 0
    for line in lines:
        if 'seg-' in line and '.ts' in line:
            tokens = line.split('-')
            idx = 0
            for i, tok in enumerate(tokens):
                if 'seg' == tok[-3:]:
                    idx = i + 1
                    break
            nsegs = int(tokens[idx])
    return nsegs


def dumpSegs(initUrl, n, path, append=False):
    """ downlaod and combine the .ts files
    given the first seg's url, the number of segments and
    the destination download path """
    with open(path, 'ab' if append else 'wb') as f:
        for i in range(1, n + 1):
            segurl = initUrl.replace('seg-1-', 'seg-{:d}-'.format(i))
            success = False
            while not success:
                try:
                    seg = requests.get(segurl, headers=HEADERS)
                    success = True
                except:
                    print('retrying...')
            f.write(seg.content)
            print(('dumped seg%d.ts' % i) + '  %d%%' % (i * 100 / n))


if __name__ == "__main__":
    DEST = LOC + OUTNAME
    if len(sys.argv) > 1:
        DEST = sys.argv[1]
    # validate destination:
    delim = ''
    if '\\' in DEST:
        delim = '\\'
    elif '/' in DEST:
        delim = '/'
    if delim:
        PATH = ''.join(DEST.split(delim)[:-1])
        if not os.path.isdir(PATH):
            print('INAVLID DESTINATION.')
            sys.exit(0)
    m3u8 = requests.get(M3URL, headers=HEADERS)
    nsegs = getSegsNum(m3u8)
    dumpSegs(SEG1URL, nsegs, DEST)