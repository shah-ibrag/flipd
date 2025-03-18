import configparser

config = configparser.ConfigParser()
config.read('config.ini')

def login_credentials():
    username = config['Flipd']['Username']
    password = config['Flipd']['Password']
    return username, password

def openai_api_key():
    return config['OpenAI']['openai_api_key']
    

def deepseek_api_key():
    return config['DeepSeek']['deepseek_api_key']    
