# ProgramvareUtvikling
The Thoth website aims to connect students and lecturers using real-time feedback,
allowing teachers to optimise lectures to meet the academic level of the students.

The projet is availiable at http://thoth.helemork.com/. The master branch settings are thus differently from those
in the dev and other branches, which are made to run locally. If you clone the project, make sure to use the local settings.

##Students
You can log in to the lecture assistant using the unique lecture-ID on the
Thoth website. There you can rate the lecture speed and quality,
post anonymous questions, rate other students´ questions,
and participate in questionnaires or tasks by the lecturer.

##Lecturers 
Log in to receive real-time notifications about your lecturing speed and
read (and answer) student questions. You can also create questionnaires
or tasks for use within lectures, with automatic validation and a
summary of student performance.
    
##Technologies
The Thoth website coded in HTML, CSS, JavaScript, uses the django framework with a sqlite database, and the node framework for real-time interactions.Question logic is enhanced using an open source natural language processing API.

##Thoth
Thoth was the ancient egyptian god of scholars, teachers, learning and balance.
As the website aims to bring balance into the classrom, he became an inspiration and
namebringer for the project.


# HOW TO RUN THE PAGE
After installing all the django and node things you need:

##Open a power shell/git shell:
1) Go inside the django folder
2) activate the environment by writing;

environment\Scripts\activate.ps1


3) Run the django server by writing:
	
python.exe manage.py runserver


##Open a new power shell/git-shell
4) go into the node folder
5) run the nodeserver by writing:

node server.js

6) GO INTO YOUR LOCALHOST in your preferred web browser by typing:

localhost:8000
