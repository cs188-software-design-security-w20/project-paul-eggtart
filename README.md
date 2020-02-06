# RATE MY TA CS188 PROJECT

## Table of Contents
* [Introduction](#intro)
* [Getting Started](#getting-started)
* [Navigating the Site](#navigating-the-site)
* [Work In Progress / To Do](#work-in-progress/to-do)
* [Sources](#sources)

## Introduction
This project allows you to rate Teaching Assistants at UCLA. The project is set up using Python 3.

Our Link to Heroku is https://rate-my-ta.herokuapp.com/

## Getting started

### Setting up a Virtual Environment (MacOS/Linux) (optional)

```sh
$ python3 -m venv env
$ source env/bin/activate
```

https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/

### Installing Dependencies

```sh
$ pip install -r requirements.txt
```

### Launching the Server

```sh
$ python3 app.py
```

## Navigating the Site
Creating a new user will give the account 3 'remaining views' which are TA's which you are allowed to view the information of.
A 'remaining view' is used up when you search a TA from the search bar.
Once that TA has been associated with the account, the TA will always be viewable for the student.
Once the three 'remaining view's are used up, the student will have to pay to get more views (not yet implemented)
- /search
- /TA/paul-eggert


### Example Search (Closest Match)
- tian-ye becomes tian-ye
- tian becomes tian-ye
- paul becomes paul-eggert


## Work In Progress / To Do
FEATURES!
- Payment System (getting more remaining views)
- Encrypt End to End (Database)
- Clean Up Frontend for everything to make it match (Login/ Signup), Purchase.html, Search Page
- add validators to verify @ucla.edu? 


BUGS!
- Next Password Reset Date 	<UnboundField(DateTimeField, ('password_reset',), {})>
TODO!
- Take down firebase key!






## Sources
- https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/
- https://materializecss.com/
- https://wtforms.readthedocs.io/en/stable/
- https://pypi.org/project/wtforms-html5/


### Firebase documentation
- https://github.com/thisbejim/Pyrebase 