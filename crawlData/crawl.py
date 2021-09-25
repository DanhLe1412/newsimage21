from hufftingtonpost import HuffPost
from ksta import startDownloadAllImages

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description="Process scrape news data")
    ArgHuffpost = parser.add_argument_group("HuffPost")
    ArgKsta = parser.add_argument_group("KSTA")
    
    ArgHuffpost.add_argument("--huffpost", type=int, default=0, help="1 activate download. otherwise, choose 0 will not download")
    ArgHuffpost.add_argument("--sizeh", default=5000, type=int, help='Amount news will download from hufftingtonpost.com [Must be in range 0-200853]')

    ArgKsta.add_argument("--ksta", type=int, default=0, help="1 activate download. otherwise, choose 0 will not download")
    ArgKsta.add_argument("--sizek", default=5132, type=int, help= "Amount News will download from ksta.de [The amount must be in range 0-5133]")
    
    parser.add_argument('--dir', type=str, default="./", help="Directory will store dataset")

    args = parser.parse_args()
    
    if args.sizek < 0 or args.sizek > 5132:
        parser.print_help()
        sys.exit()

    if args.sizeh < 0 or args.sizeh > 200853:
        parser.print_help()
        sys.exit()
    
    huffpost = HuffPost()
    
    if args.ksta == 1:
        startDownloadAllImages(args.sizek,args.dir)
    
    if args.huffpost == 1:
        huffpost.start_request(args.sizeh,args.dir)

    if args.huffpost == 0 and args.ksta == 0:
        print("---------nothing to download------------")
        parser.print_help()

    

if __name__ == "__main__":
    main()
