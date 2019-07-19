# 2. Написать функцию host_range_ping() для перебора ip-адресов из заданного диапазона.
# Меняться должен только последний октет каждого адреса.
# По результатам проверки должно выводиться соответствующее сообщение.


from ipaddress import ip_network
from task1 import host_ping


def host_range_ping(subnet_address):
    subnet = ip_network(subnet_address)
    ip_addresses = [subnet.network_address+i for i in range(1, subnet.num_addresses)]
    host_ping(ip_addresses)


if __name__ == '__main__':
    subnet_address = input('Type the subnet address with the mask (example: 192.168.0.1/24) - ')
    # subnet_address = '192.168.0.1/24'
    host_range_ping(subnet_address)