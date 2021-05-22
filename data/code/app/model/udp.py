import socket
import struct


class Multi:
    #
    #
    #
    supernode = None
    # number of messages to expect (number of supernodes)
    messages_number = 0

    group = ("230.0.0.0", 4321)

    def __init__(self, supernode=None, msgs_num=0):
        super().__init__()
        self.supernode = supernode
        self.messages_number = msgs_num

    def init_sock(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(0.5)

    def process_search_request(self, message=""):
        # * message => "20:<file_hash>"

        fhash = message.split(":")[1]
        if fhash in self.supernode.node_resources:
            file_location = self.supernode.node_resources[fhash]["node_location"]
            self.send(f"21:{file_location}")
        else:
            self.send(f"22:{fhash}")

    def process_search_response(self, file_hash="", message=""):
        # * message ok => "21:<node_location>"
        # * message nok => "22:<file_hash>"

        if file_hash == "" or message == "" or ":" not in message:
            return

        msg_type, answer = message.split(":")

        if msg_type == "21" and answer == file_hash:
            return answer
        elif msg_type == "22":
            return None

    def receive(self):
        """
        this guy should only process requests from other supernodes
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.bind(("", 55555))
        except OSError:
            s.bind(("", 55556))
        # tell the OS to receive from the multicast group
        group = socket.inet_aton(self.group[0])
        mreq = struct.pack("4sL", group, socket.INADDR_ANY)
        # join multicast group
        s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        messages_received = []
        while True:
            print("[+] Multicast is awaiting messages")

            data, addr = s.recvfrom(1024)
            print(f"[+] Multicast received ({len(data)}) bytes from addr ({addr})")

            if data != None and "20:" in data:
                self.process_search_request(message)

    def send(self, message=""):
        if message == "":
            return

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sent = s.sendto(bytes(message, "utf-8"), self.group)
        print(f"[+] Multicast message ({message}) was sent ({sent})")
        s.close()

    def request_file_search_and_listen(self, file_hash=""):
        """
        use this guy to search resources in other supernodes
        """
        if file_hash == "":
            return None

        self.send(f"20:{file_hash}")

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(("", 44444))
        group = socket.inet_aton(self.group[0])
        mreq = struct.pack("4sL", group, socket.INADDR_ANY)
        # join multicast group
        s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        received_messages = 0
        while True:
            if received_messages >= self.messages_number:
                break
            print(f"[+] Multicast is awaiting for search responses. file [{file_hash}]")

            data, addr = s.recvfrom(1024)
            print(f"[+] Multicast received search response from ({addr})")
            received_messages += 1

            res = self.process_search_response(file_hash, message)

            if res != None:
                # got a location for the resource
                return res
