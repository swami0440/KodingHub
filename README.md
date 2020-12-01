# KodingHub
This application is created for POC's
 heroku logs --tail
 
 git add .
 git commit -am "added gunicorn server"
 git push heroku master
 
 sudo heroku git:clone -a kodinghub
 
 heroku db:pull sqlite:///database.db
 
heroku config --app kodinghub
