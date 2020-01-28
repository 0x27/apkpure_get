#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function
from bs4 import BeautifulSoup
import progressbar
import requests
import argparse
import re

### XXX: hack to skip some stupid beautifulsoup warnings that I'll fix when refactoring
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
###

# Set Arguments
about = "This script downloads versioned APKs from APKPure."
parser = argparse.ArgumentParser(description = about)
parser.add_argument("-a", "--app", required=True, type=str)
parser.add_argument("-v", "--version", default=None, type=str)
args = parser.parse_args()
app_name = args.app
app_version = args.version

# Download Latest (Default)
def get_apk(app):
    site = "https://apkpure.com"
    url = "https://apkpure.com/search?q=%s" % app_name 
    html = requests.get(url)
    parse = BeautifulSoup(html.text, "html.parser")
    for i in parse.find("p"):
        a_url = i["href"]
        app_url = site + a_url + "/download?from=details"
        html2 = requests.get(app_url)
        parse2 = BeautifulSoup(html2.text, "html.parser")
        for link in parse2.find_all("a",id="download_link"):
            download_link = link["href"]
        download_apk(app, download_link)

# Download Versioned APK
def get_apk_ver(app):
    site = "https://apkpure.com"
    url = "https://apkpure.com/search?q=%s" % app_name 
    html = requests.get(url)
    parse = BeautifulSoup(html.text, 'html.parser')
    regex = re.compile((format(app_version)))
    for i in parse.find("p"):
        a_url = i["href"]
        app_landing_url = site + a_url
        html2 = requests.get(app_landing_url)
        parse2 = BeautifulSoup(html2.text, 'html.parser')
        download_landing_url = site + parse2.find("a", title=regex)["href"]
        html3 = requests.get(download_landing_url)
        parse3 = BeautifulSoup(html3.text, 'html.parser')
        for link in parse3.find_all("a",id="download_link"):
            download_link = link["href"]
        download_apk(app, download_link)

def make_progress_bar():
    return progressbar.ProgressBar(
        redirect_stdout=True,
        redirect_stderr=True,
        widgets=[
            progressbar.Percentage(),
            progressbar.Bar(),
            ' (',
            progressbar.AdaptiveTransferSpeed(),
            ' ',
            progressbar.ETA(),
            ') ',
        ])

def download_apk(app, download_link):
    if args.version:
        print ("Downloading " + app_name + " v" + app_version)
        output_file = "output/" + app_name + "-" + app_version + ".apk"
    elif args.app:
        print("Downloading " + app_name + "latest")
        output_file = "output/" + app_name + ".apk"
    r = requests.get(url=download_link, stream=True)
    with open(output_file, 'wb') as f:
        total_length = int(r.headers.get('content-length'))
        bar = make_progress_bar()
        bar.start(total_length)
        readsofar = 0
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                readsofar += len(chunk)
                bar.update(readsofar)
                f.write(chunk)
                f.flush()
        bar.finish()
    print("File saved to %s" %(output_file))

if args.version:
    get_apk_ver(app_name)
elif args.app:
    get_apk(app_name)
