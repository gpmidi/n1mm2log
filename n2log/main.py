#!/usr/bin/python
import logging
import signal

log = logging.getLogger('n2log')
import os, os.path
import argparse

try:
    import bs4
except ModuleNotFoundError as e:
    print("Please install BeautifulSoup4")
    log.exception("bs4 not installed or not importable: %r", e)
    exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Receive N1MM+ data and write to a log file')
    parser.add_argument('output', default='output.csv', help='CSV file to write logs to')
    parser.add_argument('--listen', default='0.0.0.0', help='IPv4 address to listen on')
    parser.add_argument('--port', default=12060, type=int)
    args = parser.parse_args()

    from n2log import Listener

    l = Listener(outfile=args.output, ip=args.listen, port=args.port, plog=log)
    l.start()

    signal.signal(signal.SIGINT, handleCtrlC)

    signal.pause()
