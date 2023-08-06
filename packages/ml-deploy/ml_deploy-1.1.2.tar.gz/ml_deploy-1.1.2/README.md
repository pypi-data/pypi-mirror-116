## Overview
ml-deploy is a python package for machine learning packaging and deploying. the functionality is built base on experiments and projects that have been carried out so far. This package is intended to make all the things that have been done reusable.

It provides :
1. Model Packaging
2. Model Gunicorn Deployment for Production
3. Metrics Sending trought event messaging or rest.
4. Model Serving as Rest
5. Adding custom endpoint.

## Installation

1. Clone repository http://192.168.7.138:8929/fauzantaufik/cad-it-ml.git
2. cd into ${youdirr}/python
3. pip install .

## Model Deployment

After installation, model deployment can be done by executing <b><i>ml-deploy $interface_name</i></b> command in terminal. this require you have file that contain a class to package model that will be served.

By default, model will be served by gunicorn for production ready. **Note : gunicorn cannot be run in Windows**.

if want to serve model for development purpose, set --ap-debug (APP-DEBUG if env var) to True. -> <b><i>ml-deploy $interface_name --app-debug True</i></b>

### Deployment Arguments

This are list of parameters that can be filled when deploying model :

| Name | Description | Value |
| ------ | ------ | ------ |
| interface_name | File that contain class object to package model | str |
| --http-port | server port : 500 by default | int, default value is 5000 |
| --app-debug (APP-DEBUG if env var) | if true, server will be in dev mode, if false, production mode using gunicorn | acceptable value for true ['1', 'true', 't'], otherwise it is false |
| --kafka-broker (KAFKA_BROKER if env var) | list of seperated comma value for broker address | ex: 'host:9092,host:9093,host:90094', default value is None |
| --gunicorn-access-log (GUNICORN_ACCESS_LOG if env var) | Enable gunicorn access log | boolean, option value is the same like --http-port |
| --log-level (LOG_LEVEL as env var) | Log level of the inference server. | "DEBUG", "INFO", "WARNING", "ERROR", default value is  INFO |
| --workers (GUNICORN_WORKERS if env var) | Number of Gunicorn workers for handling requests. | int, default value is 1 |
| --worker-class (GUNICORN_WORKER_CLASS if env var) | Gunicorn worker type. | <a href="https://docs.gunicorn.org/en/stable/settings.html">see gunicorn documentation for option value</a>, default value is sync   |
| --threads (GUNICORN_THREAD if env var) | Number of threads to run per Gunicorn worker. | int, default value is 1  |

## Model Packaging

In order to deploy your model, you have to package your model to make it ready to be served.
the way to package the model is by creating a file (module) that contains the class object. The minimum requirements for this class are to have:

1. __init__ method.
2. load method.
3. predict method.
4. Feedback method.

#### Example

```python
import cPickle
from ml_deploy.rest.utils import create_response
from sklearn.metrics import accuracy_score, f1_score


class UserModel:
    def __init__(self):
        self.model = None
        self.ready = False
        self.y_true = []
        self.y_predicted = []
    
    def load(self):
        with open('my_dumped_classifier.pkl', 'rb') as fid:
            gnb_loaded = cPickle.load(fid)
            self.model = gnb_loaded
    
    def predict(self, X, names):
        predicted = self.model.predict(X)
        response = create_response(
            input = X,
            target = {'y_predicted' : predicted}
        )
        return response
        
    
    def feedback(input_data, y_true, y_predicted):
        # add y_true and y_prediction
        self.y_true += append(y_true)
        self.y_predicted += append(y_predicted)
        
        # calculate metrics
        acc = accuracy_score(self.y_true, self.y_predicted)
        f1 = f1_score(self.y_true, self.y_predicted)
        acc_metric = {'name':'Accuracy', 'type': 'GAUGE', 'value':acc}
        f1_metric = {'name':'F1', 'type': 'GAUGE', 'value':f1}
        list_metrics = [acc_metric, f1_metric]
        
        response = create_response(
            input = input_data,
            target = {'y_true':y_true, 'y_predicted':y_predicted},
            list_metrics = list_metrics
        )
        
        return response
```

## Metrics
In order for your model metrics to be captured automatically and stored in the database, these requirements must be met:

1. Setup metrics-server with timescaledb
2. Setup kafka and create predict and feedback .
3. --kafka-broker (KAFKA_BROKER if env var) parameter is provided.
4. Provide a list of metrics values in a response of predict or feedback method.


#### example
```python
..........

    # calculate metrics
    acc = accuracy_score(self.y_true, self.y_predicted)
    f1 = f1_score(self.y_true, self.y_predicted)
    acc_metric = {'name':'Accuracy', 'type': 'GAUGE', 'value':acc}
    f1_metric = {'name':'F1', 'type': 'GAUGE', 'value':f1}
    list_metrics = [acc_metric, f1_metric]
    
    response = ResponseFormat(
        input = input_data,
        target = {'y_true':y_true, 'y_predicted':y_predicted},
        list_metrics = list_metrics
    )
    
    return response
    
```


## Custom Endpoints
ml-deploy provide two default endpoint for the model, which are /api/ml/predict and /api/ml/feedback. if want to add more endpoint, it can be done by adding endpoints method, and inside the method should be written flask endpoint function.

#### example
```python

    def endpoints(app):
        
        @app.route('/test', methods=['GET'])
        def test():
            return 'test'
```

## Eventing
An endpoint will send an event with message to the broker if these requirements are met:
1. Setup kafka.
2. Desired topic.
3. Endpoint return list of topic value

#### example
```python
    ......
    ......
    
    return ResponseFormat(
        input = input_data,
        target = target_data,
        list_metrics = list_metrics,
        topics = ['topic1', 'topic2']
    )
```
