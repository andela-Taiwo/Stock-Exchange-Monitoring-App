# Stock-Exchange-Monitoring-App
An app that monitors the Nigeria Stock Exchange(NSE)

Badges

<<<<<<< HEAD
[![Coverage Status](https://coveralls.io/repos/github/andela-Taiwo/Stock-Exchange-Monitoring-App/badge.svg?branch=master)](https://coveralls.io/github/andela-Taiwo/Stock-Exchange-Monitoring-App?branch=master) [![CircleCI](https://circleci.com/gh/andela-Taiwo/Stock-Exchange-Monitoring-App.svg?style=svg&circle-token=228eef13aadc17b77563161162299829c1e24618)](https://circleci.com/gh/andela-Taiwo/Stock-Exchange-Monitoring-App)
=======
[![Coverage Status](https://coveralls.io/repos/github/andela-Taiwo/Stock-Exchange-Monitoring-App/badge.svg?branch=master)](https://coveralls.io/github/andela-Taiwo/Stock-Exchange-Monitoring-App?branch=master) [![CircleCI](https://circleci.com/gh/andela-Taiwo/Stock-Exchange-Monitoring-App.svg?style=svg)](https://circleci.com/gh/andela-Taiwo/Stock-Exchange-Monitoring-App)
>>>>>>> Add hosting config (#4)

## Technology 
* **Python 3** : “Python is a widely used high-level programming language for general-purpose programming, created by Guido van Rossum and first released in 1991[source](https://www.python.org/downloads/release/python-360/). An interpreted language, Python has a design philosophy which emphasizes code readability (notably using whitespace indentation to delimit code blocks rather than curly braces or keywords), and a syntax which allows programmers to express concepts in fewer lines of code than possible in languages such as C++ or Java. The language provides constructs intended to enable writing clear programs on both a small and large scale” 
* **pip** : “The PyPA recommended tool for installing Python packages” [source](https://pypi.org/project/pip/). Use pip to manage what Python packages the system or a virtualenv has available.
* **Virtualenv** : “A tool to create isolated Python environments” [source](https://virtualenv.pypa.io/en/latest/). We will use virtualenv to create a environment where the tools used will not interfere with the system’s local Python instance.
* **Django**: “Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design.” [source](https://www.djangoproject.com/). We will install Django using pip.

## Features
* - Registration `POST api/v1/registration/`
* - Login `POST api/v1/login/` 
* - Password reset  `POST api/v1/password/reset/`
* - Retrieve top losers and gainers `GET api/v1/stock/`
* - Upload stock data csv `POST api/v1/stock/`
* - List stock for a company  for a given week `GET api/v1/stock/name/{company_name}/week/{week(yyyy-mm-day)}/`
* - Upload a profile picture `POST api/v1/profile/upload/`
* - Change profile picture `PUT api/v1/profile/upload/{id}/`
* - Delete profile picture `DELETE api/v1/profile/upload/{id}/`
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> update readme
* - Create roles  `POST api/v1/roles/`
* - Retrieve roles `GET api/v1/roles/`
* - Update roles `PUT api/v1/roles/{user_id}/`
* - Update user roles `PUT api/v1/user-roles/{user_id}/update/`
* - List user roles `GET api/v1/user-roles/{user_id}/list/`

#### Yet to be implemented
<<<<<<< HEAD
=======
>>>>>>> Add hosting config (#4)
=======
>>>>>>> update readme
* - Create personal stocks porfolio  `POST api/v1/stock/portfolio/`
* - Retrieve personal `GET api/v1/stock/portfolio/`


## Installation

### Directory structure

It is recommended to use follwing directory structure:

```
<NSE> (git clone backend to this)
```
- `For environment variables follow the .env-sample or contact the developer`

## Requirements and dependencies

- Postgresql 10 (or above)
- Python 3.6.x
- `git clone https://github.com/andela-Taiwo/Stock-Exchange-Monitoring-App.git`
- `cd Stock-Exchange-Monitoring-App`
- Virtual Python environment
  - `pip install virtualenv`
    - This will install a tool called `virtualenv` that is able to create a python sandbox directory with all of the packages installed within that directory. This helps separating different project requirements 
  - `virtualenv env`
  - Mac OS X: 
    `pip install virtualenvwrapper`
    `export WORKON_HOME=~/Envs`
    `source /usr/local/bin/virtualenvwrapper.sh`
    `mkvirtualenv my_project`
        - This will create a virtual env .This environment has to be manually activated(see below)
        `workon my_project`
- `pip install -r requirements.txt`
  - This will install all of the required packages to run the server.
-  `.env` configuration file that contains basic settings for the backend, otherwise the backend won’t run.
- `python manage.py runserver`
  - First run of the API server.

### With docker
- `docker-compose build`
- `docker-compose up -d`
- `open address locahost:8000/ on your browser`

## Running
Everytime you’ll want to call python code, you need to activate the environment first:

- `Stock-Exchange-Monitoring-App`
- `workon my_project`

Then you can proceed with running the server (or other operations described below):



To turn it off, simply stop the process in the command line.
## Running Tests:
 - `cd Stock-Exchange-Monitoring-App`
 - `tox`

## Updating
- Optionally turn off the server. It might be needed in some cases when the changes are too complex. Otherwise the running server usually picks up the changes automatically and restarts itself.
- `git pull`
- `py manage.py migrate`
- Turn server back on if you have turned it off with `python manage.py runserver`




## Authors

* **Sokunbi Taiwo** - [Taiwo](https://github.com/andela-Taiwo)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details