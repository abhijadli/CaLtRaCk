# Project Name: CalTrack
#### Video Demo:  https://youtu.be/_-NdD0yx0fs
#### Description

***What is the most important and difficult thing which becomes an obstacle to a person's path in fitness?***
The answer is *NUTRITION*.

If you could not guess it, well you know it now, and for those who guessed it correctly, voila!!!!
Everybody can exercise, its the fun stuff, lifting weights, moving your body, sweating, feeling good, oh yeah baby!!!
But now we go home and eat a Big Mac or cheeseburger or god knows what crap. But ABHI!! we worked out, we burnt **calories**, the amount you burnt and the amount you are consuming, guess, **IT DOES NOT MATCH YOUR GOAL**.

Here comes ***CalTrack***. A web app designed to keep track of your calories and your workouts. Now when you eat food, log it into CalTrack and see where you are relative to your daily goal. You can also log your daily workouts and keep track of your progress in the weight room.
The app takes your basic physical information and then calculates your BMR a.k.a *basal metabolic rate* and then suggests you the calories required per day for you to reach your stated goal.

##### **SOURCE CODE FILES**

###### **app.py**
**PATH** : /project/
This file is the main executable python file of my project which contains all the backend flask code required to run the project.

###### **caltrack_db.sql**
**PATH** : /project/
This file contains the database design and tables used for this project in sqlite3.

###### **caltrack.db**
**PATH** : /project/
This file contains the data present in the database but in non-readable format.

###### **helpers.py**
**PATH** : /project/
This file contains some additional functions created by me which were imported in the *app.py* file.

###### **requirements.txt**
**PATH** : /project/
This file lists down the requirements for running the projects. This project was made in CS50 cloud codespace.

###### **style.css**
**PATH** : /project/static/
This file contains the css code used in the project.

###### Files in PATH : /project/static/flask_session
This folder contains data from real time flask session on which the project was tested.

###### **aplogy.html**
**PATH** : /project/templates/
This HTML file contains the code for the apology meme generated whenever some validations are failed in the project.

###### **cal_logs.html**
**PATH** : /project/templates/
This HTML file contains the code for the ***calorie logger*** page.

###### **changepassword.html**
**PATH** : /project/templates/
This HTML file contains the code for the ***change password*** page.

###### **index.html**
**PATH** : /project/templates/
This HTML file contains the code for the home page the user sees when he logs in.

###### **layout.html**
**PATH** : /project/templates/
This HTML file contains the code for the basic layout of all the pages extended using **JINJA** in every page.

###### **login.html**
**PATH** : /project/templates/
This HTML file contains the code for the login page from which the user logs in.

###### **profile.html**
**PATH** : /project/templates/
This HTML file contains the code for the set profile page from where user sets his profile.

###### **register.html**
**PATH** : /project/templates/
This HTML file contains the code for the register page from where user register his profile.

###### **workout.html**
**PATH** : /project/templates/
This HTML file contains the code for the workout page from where user can log his workouts and view his logged workouts.