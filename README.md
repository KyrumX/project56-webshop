# Project 5-6: Developing a web application

### Made by
Aaron Beetstra **Lead developer**<br/>
Selim Aydi<br/>
Ralph Verburg<br/>
Jasper Wijnhoven<br/>
Ryan Wilson<br/>

------
### How to run
The following instruction specify how to run this project on different platforms.

#### Production

The following instructions are for a production mode of operation. This means no errors like routing errors are shown, instead a 404 page is returned. <br/><br/>

**Setup** <br/>
_Please not that the versions provided are the ones used for testing, no other version, like Django 2.0, have been tested._ <br/>
In order to run the latest version you require the following: <br/><br/>
* Python 3.6<br/>
* Django 1.11 <br/>
* psycopg2 2.7.3.2<br/>
* django-graphos 0.3.41<br/>

_An internet connection and database connection are required for optimal use._


##### Windows / Local

**Running**
1. Clone the master branch from this repository;
2. Extract the files to prefered location;
3. Open a console in the first website folder, the one with the manage.py file;
4. Run the following command: `python manage.py runserver --insecure`
5. Open a Google Chrome and go to the following link (default): `127.0.0.1:8000`


##### Ubuntu (external host)
1. Follow the Windows instruction up to step 4.
2. In the console, run the following command: `sudo python3 manage.py 0.0.0.0:port --insecure`
3. Either open a local browser and go to the ip address associated with your server or user another computer to go to that address.


