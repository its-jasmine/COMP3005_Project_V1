# COMP3005_Project_V1

## Overview
Design a database that stores a soccer events dataset spanning multiple competitions and seasons

## Authors
| Author | Student Number | Email |
|----------|----------|----------|
|Jasmine Gad El Hak | 101181201 | jasminegadelhak@cmail.carleton.ca|
|Nivetha Sivasaravanan | 101182962 | nivethasivasaravanan@cmail.carleton.ca|
|Victoria Malouf | 101179986 | victoriamalouf@cmail.carleton.ca|

## File Organization
### json_loader
Directory that stores source code that maps and loads JSON files into the DB

- **helper_scripts:** Directory that stores scripts that generate DDL (Data Definition Language) and DML (Data Manipulation Language) SQL files for the DB
- **statsbomb_data:** Includes all data relating to La Liga seasons 2018/2019, 2019/2020, 2020/2021, and Premier League season 2003/2004. (https://github.com/statsbomb/open-data/tree/0067cae166a56aa80b2ef18f61e16158d6a7359a)

### dbexport.sql
- file produced by pg_dump that can be used to import the DB
  
### queries.py
- queries 1-10

## Entity Relationship Diagram
![image](https://github.com/its-jasmine/COMP3005_Project_V1/assets/84146479/562f5537-6c39-4470-b714-a341cbc24895)

## Database Schema Diagram
![image](https://github.com/its-jasmine/COMP3005_Project_V1/assets/84146479/b75f2de5-b21c-4cd6-be51-9bae34dcffd4)


