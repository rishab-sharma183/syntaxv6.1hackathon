from gevent import monkey

monkey.patch_all()

from website import create_app
from flask_compress import Compress
from gevent.pywsgi import WSGIServer

app = create_app()

compress = Compress()
compress.init_app(app)

if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 8080), app)
    http_server.serve_forever()
