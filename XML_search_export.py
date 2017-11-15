#!/usr/bin/env python

"""
This downloads archives records as XML documents based on filtered search results.

"""

import cookielib
import os
import re
import sys
import urllib
import urllib2

ARCHIVES_USERNAME = ''
ARCHIVES_URL = 'https://cavafy.wnyc.org'
SEARCH_URLS = [
    'ENTER SEARCH RESULTS URL HERE',
]

def main(argv):
    xml_dir = argv[-1]
    if not os.path.isdir(xml_dir):
        print(argv)
        print 'Usage: %s <dest dir>' % argv[0]
        return
    password = ARCHIVES_SITE_PASSWORD
    opener = log_in_to_archives(ARCHIVES_USERNAME, password)

    if argv[1] == '--record':
         download_xml_file('%s/assets/%s.xml' % (ARCHIVES_URL, argv[2]), opener, xml_dir)
    else:
        print "Downloading archives records to '%s'" % xml_dir
        download_archives_data(opener, SEARCH_URLS, xml_dir)


def log_in_to_archives(username, password):
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    print "Logging in to archives database."
    resp = opener.open(ARCHIVES_URL + '/login').read()
    token = re.search('type="hidden" value="([^"]+)"', resp).groups()[0]
    login_data = urllib.urlencode({
        'login': username, 'password': password,
        'authenticity_token': token})
    resp = opener.open(ARCHIVES_URL+'/session', login_data).read()
    if 'Logged in as' not in resp:
        raise Exception("Couldn't log in.")
    print "Logged in."
    return opener


def download_archives_data(opener, search_urls, xml_dir):
    for search_url in search_urls:
        for url in search_assets(opener, search_url):
            xml_url = url + '.xml'
            print "Downloading " + xml_url
            download_xml_file(xml_url, opener, xml_dir)


def download_xml_file(xml_url, opener, xml_dir):
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
        asset_urls += re.findall('"(https://[^"]+/assets/[^"]+)"', html)
    return asset_urls


if __name__ == '__main__':
    main(sys.argv)
