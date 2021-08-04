# LOGIN SYSTEM
this is task for Fenix Networks Limited </br>
This project is done using python flask framework and mongo as a backend database

#Pre requisite
Python,Flask,MongoDB
#How to Run
cd to the simple_login_app directory
type following command<br>
python app.py<br>
go to postman and add new request at 
http://127.0.0.1:5000
#Task Detail
<b>/Sign<br></b>
METHOD-> POST<br>
This endpoint takes 2 required field<br>
email and password <br>
any of one missing will return error<br>
create a new user with given password
if user already created then in case of wrong password it return response with user already exist and if password is correct it login the user and return userid and session key that is used in other calls</br> 
other info you provide is stored is user db

<b>/login<br></b>
METHOD-> POST<br>
This endpoint takes 2 required field<br>
email and password <br>
if user don't exist it return no user fond<br>
if it exists then in case of wrong password it return response with Wrong login attempt and if password is correct it log in the user and return userid and session key that is used in other calls</br> 
other info you provide is stored is user db

<b>/get_user/{user_id}<br></b>
METHOD-> GET<br>
it return the data stored in user in call of sign_in except the sensitive data<br>
it require x-access-token in header with value of session key return by login or signup call
the session key is expirable and expiry time can be configure using config/project_config.py

#DB
In DB the password is stored in form of hash to ensure security and session key is also stored in bytes

#Architecture
Thr project follows the MVC Architecture having separate models controller and views for user.
the DB interact with Model while, views define entry points for different routes while controller contain business logic

#Unit Test
unittest can be run by following command<br>
python -m unittest -v test\test_user.py
