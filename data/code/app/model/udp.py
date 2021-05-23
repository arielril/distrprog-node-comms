import socket
import struct


class Multi:
    #
    #
    #
    supernode = None
    supernode_name = ""
    # number of messages to expect (number of supernodes)
    messages_number = 0

    group = ("230.0.0.0", 4321)

    def __init__(self, supernode=None, msgs_num=0, supernode_name=""):
        super().__init__()
        self.supernode = supernode
        self.supernode_name = supernode_name
        self.messages_number = msgs_num

    def init_sock(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(0.5)

    def process_search_request(self, message=""):
        # * message => "<name>;20;<file_hash>"

        sname, msg_type, fhash = message.split(";")

        if sname == self.supernode_name:
            # ignore if it myself
            print(f"[MULTI-ProcSReq] Ignoring message from myself ({msg_type};{fhash})")
            return

        if fhash in self.supernode.node_resources:
            file_location = self.supernode.node_resources[fhash]["node_location"]
            self.send(f"21;{file_location}")
        else:
            self.send(f"22;{fhash}")

    def process_search_response(self, file_hash="", message=""):
        # * message ok => "<name>;21;<node_location>"
        # * message nok => "<name>;22;<file_hash>"

        if file_hash == "" or message == "" or ";" not in message:
            return

        sname, msg_type, answer = message.split(";")
        print("Process search response", sname, msg_type, answer)
        if sname == self.supernode_name:
            # ignore response from myself
            print(f"[MULTI-ProcSResp] Ignoring message from myself ({msg_type};{answer})")
            return None

        if msg_type == "21":
            return answer
        elif msg_type == "22":
            return None

    def receive(self):
        """
        this guy should only process requests from other supernodes
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        try:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except AttributeError:
            pass

        # loopback to local interfaces
        s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 20)

        try:
            s.bind(self.group)
        except Exception:
            print("[MULTI-Recv] failed to listen multicast")

        # tell the OS to receive from the multicast group
        group = socket.inet_aton(self.group[0])
        mreq = struct.pack("4sl", group, socket.INADDR_ANY)
        # join multicast group
        s.setsockopt(
            socket.IPPROTO_IP,
            socket.IP_ADD_MEMBERSHIP,
            mreq,
        )

        while True:
            print("[MULTI-Recv] Multicast is awaiting messages")

            data, addr = s.recvfrom(1024)
            data = data.decode("utf-8")
            print(f"[MULTI-Recv] Multicast received ({data}) from ({addr})")

            if data != None and ";20;" in data:
                self.process_search_request(data)

    def send(self, message=""):
        if message == "":
            return

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 20)

        message = f"{self.supernode_name};{message}"

        print(f"[MULTI-Send] Multicast sending message ({message})")
        s.sendto(bytes(message, "utf-8"), self.group)
        print(f"[MULTI-Send] Multicast message ({message}) was sent")
        s.close()

    def request_file_search_and_listen(self, file_hash=""):
        """
        use this guy to search resources in other supernodes
        """
        if file_hash == "":
            return None

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except AttributeError:
            pass

        s.bind(self.group)
        group = socket.inet_aton(self.group[0])
        mreq = struct.pack("4sl", group, socket.INADDR_ANY)
        # join multicast group
        s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        self.send(f"20;{file_hash}")

        received_messages = 0
        while True:
            if received_messages >= self.messages_number:
                break
            print(f"[MULTI-RSearch] Multicast is awaiting for search responses. file [{file_hash}]")

            data, addr = s.recvfrom(1024)
            data = data.decode("utf-8")
            print(f"[MULTI-RSearch] Multicast received search response from ({addr}). [{data}]")

            if self.supernode_name not in data:
                received_messages += 1

            res = self.process_search_response(file_hash, data)

            if res != None:
                # got a location for the resource
                return res
