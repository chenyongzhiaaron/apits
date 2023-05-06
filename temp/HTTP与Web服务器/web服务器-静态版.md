# web服务器-静态版



```python
import socket


def handle_request(client_socket):
    """
    处理浏览器发送过来的数据
    然后回送相对应的数据（html、css、js、img。。。）
    :return:
    """
    # 1. 接收
    recv_content = client_socket.recv(1024).decode("utf-8", errors="ignore")

    print("-----接收到的数据如下----：")
    print(recv_content)

    # 2. 处理请求（此时忽略）

    # 3.1 整理要回送的数据
    response_headers = "HTTP/1.1 200 OK\r\n"
    response_headers += "Content-Type:text/html;charset=utf-8\r\n"
    response_headers += "\r\n"

    response_boy = "hahahah"

    response = response_headers + response_boy

    # 3.2 给浏览器回送对应的数据
    client_socket.send(response.encode("utf-8"))

    # 4. 关闭套接字
    client_socket.close()


def main():
    """
    用来控制整体
    :return:
    """

    # 1. 创建套接字
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 为了保证在tcp先断开的情况下，下一次依然能够使用指定的端口，需要设置
    tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # 2. 绑定本地信息
    tcp_server_socket.bind(("", 8081))

    # 3. 变成监听套接字
    tcp_server_socket.listen(128)

    while True:
        # 4. 等待客户端的链接
        client_socket, client_info = tcp_server_socket.accept()

        print(client_info)  # 打印 当前是哪个客户端进行了请求

        # 5. 为客户端服务
        handle_request(client_socket)

    # 6. 关闭套接字
    tcp_server_socket.close()


if __name__ == '__main__':
    main()

```

