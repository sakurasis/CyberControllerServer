import socket


class TcpServer:
    def __init__(self):
        self.port = 2233  # ���ö˿�
        self.HEAD_LEN = 8
        self.tcpServerSocket = socket.socket()  # ����socket����
        hostname = socket.gethostname()  # ��ȡ����������
        sysinfo = socket.gethostbyname_ex(hostname)
        hostip = sysinfo[2][2]
        self.tcpServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # �ö˿ڿ��Ը���
        self.tcpServerSocket.bind((hostip, self.port))  # ����ַ���׽��ְ󶨣����׽���Ҫ���Ǵ�δ���󶨹���
        self.tcpServerSocket.listen(5)  # �����¼����Ŷӵȴ�connect�������Ŀ

    def set_receive_listener(self, receive_listener):
        self.receive_listener = receive_listener

    def server(self):
        while True:
            print("�ȴ�����")
            self.clientSocket, addr = self.tcpServerSocket.accept()
            print('���ӵ�ַ��', addr)
            if self.connected_listener:
                self.connected_listener()
            while True:
                try:
                    head_data = self.clientSocket.recv(self.HEAD_LEN)
                    if not len(head_data) == 8:
                        print("bad package!head_data len:", head_data)
                        self.restart()
                        return
                    body_len = self.get_length_from_head_data(head_data)
                    body_data = self.clientSocket.recv(body_len)
                    if not body_len == len(body_data):
                        print("bad package!body_len:", body_len)
                        self.restart()
                        return
                    data_type = self.get_type_from_head_data(head_data)

                    if data_type == 1:  # test/json data
                        text = body_data.decode()
                        print(text)
                        if not text:
                            break
                        if self.receive_listener:
                            self.receive_listener(text)
                    elif data_type == 2:  # image data
                        pass

                except ConnectionResetError:
                    print("ConnectionResetError!")
                    self.restart()
                    return

            self.clientSocket.close()  # �ر�����
            self.tcpServerSocket.close()
import socket
import threading


class TcpServer:
    def __init__(self):
        self.port = 2233  # ���ö˿�
        self.HEAD_LEN = 8
        self.tcpServerSocket = socket.socket()  # ����socket����
        hostname = socket.gethostname()  # ��ȡ����������
        sysinfo = socket.gethostbyname_ex(hostname)
        hostip = sysinfo[2][2]
        self.tcpServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # �ö˿ڿ��Ը���
        self.tcpServerSocket.bind((hostip, self.port))  # ����ַ���׽��ְ󶨣����׽���Ҫ���Ǵ�δ���󶨹���
        self.tcpServerSocket.listen(5)  # �����¼����Ŷӵȴ�connect�������Ŀ

    def set_receive_listener(self, receive_listener):
        self.receive_listener = receive_listener

    def server(self):
        while True:
            print("�ȴ�����")
            self.clientSocket, addr = self.tcpServerSocket.accept()
            print('���ӵ�ַ��', addr)
            if self.connected_listener:
                self.connected_listener()
            while True:
                try:
                    head_data = self.clientSocket.recv(self.HEAD_LEN)
                    if not len(head_data) == 8:
                        print("bad package!head_data len:", head_data)
                        self.restart()
                        return
                    body_len = self.get_length_from_head_data(head_data)
                    body_data = self.clientSocket.recv(body_len)
                    if not body_len == len(body_data):
                        print("bad package!body_len:", body_len)
                        self.restart()
                        return
                    data_type = self.get_type_from_head_data(head_data)

                    if data_type == 1:  # test/json data
                        text = body_data.decode()
                        print(text)
                        if not text:
                            break
                        if self.receive_listener:
                            self.receive_listener(text)
                    elif data_type == 2:  # image data
                        pass

                except ConnectionResetError:
                    print("ConnectionResetError!")
                    self.restart()
                    return

            self.clientSocket.close()  # �ر�����
        self.tcpServerSocket.close()

    def get_length_from_head_data(self, head_data):
        if (not len(head_data) == 8):
            return
        ch1 = head_data[4] & 0x00FF
        ch2 = head_data[5] & 0x00FF
        ch3 = head_data[6] & 0x00FF
        ch4 = head_data[7] & 0x00FF
        return ((ch1 << 24) + (ch2 << 16) + (ch3 << 8) + (ch4 << 0));

    def get_type_from_head_data(self, head_data):
        if (not len(head_data) == 8):
            return
        ch1 = head_data[0] & 0x00FF
        ch2 = head_data[1] & 0x00FF
        ch3 = head_data[2] & 0x00FF
        ch4 = head_data[3] & 0x00FF
        return ((ch1 << 24) + (ch2 << 16) + (ch3 << 8) + (ch4 << 0))

    def start(self):
        self.server_threading = threading.Thread(target=self.server, args=())
        self.server_threading.start()

    def restart(self):
        self.start()

    def send_data(self, data):
        try:
            self.clientSocket.send(data)
        except ConnectionResetError:
            print("ConnectionResetError!")
            self.restart()

    def send_img(self, bytes_data):
        data = self.wrapper_data(2, bytes_data)
        self.send_data(data)

    def send_text(self, text):
        data = self.wrapper_data(1, text.encode())
        self.send_data(data)

    def wrapper_data(self, data_type, body_data):

        print("data_type:", data_type)
        print("body_data len:", len(body_data))

        type_bytes = data_type.to_bytes(4, 'big')
        print("type_bytes:", type_bytes)
        body_len = len(body_data)

        body_len_bytes = body_len.to_bytes(4, 'big')
        print("body_len_bytes:", body_len_bytes)

        head_data = type_bytes + body_len_bytes
        print("head_data:", head_data)

        data = head_data + body_data
        return data
