# THOTH

## A webproject by  Group 50 in the course TDT4140 Software Engineering at NTNU, 2017
The Thoth website aims to connect students and lecturers using real-time feedback,
allowing teachers to optimise lectures to meet the academic level of the students.

The projet is availiable at http://thoth.helemork.com/. 
The master branch settings are thus differently from those
in the dev and other branches, which are made to run locally. If you clone the project, make sure to use the local settings.

## Students
You can log in to the lecture assistant using the unique lecture-ID on the
Thoth website. There you can rate the lecture speed and quality,
post anonymous questions, rate other students´ questions,
and participate in questionnaires or tasks by the lecturer.

## Lecturers 
Log in to receive real-time notifications about your lecturing speed and
read (and answer) student questions. You can also create questionnaires
or tasks for use within lectures, with automatic validation and a
summary of student performance.
    
## Technologies
The Thoth website coded in HTML, CSS, JavaScript, uses the django framework with a sqlite database, and the node framework for real-time interactions.Question logic is enhanced using Language Understanding Intelligent Service (LUIS.ai) API from microsoft.  

## Thoth
Thoth was the ancient egyptian god of scholars, teachers, learning and balance.
As the website aims to bring balance into the classrom, he became an inspiration and
namebringer for the project.


# SETUP

## Requirements:
1) Python 3
2) Node
3) Git 

## Branch (IMPORTANT!):
Checkout dev branch to run locally. The master branch has deployment specific settings specific. If running locally, run from the dev branch.

## How to start the project:
1) clone this repository
2) Install django with pip install django (1.10)
3) enter django folder
4) activate the environment by writing;

**environment\Scripts\activate.ps1**

5) create database by writing 

**python manage.py migrate**

6) start development server: 

**python.exe manage.py runserver**

## Open a new power shell/git-shell
7) go into the node folder
8) Install required packages (express, socket.io, cors, projectoxford: 

**npm install <package>**

9) run the nodeserver by writing:

**node server.js**

10) Access the webpage at LOCALHOST in your preferred web browser by typing:

**localhost:8000**

# HOW TO RUN THE TESTS
We have tests both for node and Django. The tests for node uses Mocha with Chai. 

## Install Modules for Node
You need to have both django and Node installed as previosly stated. In addition you need the Mocha and Chai modules installed. 
1) Open a new power shell/Terminal
2) Navigate to the node folder where the node server.js is
3) Install Mocha by writing:

**npm install mocha**

4) Install chai by writing:

**npm install chai**

## Run node tests
You are now ready to run the tests. Start by running the node tests
1) Open terminal/power shell
2) Navigate to the node folder
3) Run tests by writing

**mocha test**

## Run django tests
1) Open a terminal/power shell
2) Navigate to the django folder that contains manage.py
3) run tests by writing:

**python3 manage.py test**
