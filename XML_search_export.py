#!/usr/bin/env python

"""
This downloads archives records as XML documents based on filtered search results.

"""

import cookielib
from getpass import getpass
import os
import re
import sys
import urllib
import urllib2

ARCHIVES_USERNAME = ('ARCHIVES_USERNAME', 'XXXXXXX')
SEARCH_URLS = [
    'ENTER SEARCH RESULTS URL HERE',
]


def main(argv):
    xml_dir = argv[-1]
    if not os.path.isdir(xml_dir):
        print 'Usage: %s <dest dir>' % argv[0]
        return
    password = ('ARCHIVES_SITE_PASSWORD', 'XXXXXXX')
    if password is None:
        password = getpass("Password for %s on cavafy: " % ARCHIVES_USERNAME)
    opener = log_in_to_archives(ARCHIVES_USERNAME, password)
    print "Downloading archives records to '%s'" % xml_dir
    download_archives_data(opener, SEARCH_URLS, xml_dir)


def log_in_to_archives(username, password):
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    print "Logging in to archives database."
    resp = opener.open('http://cavafy.wnyc.net').read()
    print "Logged in."
    return opener


def download_archives_data(opener, search_urls, xml_dir):
    for search_url in search_urls:
        for url in search_assets(opener, search_url):
            xml_url = url + '.xml'
            print "Downloading " + xml_url
            file_name = xml_url.split('/')[-1]
            xml_file = open(os.path.join(xml_dir, file_name), 'w')
            xml = opener.open(xml_url).read()
            xml_file.write(xml)
            xml_file.close()


def search_assets(opener, url):
    asset_urls = []
    page = 1
    while True:
        page_url = url + '&page=%s' % page
        print "Searching " + page_url
        html = opener.open(page_url).read()
        if 'Nothing found' in html:
            break
        page += 1
        asset_urls += re.findall('"(http://[^"]+/assets/[^"]+)"', html)
    return asset_urls


if __name__ == '__main__':
    main(sys.argv)