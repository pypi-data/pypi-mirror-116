from abc import ABC, abstractmethod
import logging
import time
import traceback

from ml_deploy import app, myargs, producer, metric
from ml_deploy.rest.utils import check_return_model_md, process_api_prefix, threads, post_worker_init
from ml_deploy.utils import bool_as_str
from ml_deploy.gunicorn.utils import accesslog

from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from flask import request, g


class BaseDeploy(ABC):
    __name__ = None
    __version__ = None
    __api_prefix__ = None


    def __init__(self) -> None:
        super(BaseDeploy, self).__init__()
        self.__app = app
        self.__producer = producer
        self.app_debug = bool_as_str(myargs.app_debug)
        self.mode = myargs.mode
        self.setup_md()
        self.setup_logger()
        self.metric = metric
        self.app.wsgi_app = DispatcherMiddleware(self.app.wsgi_app, {
            f'/metrics': make_wsgi_app(registry=metric.registry)
        })


    @property
    def app(self):
        return self.__app

    
    @property
    def producer(self):
        return self.__producer

    
    def setup_logger(self):
        if not self.app_debug :
            gunicorn_logger = logging.getLogger('gunicorn.error')
            self.app.logger.handlers = gunicorn_logger.handlers

    
    def setup_md(self):
        self.model_name = check_return_model_md(self, None, '__name__')
        self.model_version = check_return_model_md(self, None, '__version__')
        self.api_prefix = check_return_model_md(self, None, '__api_prefix__')
        self.api_prefix_processed = process_api_prefix(self.api_prefix)
    

    @abstractmethod
    def load(self):
        pass



    def api_resources(self):
        @self.app.errorhandler(500)
        def internal_error(e):
            self.metric.record('request_counter', dim_vals={
                    'method':request.method, 'endpoint' : request.url_rule, 'status': 500,
                    'model': self.model_name, 'version' : self.model_version
                }, value=1)
            return {
                'message' : 'Oops, internal server error',
                'error' : str(e),
                'traceback' : str(traceback.format_exc())
                }, 500

        
        @self.app.before_request
        def before_request():
            g.start = time.time()



    def after_request(self, response):
        try :
            self.metric.record('request_counter', dim_vals={
                'method':request.method, 'endpoint' : request.url_rule, 'status': response.status_code,
                'model': self.model_name, 'version' : self.model_version
            }, value=1)


            procee_time = time.time() - g.start
            self.metric.record('request_timer', dim_vals={
                'method':request.method, 'endpoint' : request.url_rule, 'status': response.status_code,
                'model': self.model_name, 'version' : self.model_version
            }, value=procee_time)
        except :
            pass


    def dev_run(self):
        http_port = myargs.http_port

        self.app.run(
            host='0.0.0.0',
            port = http_port,
            debug=True,
            threaded=False if myargs.single_threaded else True,
        )


    def prod_run(self):
        from ml_deploy.gunicorn.app import UserModelApplication
        worker_class = myargs.worker_class
        http_port = myargs.http_port

        options = {
            "bind": "%s:%s" % ("0.0.0.0", http_port),
            "accesslog": accesslog(bool_as_str(myargs.gunicorn_access_log)),
            "loglevel": myargs.log_level.lower(),
            "timeout": myargs.gunicorn_timeout,
            "threads": threads(myargs.threads, myargs.single_threaded),
            "workers": myargs.workers,
            "max_requests": myargs.max_requests,
            "max_requests_jitter": myargs.max_requests_jitter,
            "worker_class": worker_class,
            "post_worker_init": post_worker_init,
            "enable_stdio_inheritance" : True,
            "keepalive": myargs.keepalive
        }

        if myargs.pidfile is not None:
            options["pidfile"] = myargs.pidfile
        

        UserModelApplication(
            self.app, options=options
        ).run()


    def run(self):
        if self.mode == 'development':
            self.dev_run()
        elif self.mode == 'production' :
            self.prod_run()