# 3. Написать функцию host_range_ping_tab(), возможности которой основаны на функции из примера 2.
# Но в данном случае результат должен быть итоговым по всем ip-адресам, представленным в табличном формате
# (использовать модуль tabulate). Таблица должна состоять из двух колонок.

from tabulate import tabulate
from task2 import host_range_ping


def host_range_ping_tab(subnet_address, start_address=None, end_address=None):
    headers = ["address", "status"]
    addresses_dict = {'Reachable': [],
                      'Unreachable': []}

    for address in host_range_ping(subnet_address, start_address=start_address, end_address=end_address, info=False):
        address_dict = dict(zip(headers, address))
        if address_dict['status'] == True:
            addresses_dict['Reachable'].append(str(address[0]))
        else:
            addresses_dict['Unreachable'].append(str(address[0]))
    return tabulate(addresses_dict, tablefmt="pipe", headers='keys', stralign="center")


if __name__ == '__main__':
    subnet_address = '192.168.0.0/24'
    start_address = '192.168.0.4'
    end_address = '192.168.0.10'
    print('Please wait...')
    result_table = host_range_ping_tab(subnet_address, start_address=start_address, end_address=end_address)
    print(result_table)
