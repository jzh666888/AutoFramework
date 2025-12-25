import yaml

from main import DIR


def env_config():
    """读取环境变量"""
    with open(file=f'{DIR}\\data\\envConfig\\config.yaml',mode='r',encoding='utf-8') as f:
        return yaml.load(f,Loader=yaml.FullLoader)

def api_config():
    with open(file=f'{DIR}\\data\\apiConfig\\config.yaml',mode='r',encoding='utf-8') as f:
        return yaml.load(f,Loader=yaml.FullLoader)

if __name__ == '__main__':
    print(env_config())
