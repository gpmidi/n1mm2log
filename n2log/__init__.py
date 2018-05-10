import socket
import threading
import logging
import bs4


class Listener(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(Listener, self).__init__(*args, **kwargs)
        self.ip = kwargs.get('ip', '0.0.0.0')
        self.port = kwargs.get('port', 12060)
        self.outfile = kwargs.get('outfile', 'output.csv')
        self.plog = kwargs.get('plog', logging.getLogger('n2log'))
        self.log = self.plog.getChild(self.__class__.__name__)
        self.doRun = True

    def disable_sig(self, signum, frame):
        self.doRun = False

    def run(self):
        self.log.info("Running worker thread for n2log named %r", self.getName())
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.ip, self.port))
        with open(self.outfile, 'wb+') as f:
            self.log.info("%r opened as %r", self.outfile, f)
            while self.doRun:
                data, addr = self.sock.recvfrom(1024 * 1024)
                self.log.debug("Got packet %r from %r",data[:20],addr)
                doc = bs4.BeautifulSoup(data,'xml')
