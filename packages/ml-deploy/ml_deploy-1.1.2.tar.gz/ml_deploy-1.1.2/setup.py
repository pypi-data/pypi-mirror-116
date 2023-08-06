from setuptools import setup, find_packages

find_packages()

setup(
    name="ml_deploy",
    version="1.1.2",
    description="Package to deploy ml model",
    author="Fauzan Taufik",
    author_eamil="fauzantaufik178@gmail.com",
    url="http://192.168.7.138:8929/fauzantaufik/cad-it-ml/-/tree/master/python",
    packages=find_packages(exclude=('tests', 'examples')),
    python_requires=">=3.6",
    install_requires=[
        "Flask==1.1.2",
        "Flask-Cors==3.0.10",
        "confluent-kafka==1.6.1",
        "gunicorn==20.0.0",
        "Flask-APScheduler==1.12.2",
        "pydantic==1.8.2",
        "prometheus-client==0.10.1",
        "strictyaml==1.4.4"
    ],
    entry_points={
        'console_scripts':[
            'ml-deploy = ml_deploy.main:main'
        ],
    }
)