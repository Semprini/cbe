# cbe
Django app for controlling cross industry Common Business Entities

[![Build Status](http://circleci-badges-max.herokuapp.com/img/Semprini/cbe?token=f5c87c28c73b5351e837a0769c4f8886f4af3314)](https://circleci.com/gh/Semprini/cbe/)

CBE is a realization of a cross industry standard data model. The app provides RESTful CRUD and administration for common business entities.

Sources: TM Fourum SID (Telco), IBM IFW (Finance/Banking), IAA (Insurance)

Entity Domains:
    Party - Entities relating to individuals and organizations and the roles they play
    Location - Entities for addresses and places

The data model is designed to be extended for each industry. PartyRole is the main abstract entity which concrete classes should be derived.

