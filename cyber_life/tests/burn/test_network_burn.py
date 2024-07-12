"""
发出大量请求，加大吞吐量（不会拉满）
向某个网站发出 HTTP 请求

！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
！！！警告：一定注意发送频率不要过大，否则有被认为是 DoS 攻击的风险！！！
！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
"""

import socket
import ssl
import threading


class NetworkRequester:
    """
    网络请求器，用于发出 GET 请求

    支持 HTTP 请求和 HTTPS 请求
    """

    REQUEST_TEMPLATE = 'GET / HTTP/1.1\r\nHost: {url}\r\nConnection: close\r\n\r\n'

    def __init__(self, url: str):
        self.url = url

    def http_request(self):
        """
        发出 HTTP 请求
        """
        # 创建一个 TCP/IP 套接字
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 连接到服务器
        sock.connect((self.url, 80))

        # 发送请求
        # 为了不引入第三方库，这里手动构建 HTTP 请求
        sock.sendall(self.REQUEST_TEMPLATE.format(url=self.url).encode())

        # 接收响应
        response = self._recv_all(sock)

        # 打印响应
        self._output_response(response)

        # 关闭套接字
        sock.close()

    def https_request(self):
        """
        发出 HTTPS 请求
        """
        # 创建一个 TCP/IP 套接字
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 包装 socket 以支持 SSL/TLS
        ssl_context = ssl.create_default_context()
        secure_sock = ssl_context.wrap_socket(sock, server_hostname=self.url)

        # 连接到服务器
        secure_sock.connect((self.url, 443))

        # 发送请求
        # 为了不引入第三方库，这里手动构建 HTTP 请求
        # HTTPS 里的这个 *S* 是一套独立于 HTTP 的安全协议，HTTP 请求部分与先前一致
        secure_sock.sendall(self.REQUEST_TEMPLATE.format(url=self.url).encode())

        # 接收响应
        response = self._recv_all(secure_sock)

        # 打印响应
        self._output_response(response)

        # 关闭连接
        secure_sock.close()

    @staticmethod
    def _recv_all(sock: socket.socket) -> bytes:
        """
        接收所有数据
        """
        response = b''
        while True:
            data = sock.recv(65536)
            if not data:
                break
            response += data
        return response

    @staticmethod
    def _output_response(response: bytes):
        """
        输出响应
        """
        # print(response.decode(errors='ignore'))
        print(f'size={len(response)}')


def network_burn(url: str, n_each_thread: int, n_threads: int, https: bool = False):
    """
    多线程请求

    :param url: 请求的 URL
    :param n_each_thread: 每个线程发出的请求数量
    :param n_threads: 线程数量
    :param https: 是否使用 HTTPS 请求
    """

    assert isinstance(n_each_thread, int) and isinstance(n_threads, int) and n_each_thread > 0 and n_threads > 0

    baidu_requester = NetworkRequester(url)

    request_func = baidu_requester.https_request if https else baidu_requester.http_request

    def inner():
        print(f'线程 {threading.current_thread().name} 开始运行')
        for _ in range(n_each_thread):
            request_func()

    ts = []
    for _ in range(n_threads):
        ts.append(threading.Thread(target=inner, name=str(_)))
    for t in ts:
        t.start()
    for t in ts:
        t.join()


if __name__ == '__main__':
    # 百度贴吧首页
    URL = 'news.baidu.com'
    # test_network_burn(URL, 1, 1, https=True)
    network_burn(URL, 10, 200, https=True)
