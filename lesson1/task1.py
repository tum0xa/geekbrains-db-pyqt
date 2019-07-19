# 1. Написать функцию host_ping(), в которой с помощью утилиты ping будет проверяться доступность сетевых узлов.
# Аргументом функции является список, в котором каждый сетевой узел должен быть представлен именем хоста или ip-адресом.
# В функции необходимо перебирать ip-адреса и проверять их доступность с выводом соответствующего сообщения
# («Узел доступен», «Узел недоступен»).
# При этом ip-адрес сетевого узла должен создаваться с помощью функции ip_address().


from ipaddress import ip_address
from subprocess import Popen, PIPE


def host_ping(list_ip_addresses, timeout=500, requests=1, info=True):
    result = []
    for address in list_ip_addresses:
        try:
            address = ip_address(address)
        except ValueError:
            pass
        ping = Popen(f"ping {address} -w {timeout} -n {requests}", shell=False, stdout=PIPE)
        ping.wait()
        if ping.returncode == 0:
            if info:
                print(f"Network node '{address}' is accesible.")
            result.append((address, True))
        else:
            if info:
                print(f"Network node '{address}' is not accesible.")
            result.append((address, True))
    return result


if __name__ == '__main__':
    ip_addresses = ['ya.ru', '10.2.3.5', '192.168.0.1', 'localhost']
    host_ping(ip_addresses)
