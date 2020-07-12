import netaddr
import argparse
import sys
import subprocess
import json
import threading
import socket
import datetime
import multiprocessing
from concurrent.futures import ThreadPoolExecutor as TPool
from concurrent.futures import ProcessPoolExecutor as PPool

USEAGE = """
-n num : 并发数量,使用数字0可以实现多进程中自动运行cpu核数的进程
-m proc/thread: 选择是多进程模型还是多线程模型
-f ping/tcp : 要执行的操作
-ip ipaddr : ping：地址段支持：x.x.x.x-x.x.x.x和x.x.x.x/x两种格式，tcp：具体IP地址
-w json_file : 将结果保存到json文件
-v: 显示扫描耗时
"""

def parse_cmd_args() -> "NameSpace":
    parser = argparse.ArgumentParser(description=USEAGE)
    parser.add_argument("-n", type=int)
    parser.add_argument("-m", type=str)
    parser.add_argument("-f", type=str)
    parser.add_argument("-ip", type=str)
    parser.add_argument("-w", type=str)
    parser.add_argument("-v", default=False, action="store_true")
    args = parser.parse_args()
    return args

class PingResult:
    def __init__(self, ip: str, result: bool):
        self.ip = ip
        self.result = result
    def get_json(self) -> str:
        return json.dumps(self.__dict__, ensure_ascii=False)


def ping(ip: str) -> bool:
    result = subprocess.Popen("ping -i 1 -w 100 -n 1 {}".format(ip), stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.read()
    if "Reply from" in str(result):
        return PingResult(ip, True)
    else:
        return PingResult(ip, False)

class TCPScanResult:
    def __init__(self, ip: str, port: int, result: bool):
        self.ip = ip
        self.port = port
        self.result = result

    def get_json(self):
        return json.dumps(self.__dict__, ensure_ascii=False)

def scan_tcp(ip: str, port: int):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.connect((ip,port))
        return TCPScanResult(ip, port, True)
    except Exception:
        return TCPScanResult(ip, port, False)
    finally:
        server.close()

def get_ip_list(ip: str) -> list:
    ip_list = []
    if "-" in ip:
        ips = ip.split("-")
        if len(ips) != 2:
                raise Exception("IP地址格式错误，请使用：x.x.x.x-x.x.x.x或x.x.x.x/x")
        ip_list = [str(addr) for addr in netaddr.iter_iprange(ips[0], ips[1], step=1)]
    elif "/" in ip:
        ip_list = [addr for addr in netaddr.IPNetwork(ip)]
    return ip_list

def exec_ping(args: "NameSpace") -> None:
    ip_net = args.ip
    ip_list = []
    try:
        f = None
        fopen = False
        if args.w != None:
            f = open(args.w, mode="a", encoding="utf-8")
            fopen = True
        ip_list = get_ip_list(ip_net)
        if args.m == "thread":
            with TPool(args.n) as pool:
                futures = [pool.submit(ping, str(ip)) for ip in ip_list]
                start_time = datetime.datetime.now if args.v != False else 0
                for future in futures:
                    result = future.result()
                    print("Ping: {}, Result: {}".format(result.ip, result.result))
                    if args.w != None:
                        f.write(result.get_json() + "\n")
                        f.flush()
                end_time = datetime.datetime.now() if args.v != False else 0
                if start_time != 0 and end_time != 0:
                    print("ping扫描执行时间：{}".format(end_time - start_time))
        elif args.m == "proc":
            pcount = multiprocessing.cpu_count() if args.n == 0 else args.n
            with PPool(pcount) as pool:
                futures = [pool.submit(ping, str(ip)) for ip in ip_list]
                start_time = datetime.datetime.now() if args.v != False else 0
                for future in futures:
                    result = future.result()
                    print("Ping: {}, Result: {}".format(result.ip, result.result))
                    if args.w != None:
                        f.write(result.get_json() + "\n")
                        f.flush()
                end_time = datetime.datetime.now() if args.v != False else 0
                if start_time != 0 and end_time != 0:
                    print("ping扫描执行时间：{}".format(end_time - start_time))
    except Exception as e:
        sys.exit("ping扫描出错啦：{}".format(e))
    finally:
        if fopen == True:
            f.close()

def exec_tcp(args):
    try:
        ip_addr = args.ip
        f = None
        fopen = False
        if args.w != None:
            f = open(args.w, mode="a", encoding="utf-8")
            fopen = True
        if args.m == "thread":
            with TPool(args.n) as pool:
                futures = [pool.submit(scan_tcp, ip_addr, port) for port in range(1, 1025)]
                start_time = datetime.datetime.now() if args.v != False else 0
                for future in futures:
                    result = future.result()
                    print("tcp扫描：IP：{}, port：{}, result：{}".format(result.ip, result.port, result.result))
                    if args.w != None and f != None:
                        f.write(result.get_json() + "\n")
                        f.flush()
                end_time = datetime.datetime.now() if args.v != False else 0
                if start_time != 0 and end_time != 0:
                    print("tcp扫描执行时间：{}".format(end_time - start_time))
        elif args.m == "proc":
            pcount = multiprocessing.cpu_count() if args.n == 0 else args.n
            with PPool(pcount) as pool:
                futures = [pool.submit(scan_tcp, ip_addr, port) for port in range(1, 1025)]
                start_time = datetime.datetime.now() if args.v != False else 0
                for future in futures:
                    result = future.result()
                    print("tcp扫描：IP：{}, port：{}, result：{}".format(result.ip, result.port, result.result))
                    if args.w != None and f != None:
                        f.write(result.get_json() + "\n")
                        f.flush()
                end_time = datetime.datetime.now() if args.v != False else 0
                if start_time != 0 and end_time != 0:
                    print("tcp扫描执行时间：{}".format(end_time - start_time))
    except Exception as e:
        sys.exit("TCP扫描出错啦：{}".format(e))
    finally:
        if fopen == True:
            f.close()


if __name__ == "__main__":
    args = parse_cmd_args()
    if args.f == "ping":
        exec_ping(args)
    elif args.f == "tcp":
        exec_tcp(args)
    else:
        sys.exit("只支持ping/tcp操作")
