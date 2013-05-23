## Dependencies

- Python 2.7
- rabbitmq-server
- Requests
- Celery
- Flask
- Tor
- mongoDB

## Steps

### Install python-pip

 sudo aptitude install python-pip python-virtualenv

### Create virtualenv

virtualenv --distribute venv

### Activate virtualenv

source venv/bin/activate

### instal python-packages using pip

 pip install -r requirements.txt

### Install `mongodb-server`, `rabbitmq-server`
 sudo aptitude install mongodb-server rabbitmq-server
###
 Download and install latest stable release of `MongoDB` from [official website](http://www.mongodb.org/)

### Install `Tor proxy`
 sudo aptitude install tor
