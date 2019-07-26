import json
import socket
import argparse
import logging
import threading
from random import sample
from string import ascii_letters

from server import *
from settings import *
from tools.decorators import log
from tools.metaclasses import ClientVerifier
from tools.msg_handler import *

logger = logging.getLogger('client')


class ClientSender(threading.Thread, metaclass=ClientVerifier):
    def __init__(self, account_name, sock):
        self.account_name = account_name
        self.sock = sock
        super().__init__()

    def create_exit_message(self):
        return {
            ACTION: EXIT,
            TIME: time.time(),
            ACCOUNT_NAME: self.account_name
        }

    def create_message(self):
        to = input('Type the username: ')
        message = input('Type the message for: ')
        message_dict = {
            ACTION: MESSAGE,
            SENDER: self.account_name,
            DESTINATION: to,
            TIME: time.time(),
            MESSAGE_TEXT: message
        }
        logger.debug(f'The dictionary for the message was formed: {message_dict}')
        try:
            send_message(self.sock, message_dict)
            logger.info(f'The message has been send for the user {to}')
        except Exception:
            logger.critical('Connection is lost.')
            exit(1)

    def run(self):
        self.print_help()
        while True:
            command = input('Type the command: ')
            if command == 'message':
                self.create_message()
            elif command == 'help':
                self.print_help()
            elif command == 'exit':
                try:
                    send_message(self.sock, self.create_exit_message())
                except:
                    pass
                print('Disconnecting...')
                logger.info('Exit by user.')
                time.sleep(0.5)
                break
            else:
                print('Command is unknown, try again. Type "help" for the getting help.')

    def print_help(self):
        print('Available commands:')
        print('message - send message;')
        print('help - show information about commands;')
        print('exit - exit from the messenger.')


class ClientReader(threading.Thread, metaclass=ClientVerifier):
    def __init__(self, account_name, sock):
        self.account_name = account_name
        self.sock = sock
        super().__init__()

    def run(self):
        while True:
            try:
                message = get_message(self.sock)
                if ACTION in message and message[ACTION] == MESSAGE and SENDER in message and DESTINATION in message \
                        and MESSAGE_TEXT in message and message[DESTINATION] == self.account_name:
                    message = f'The message has been received from {message[SENDER]}:\n{message[MESSAGE_TEXT]}'
                    print(f'\n{message}')
                    logger.info(message)
                else:
                    logger.error(f'Bad message from the server: {message}')
            except IncorrectDataReceivedError:
                logger.error(f'Could not decode the message.')
            except (OSError, ConnectionError, ConnectionAbortedError, ConnectionResetError, json.JSONDecodeError):
                logger.critical(f'The connection to server was lost.')
                break


@log
def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-n', '--name', default=None, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_name = namespace.name

    if not 1023 < server_port < 65536:
        message = f'Wrong port number {server_port}. Correct value for a port number is in range from 1024 to 65535.' \
            f'Will be used a default port number {DEFAULT_PORT}.'
        logger.critical(message)
        exit(1)

    return server_address, server_port, client_name


def main():
    print('The Messenger!')

    server_address, server_port, client_name = arg_parser()

    if not client_name:
        client_name = input('Type username: ')
    else:
        print(f'Your name is: {client_name}')
    message = f'Messenger is running: Server: {server_address}:{server_port}, Username: {client_name}'
    logger.info(message)

    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        send_message(transport, create_presence(client_name))
        answer = process_response_ans(get_message(transport))
        message = 'Connection to server has been established.'
        logger.info(f'{message}. Server response: {answer}')
        print(f'{message}')
    except json.JSONDecodeError:
        logger.error('Could not decode the json')
        exit(1)
    except ServerError as error:
        logger.error(f'Server error while connecting: {error.text}')
        exit(1)
    except ReqFieldMissingError as missing_error:
        logger.error(f'Field {missing_error.missing_field} is missing')
        exit(1)
    except (ConnectionRefusedError, ConnectionError):
        logger.critical(
            f'Could not connect to {server_address}:{server_port}. Connection refused.')
        exit(1)
    else:

        module_receiver = ClientReader(client_name, transport)
        module_receiver.daemon = True
        module_receiver.start()

        module_sender = ClientSender(client_name, transport)
        module_sender.daemon = True
        module_sender.start()

        while True:
            time.sleep(1)
            if module_receiver.is_alive() and module_sender.is_alive():
                continue
            break


if __name__ == '__main__':
    main()
