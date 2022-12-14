import webget

import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A program that downloads a URL and stores it locally')
    parser.add_argument('url', help='The URL to process')
    parser.add_argument('-d', '--destination', help='The name of the file to store the url in')

    args = parser.parse_args()
    webget.download(args.url, args.destination)
