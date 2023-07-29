from config import HTTP

workers = 5
worker_class = 'gevent'

bind = f'{HTTP["host"]}:{HTTP["port"]}'
if HTTP['ssl']['enable']:
    keyfile = HTTP['ssl']['keyPath']
    certfile = HTTP['ssl']['certPath']