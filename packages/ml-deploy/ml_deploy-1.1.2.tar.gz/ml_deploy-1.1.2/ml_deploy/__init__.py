from flask import Flask
from flask_cors import CORS
from ml_deploy.main import args
from ml_deploy.kafka.utils import create_producer
from ml_deploy.metrics import Metric
from ml_deploy.utils import load_class


app = Flask(__name__)
CORS(app)


myargs = args
producer = create_producer(args.kafka_broker) if args.kafka_broker is not None else None

metric_class = getattr(myargs, 'metric_class', None)
metric_class = load_class(metric_class) if metric_class else Metric
metric = metric_class()
