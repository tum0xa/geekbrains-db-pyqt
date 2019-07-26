import socket
import sys
import argparse
import logging
import select
from datetime import datetime

import logs.config_server_log
from tools.msg_handler import *
from tools.decorators import log
from tools.descriptors import Port
from settings import *
from tools.metaclasses import ServerVerifier

logger = logging.getLogger('server')

@log
def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p
    return listen_address, listen_port


class Server(metaclass=ServerVerifier):
    port = Port()

    def __init__(self, listen_address, listen_port):
        self.addr = listen_address
        self.port = listen_port

        self.clients = []

        self.messages = []

        self.names = {}

    def init_socket(self):
        message = f'Server is running on {self.addr}:{self.port}'
        logger.info(message)
        print(message)

        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.bind((self.addr, self.port))
        transport.settimeout(0.5)

        self.sock = transport
        self.sock.listen()

    def run(self):

        self.init_socket()

        while True:

            try:
                client_conn, client_address = self.sock.accept()
            except OSError:
                pass
            else:
                message = f'The connection was established with address {client_address} at {datetime.now()}'
                logger.info(message)
                print(message)
                self.clients.append(client_conn)

            recv_data_lst = []
            send_data_lst = []
            err_lst = []
            try:
                if self.clients:
                    recv_data_lst, send_data_lst, err_lst = select.select(self.clients, self.clients, [], 0)
            except OSError:
                pass

            if recv_data_lst:
                for client_with_message in recv_data_lst:
                    try:
                        self.process_client_message(get_message(client_with_message), client_with_message)
                    except Exception:
                        message = f'The client {client_with_message.getpeername()} has been disconnected.'
                        logger.info(message)
                        print(message)
                        self.clients.remove(client_with_message)

            for message in self.messages:
                try:
                    self.process_message(message, send_data_lst)
                except Exception:
                    message = f'The connection with client {message[DESTINATION]} was lost at {datetime.now()}'
                    logger.info(message)
                    print(message)
                    self.clients.remove(self.names[message[DESTINATION]])
                    del self.names[message[DESTINATION]]
            self.messages.clear()

    def process_message(self, message, listen_socks):
        if message[DESTINATION] in self.names and self.names[message[DESTINATION]] in listen_socks:
            send_message(self.names[message[DESTINATION]], message)
            message = f'The message was send to {message[DESTINATION]} from {message[SENDER]}.'
            logger.info(message)
            print(message)
        elif message[DESTINATION] in self.names and self.names[message[DESTINATION]] not in listen_socks:
            raise ConnectionError
        else:
            logger.error(
                f'User {message[DESTINATION]} is not registered - sending is not available.')

    def process_client_message(self, message, client):
        logger.debug(f'Message from the client: {message}')

        if ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message:

            if message[USER][ACCOUNT_NAME] not in self.names.keys():
                self.names[message[USER][ACCOUNT_NAME]] = client
                send_message(client, RESPONSE_200)
            else:
                response = RESPONSE_400
                response[ERROR] = 'The username is busy'
                send_message(client, response)
                self.clients.remove(client)
                client.close()
            return

        elif ACTION in message and message[ACTION] == MESSAGE and DESTINATION in message and TIME in message \
                and SENDER in message and MESSAGE_TEXT in message:
            self.messages.append(message)
            return

        elif ACTION in message and message[ACTION] == EXIT and ACCOUNT_NAME in message:
            self.clients.remove(self.names[ACCOUNT_NAME])
            self.names[ACCOUNT_NAME].close()
            del self.names[ACCOUNT_NAME]
            return

        else:
            response = RESPONSE_400
            response[ERROR] = 'Bad request.'
            send_message(client, response)
            return


def main():
    listen_address, listen_port = arg_parser()
    server = Server(listen_address, listen_port)
    server.run()


if __name__ == '__main__':
    main()
