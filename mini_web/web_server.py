import socket
import re
import multiprocessing
from dynamic import mini_frame01


class WebServer(object):
    def __init__(self):
        # 1. 创建套接字
        self.tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # 2. 绑定
        self.tcp_server_socket.bind(("", 7890))

        # 3. 变为监听套接字
        self.tcp_server_socket.listen(128)

    def __del__(self):
        # 6. 关闭监听套接字
        self.tcp_server_socket.close()

    def service_client(self, new_socket):
        """为客户端返回数据"""

        # 1.接收浏览器发送过来的request请求(符合http协议的格式) ，即http请求
        # GET /index.html HTTP/1.1
        request = new_socket.recv(1024).decode("utf-8")

        request_lines = request.splitlines()
        print("")
        print(">" * 20)
        print(request_lines)

        # 2.通过正则解析 GET /index.html HTTP/1.1 获取文件名 即 /index.html
        file_name = ""
        ret = re.match(r"[^/]+(/[^ ]*)", request_lines[0])
        if ret:
            file_name = ret.group(1)
            if file_name == "/":
                file_name = "/index.html"

        # 3. 通过文件名 /index.html 打开文件读取数据后 组织符合http格式的response
        # 即应答报文 header + body 给浏览器
        if not file_name.endswith(".html"):  # css，js等静态资源
            try:
                f = open("./static" + file_name, "rb")
            except FileNotFoundError:
                response = "HTTP/1.1 404 NOT FOUND\r\n"
                response += "\r\n"
                response += "------file not found-----"
                new_socket.send(response.encode("utf-8"))
            else:
                # 3.1 准备发送给浏览器的数据---response_header
                response_header = "HTTP/1.1 200 OK\r\n"
                response_header += "\r\n"
                # 3.2 准备发送给浏览器的数据---response_body
                response_body = f.read()
                f.close()

                # 将response header发送给浏览器
                new_socket.send(response_header.encode("utf-8"))
                # 将response body发送给浏览器
                new_socket.send(response_body)
        # html伪静态url
        else:
            env = dict()
            env["url"] = file_name
            response_body = mini_frame01.application(env, self.set_response_header)

            response_header = "HTTP/1.1 %s\r\n" % self.statue
            for msg in self.headers:
                response_header += "%s:%s\r\n" % (msg[0], msg[1])
            response_header += "\r\n"

            response = response_header + response_body

            new_socket.send(response.encode("utf-8"))

        # 关闭套接
        new_socket.close()

    def set_response_header(self, statue, headers):
        self.statue = statue
        self.headers = headers

    def run_for_ever(self):
        """用来完成整体的控制"""

        while True:
            # 4. 等待新客户端的链接
            new_socket, client_addr = self.tcp_server_socket.accept()

            # 5. 为这个客户端服务
            p = multiprocessing.Process(target=self.service_client, args=(new_socket,))
            p.start()

            new_socket.close()


def main():
    """业务流程"""
    my_web_server = WebServer()
    my_web_server.run_for_ever()


if __name__ == "__main__":
    main()
