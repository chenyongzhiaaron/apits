## Web静态服务器-7-gevent版


```python

from gevent import monkey
import gevent
import socket
import sys
import re

monkey.patch_all()


class WSGIServer(object):
    """定义一个WSGI服务器的类"""

    def __init__(self, port, documents_root):

        # 1. 创建套接字
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 2. 绑定本地信息
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(("", port))
        # 3. 变为监听套接字
        self.server_socket.listen(128)

        self.documents_root = documents_root

    def run_forever(self):
        """运行服务器"""

        # 等待对方链接
        while True:
            new_socket, new_addr = self.server_socket.accept()
            gevent.spawn(self.deal_with_request, new_socket)  # 创建一个协程准备运行它

    def deal_with_request(self, client_socket):
        """为这个浏览器服务器"""
        while True:
            # 接收数据
            request = client_socket.recv(1024).decode('utf-8')
            # print(gevent.getcurrent())
            # print(request)

            # 当浏览器接收完数据后，会自动调用close进行关闭，因此当其关闭时，web也要关闭这个套接字
            if not request:
                new_socket.close()
                break

            request_lines = request.splitlines()
            for i, line in enumerate(request_lines):
                print(i, line)

            # 提取请求的文件(index.html)
            # GET /a/b/c/d/e/index.html HTTP/1.1
            ret = re.match(r"([^/]*)([^ ]+)", request_lines[0])
            if ret:
                print("正则提取数据:", ret.group(1))
                print("正则提取数据:", ret.group(2))
                file_name = ret.group(2)
                if file_name == "/":
                    file_name = "/index.html"

            file_path_name = self.documents_root + file_name
            try:
                f = open(file_path_name, "rb")
            except:
                # 如果不能打开这个文件，那么意味着没有这个资源，没有资源 那么也得需要告诉浏览器 一些数据才行
                # 404
                response_body = "没有你需要的文件......".encode("utf-8")

                response_headers = "HTTP/1.1 404 not found\r\n"
                response_headers += "Content-Type:text/html;charset=utf-8\r\n"
                response_headers += "Content-Length:%d\r\n" % len(response_body)
                response_headers += "\r\n"

                send_data = response_headers.encode("utf-8") + response_body

                client_socket.send(send_data)

            else:
                content = f.read()
                f.close()

                # 响应的body信息
                response_body = content
                # 响应头信息
                response_headers = "HTTP/1.1 200 OK\r\n"
                response_headers += "Content-Type:text/html;charset=utf-8\r\n"
                response_headers += "Content-Length:%d\r\n" % len(response_body)
                response_headers += "\r\n"
                send_data = response_headers.encode("utf-8") + response_body
                client_socket.send(send_data)

# 设置服务器服务静态资源时的路径
DOCUMENTS_ROOT = "./html"

def main():
    """控制web服务器整体"""
    # python3 xxxx.py 7890
    if len(sys.argv) == 2:
        port = sys.argv[1]
        if port.isdigit():
            port = int(port)
    else:
        print("运行方式如: python3 xxx.py 7890")
        return

    print("http服务器使用的port:%s" % port)
    http_server = WSGIServer(port, DOCUMENTS_ROOT")
    http_server.run_forever()


if __name__ == "__main__":
    main()


```