import subprocess

process = []

while True:
    action = input('Choose the action: q - to exit , s - run server and clients, x - close all windows:')
    if action == 'q':
        break
    elif action == 's':
        clients_count = int(input('Type count of clients: '))

        process.append(subprocess.Popen('python server.py', creationflags=subprocess.CREATE_NEW_CONSOLE))

        for i in range(clients_count):
            process.append(subprocess.Popen(f'python client.py -n test{i}', creationflags=subprocess.CREATE_NEW_CONSOLE))
    elif action == 'x':
        while process:
            process.pop().kill()
