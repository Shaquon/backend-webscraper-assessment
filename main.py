#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" A simple webscraper. This takes in a file as an arg and parses
out the urls, emails, and phone numbers found in the html. """

__author__ = "Shaquon Kelley"


# Imports go at the top of your file, after the module docstring.
# One module per import line. These are for example only.
from HTMLParser import HTMLParser
import argparse
import re
import requests
import sys


def the_scrape(url):
    """ Takes in a url from args and parses out any URLs,
    email addresses, or phone numbers included ,in the HTML
    """

    req = requests.get(url)
    url_list = parse_urls(req.text)
    email_list = parse_email_addresses(req.text)
    phone_list = parse_phone_numbers(req.text)

    print_list('Emails', email_list)
    print_list('Phone Numbers', phone_list)
    print_list('Urls', url_list)


def print_list(title, data):
    """Print data from collected lists to console"""
    message = '-----------------------------------------------------'\
              '{} Found' \
              '-----------------------------------------------------' \
              '\n'.format(title)
    if data:
        for entry in data:
            message += entry + '\n'
    else:
        message += "none"
    print message + '\n\n'


def parse_phone_numbers(f):
    """ Lists of all phone numbers in a string"""
    phone_match = re.findall(r'(\d{3}[-\.\s]\d{3}[-\.\s]\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]\d{4}|\d{3}[-\.\s]\d{4})', f)
    phone_list = []
    if phone_match:
        for match in phone_match:
            if match not in phone_list:
                phone_list.append(match)
    phone_list = set(phone_list)
    return phone_list


def parse_email_addresses(f):
    """ List of all email addresses from a string"""
    email_match = re.findall(r'[\w.-]+@[\w.-]+.\w+', f)
    email_list = []
    if email_match:
        for match in email_match:
            if match not in email_list:
                email_list.append(match)
    email_list = set(email_list)
    return email_list


def find_tag_urls(f):
    """Parse Html get urls in img and A tags"""
    parser = MyHTMLParser()
    parser.feed(f)
    return parser.url_list


def parse_urls(f):
    """Get a list of all urls found in a string"""
    url_list = find_urls(f)
    url_list += find_tag_urls(f)
    return set(url_list)


def find_urls(f):
    """Gets a list of all urls with https from a string"""
    http_match = re.findall(r'https:\/\/[\w\/?=.-]+', f)
    url_list = []
    if http_match:
        for match in http_match:
            if match not in url_list:
                url_list.append(match)
    return url_list


class MyHTMLParser(HTMLParser):
    """List all urls in an a or image tag"""
    url_list = []

    def handle_starttag(self, tag, attrs):
        if attrs and (tag == 'img' or tag == 'a'):
            self.url_list.append(attrs[0][1])


def create_parser():
    """Creates an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='url to scrape')
    return parser


def main(args):
    """Finds all urls, phone numbers, and email addresses from a given a
     url and returns them to the console"""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)
    the_scrape(parsed_args.url)


if __name__ == "__main__":
    main(sys.argv[1:])
