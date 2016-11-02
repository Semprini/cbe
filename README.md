# cbe
Cross industry Common Business Entities

[![Build Status](http://circleci-badges-max.herokuapp.com/img/Semprini/cbe?token=f5c87c28c73b5351e837a0769c4f8886f4af3314)](https://circleci.com/gh/Semprini/cbe/)

CBE is a realization of a cross industry standard data model. The app provides RESTful CRUD and administration for common business entities persisted on a relational DB.

Sources: TM Fourum SID (Telco), IBM IFW (Finance/Banking), IAA (Insurance)

To run:
- clone repo
- python manage.py migrate (will use a default sqllite db)
- python manage.py createsuperuser
- python manage.py runserver
- browse to http://localhost:8000/admin for the admin interface
- browse to http://localhost:8000/api for the api interface

Entity Domains:
- Party - Entities relating to individuals, organizations, how to contact them and the roles they play
- Location - Entities for addresses and places
- Business interaction - Entities for how parties interact in the business
- ...more to come

![Party](https://github.com/Semprini/cbe/blob/master/docs/classParty.png)
![Party](https://github.com/Semprini/cbe/blob/master/docs/classLocation.png)
![Party](https://github.com/Semprini/cbe/blob/master/docs/classBusinessInteraction.png)

The data model is designed to be extended for each industry. In Party, the PartyRole class is the main abstract entity from which concrete classes like Customer or Supplier should be derived.

