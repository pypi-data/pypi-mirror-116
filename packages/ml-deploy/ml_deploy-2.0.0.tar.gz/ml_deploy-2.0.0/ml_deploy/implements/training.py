from abc import ABC, abstractmethod
import json


from ml_deploy.implements.base import BaseDeploy
from ml_deploy import metric
from flask_apscheduler import APScheduler
from prometheus_client import Enum


class Training(BaseDeploy, ABC):
    
    def __init__(self) -> None:
        super().__init__()
        self.setup_scheduler()
        Enum('training_task', 'State of training task', states=['running', 'rest'], registry=self.metric.registry)
        metric.record('training_task', value='rest')
        

    def setup_scheduler(self):
        scheduler = APScheduler()
        self.scheduler = scheduler
        self.scheduler.init_app(self.app)
        self.scheduler.start()


    @abstractmethod
    def train(self):
        pass



    def is_training(self):
        training_state = self.metric.enum_state_value('training_task')
        if training_state == 'running':
            message = 'There is still another process of training'
            self.app.logger.info(message)
            return True
        return False
        
    
    def api_resources(self):
        super().api_resources()
        

        @self.app.after_request
        def after_request(response):
            self.after_request(response)
            try :
                data = json.loads(response.data)
                data = self.add_model_md(data)
                response.data = json.dumps(data)
                return response
            except :
                return response
                

        @self.scheduler.task('cron', id='train', **self.cron_datetime)
        def train_scheduler():
            is_training = self.is_training()
            if is_training:
                self.app.logger.info('There is still another process of training')
            else :
                self.metric.record('training_task', value='running')
                self.train()
                self.metric.record('training_task', value='rest')

        
        @self.app.route(f'{self.api_prefix_processed}/train', methods=['POST'])
        def train_api():
            is_training = self.is_training()
            if is_training :
                message = 'There is still another process of training'
                return {'message' : message, 'status_code':200}

            self.metric.record('training_task', value='running')
            self.train()
            self.metric.record('training_task', value='rest')
            return {'message' : 'Model is trained', 'status_code':200}
