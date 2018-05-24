#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function
from bs4 import BeautifulSoup
import progressbar
import requests
import sys
### XXX: hack to skip some stupid beautifulsoup warnings that I'll fix when refactoring
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

def get_apk(app_name): # XXX: this function needs refactoring/cleaning.
    print("{+} getting download link for %s" %(app_name))
    site = "https://apkpure.com"
    url = "https://apkpure.com/search?q=%s" %(app_name)
    html = requests.get(url)
    parse = BeautifulSoup(html.text)
    for i in parse.find("p"):
        a_url = i["href"]
        app_url = site + a_url + "/download?from=details"
        html2 = requests.get(app_url)
        parse2 = BeautifulSoup(html2.text)
        for link in parse2.find_all("a",id="download_link"):
            download_link = link["href"]
        download_apk(app_name, download_link)

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

def download_apk(app_name, download_link):
    print("{+} downloading %s" %(app_name))
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
    print("{+} done. file saved to %s" %(output_file))

def main(args):
    if len(args) != 2:
        sys.exit("use: %s com.blah.blah" %(args[0]))
    get_apk(args[1])

if __name__ == "__main__":
    main(args=sys.argv)
