import os
from pydantic import BaseModel, validator
from strictyaml import load


def fetch_config_from_yaml(cfg_path:str) -> dict:
    """Parse YAML containing the package configuration."""

    if not is_file_exists(cfg_path):
        raise OSError(f"File not found at {cfg_path!r}")
        

    with open(cfg_path, "r") as conf_file:
        parsed_config = load(conf_file.read())
        return parsed_config.data


def is_file_exists(path:str)->bool:
    if os.path.isfile(path):
        return True
    return False


def create_and_validate_config(cfg_path:str):
    yaml_config = fetch_config_from_yaml(cfg_path)
    _config = AppConfig(**yaml_config)
    return _config


class AppConfig(BaseModel):
    interface:str
    metric_class:str = None
    kafka_broker:str = None
    http_port:int = 5000
    mode:str = 'development'
    debug:bool = True
    log_level:str = 'INFO'
    workers:int = 1
    worker_class:str = 'sync'
    gunicorn_timeout:int = 5000
    threads:int = 5
    max_requests:int = 0
    max_requests_jitter:int = 0
    keepalive:int = 2


    @validator('interface')
    def option_interface_value(cls, v):
        if not is_file_exists(v):
            ValueError(f'interface file is not exists {v}')
        return v

    
    @validator('metric_class')
    def option_metric_value(cls, v):
        if not is_file_exists(v):
            ValueError(f'Metric file is not exists {v}')
        return v

    @validator('mode')
    def option_mode_value(cls, v):
        option = ['development', 'production']
        if v not in option:
            ValueError(f'Mode value must be one of this {option}')
        return v