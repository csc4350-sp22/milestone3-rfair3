# Milestone3-rfair3

## How to get Started:

###
For anyone looking to clone my repository and run the app locally:

You will need to install the following using pip or pip3 install:

1.Flask

2.requests

3.flask-login

4.Flask-WTf

5.Flask

6.SQLAlchemy

7.WTForms

8.Flaks-bcrypt

9.dotenv

10. psycopg2


You also need to reqister for 3 things. The first is a api key from The Movie Database. You must apply for a API key by creating a profile as well as applying for the API key itself.
The API key that you will need is version 3. The second is register for a heroku database using the command "heroku create" and "heroku addons:create heroku-postgresql:hobby-dev"
in your terminal. IF THE URL STARTS WITH postgres:, replace that with postgresql: Finally you will also need t ocreate a secrect key of your choice. This can be any combination of characters. Your .env file should look like the following:

export api_key= “YOUR API KEY HERE”
export DATABASE_URL="YOUR DATABASE KEY HERE"
export SECRET_KEY="YOUR SECRET KEY HERE"

Make sure to also add the .env file to a .gitignore file. To run the app locally, in your terminal run "python app.py". In the javascript file you need to also run npm run build. This is all of the requirements to get the app up and running locally.


# 3 Technical issues

###
A technical issue that arose during the building process was getting the react JS file to render in my HTML. The problem was that when I clicked on my react link, I was getting a template error index.html not found. This error held me up but it was a simple fix. To fix, instead of running npm start, I was supposed to use npm run build, which then made a static folder which contained my index.html file. Another technical issue that arose during the building process was getting the react page to read the data from my database for the comments. The problem was that my data was not in a format that JSON could read hence getting the error, Comment is not JSON serializable. To fix this, I created an array that would be readable by JSON using return flask.jsonify.
The last technical issue that arose during the building process was getting the map to work in react. The error I was getting was the map was unable to retrieve undefined. To fix this, instead of having my useState variable empty, i used [] to keep the useState from being undefined.


# Hardest and Most useful
Overall the milestones have been an eye opening experience for me. The hardest part of the milestones has been working with the API's and Databases and getting them to render onto an HTML page. Starting this class, I didn't have much Python experience but through the great learning process of this class and working through the milestones, I have learned a lot. The most useful part for me has been using overall learning how to code in Python. Working on the milestones allows me to feel more confident in my coding abilites when it comes to Python. The milestones, showed me different ways to approach a problem while retriving the same end goal.