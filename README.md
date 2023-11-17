# requests-vid_stream
A small script to save *.ts files from streaming players if you know the/one URL(s) and the URLs are counting up
and creates an MP4 file out of them via ffmpeg


## disclaimer
You are solely responsible if you use/modify this script to make illegal copies of videos! 


## dependencies
### system
- Mozilla Firefox - for its cookies (Chrome/etc. also work but need a small code change)
- FFMPEG - also needs to be in PATH (Windows)
Windows see: https://www.wikihow.com/Install-FFmpeg-on-Windows
Linux/Ubuntu: Install via software manager or apt-get install
### python
- browser_cookie3 (if your env does not install, use "pip install browser_cookie3)
- requests


## Usage:
- clone repo
- install dependencies on your pc and in your venv

- paste a video URL into the "url" at the beginning of the script
the script will split the URL at ".ts", substract 5 characters from the first part

- run script
-    it will abort ("break") loop when HTTP GET 200 changes to e.g. HTTP GET 404 
-    it will try to make one video file out of all the *.ts files

### optional
- set counter digits (default is 5)
- set counter range (default is 3000)
- enable/edit/disable file shenanigans


