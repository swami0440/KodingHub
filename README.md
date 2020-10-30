# KodingHub
This application is created for POC's
 heroku logs --tail
 
 git add .
 git commit -am "added gunicorn server"
 git push heroku master
 
 sudo heroku git:clone -a kodinghub
 
 heroku db:pull sqlite:///database.db
 
heroku config --app kodinghub
Access Credentials
Username:	b39d11e9fe9bb9
Password:	284f46990974059 (Reset)
mysql://b39d11e9fe9bb9:284f46990974059@us-cdbr-east-02.cleardb.com/heroku_df998aa187223ac?reconnect=true