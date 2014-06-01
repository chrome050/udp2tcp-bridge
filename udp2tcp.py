import socket, time
from threading import Thread

class Udp2Tcp (Thread):
    def __init__ (self):
        Thread.__init__(self)

        self._port = 10000
        self._dst = '10.2.1.231'
        self._dst_port = 4711

        self.daemon = True
        self.start()

    def _init(self):
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp.bind(('0.0.0.0', self._port))

        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp.connect((self._dst, self._dst_port))
        self.tcp.setblocking(False)

    def run(self):
        self._init()
        while True:
            try:
                data, address = self.udp.recvfrom(1024)
                if len(data) > 0:
                    print("Received {0} bytes via udp from {1}".format(len(data), address))
                    self.tcp.sendall(data)
                data = self.tcp.recv(1024)
                if len(data) > 0:
                    print("Received {0} bytes via tcp".format(len(data)))
                    self.udp.sendall(data)
            except Exception as e:
                print(e)

        self._deinit()

    def _deinit(self):
        self.tcp.shutdown(socket.SHUT_RDWR)
        self.udp.shutdown(socket.SHUT_RDWR)

if __name__ == '__main__':
    print ("Opening gateway ...")
    v = Udp2Tcp()
    time.sleep(120)
    print ("Closing gateway ...")

