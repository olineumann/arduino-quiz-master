import os
import json
import serial

with open('config.json', 'rb') as config_file:
    config = json.load(config_file)
serial_interface = serial.Serial(**config['serial'])
push_time = -1


def start():
    if os.name == 'posix':
        # for mac and linux(here, os.name is 'posix')
        _ = os.system('clear')
    else:
        # for windows platfrom
        _ = os.system('cls')
    print('Welcome to Buzz Night! You can close the game or reset the buzzer with CTRL+C!\n')


def loop():
    global serial_interface
    global push_time
    if serial_interface.inWaiting():
        serial_input = serial_interface.readline()
        serial_input = [chr(x) for x in serial_input]
        serial_input = ''.join(serial_input)
        serial_input = serial_input.replace('\n', '')
        if serial_input == 'reset':
            pass
        else:
            player, pin, time = [int(x) for x in serial_input.split(';')]
            if str(player) in config['player']:
                player = config['player'][str(player)]
            if push_time < 0:
                push_time = time
                print(f'Player {player} pushed first!')
            else:
                print(f'Player {player} was {time - push_time}ms to late!')

    keyboard_input = '' # input()
    if keyboard_input == 'r':
        serial_interface.write(b'reset\n')


if __name__ == '__main__':
    start()
    while True:
        try:
            loop()
        except KeyboardInterrupt:
            keyboard_input = input('Do you want to stop the game (s) or reset the buzzer (r)? ')
            if keyboard_input == 'r':
                serial_interface.write(b'reset\n')
                push_time = -1
                start()
            elif keyboard_input == 's':
                exit()
            else:
                print('Unkown command!')

