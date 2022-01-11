# Corona 4 you

"big data engineer" - naya college 2021 - final project

author: Guy Avraham.

project name:
corona 4 u

consept:
this system will help a user to locate the nearest and less crowded corona test station 
based upon the address that the user will send to the system using the telegram bot network

how:
the system uses 3 databases for achieving this goal
1. the database of locations of cellular antennas, and
2. the database of locations of "pikud ha oref" corona test stations
3. the database of cellphone used to connect to cell towers

the system is:
1. comparing the antennas locations and the location of the user to the location of the corona test stations 
2. selecting the less occupide station ( based upon the number of cellphone connected the nearest cell site in the last 30 min )
3. sending the address back to the telegram user.

in addition we are saving logs of events and backing up files / logs / data to the cloud.
several parts of this project are served as a web service, via API interfaces we wrote.


technologies used:
in the project we used the following technologies:
* python
* spark
* kafka
* telegram
* web scrapping
* airflow
* GCP
* mongoDB
* web services
* impala
* powerBI
* mongodb compass
* git
* public API's 
* private API's
* computing platform is raspberry pi 4




