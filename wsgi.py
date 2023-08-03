from gevent import monkey
monkey.patch_all()

from gevent import ssl, pywsgi
import main
import config

if __name__ == '__main__':
    listener = (config.HTTP['host'], config.HTTP['port'])
    if config.HTTP['ssl']['enable']:
        sslContext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        sslContext.load_cert_chain(config.HTTP['ssl']['certPath'], config.HTTP['ssl']['keyPath'])
        pywsgi.WSGIServer(listener, application=main.APP, ssl_context=sslContext).serve_forever()
    else:
        pywsgi.WSGIServer(listener, application=main.APP).serve_forever()