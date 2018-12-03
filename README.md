[![Build Status](https://travis-ci.org/leobene/Simple-Competition-Flask-API.svg?branch=master)](https://travis-ci.org/leobene/Simple-Competition-Flask-API)
[![Coverage Status](https://coveralls.io/repos/github/leobene/Simple-Competition-Flask-API/badge.svg?branch=master)](https://coveralls.io/github/leobene/Simple-Competition-Flask-API?branch=master)
# Simple-Competition-Flask-API
A simple **REST** API to create and record competitions using Flask

## API 

From the API we can:

1. Create a competition
2. Add results to a competition (all fields are mandatory), 
  
  ex: 
  ```json
  {
    "competicao": "100m classificatoria 1", 
    "atleta": "Joao das Neves", 
    "value": "10.234", 
    "unidade": "s"
  }
  ```
  ex: 
  ```json
  {
    "competicao": "Dardo semifinal", 
    "atleta": "Claudio", 
    "value": "70.43", 
    "unidade": "m"
  }
  ```
3. Finish a competition.
4. Return the competition rank, showing the final position of each athlete.

### **Rules**:
1. The API should not accept results records if the competition is already finished.
2. The API may return the ranking / partial result if the dispute is not yet finished.
3. In the darts throw competition, each athlete will have 3 chances, and the result of
competition shall take into account the furthest throwing of each athlete.


## Setting up the application
To download and start the application issue the following commands.
First clone the application code into any directory on your disk:

$ cd /path/to/my/workspace/

$ git clone https://github.com/leobene/Simple-Competition-Flask-API

$ cd Simple-Competition-Flask-API

Create a virtual Python environment in a directory named venv, activate the virtualenv and install required dependencies using pip:

$ virtualenv -p python3 venv

$ source venv/bin/activate

(venv) $ pip install -r requirements.txt

Now let’s start the app:

(venv) $ python app.py

OK, everything should be ready. In your browser, open the URL http://127.0.0.1:5006/

## Testing the application

To run the unit, integration or system tests just folow the example above:

$python -m unittest tests/system/entry_test.py

