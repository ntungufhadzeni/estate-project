import configparser

config = configparser.ConfigParser()
config.read('config.txt')

sender_email = config.get('email', 'email')
password = config.get('email', 'password')
smtp_server = config.get('email', 'server')
smtp_port = config.get('email', 'port')
