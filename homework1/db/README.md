# Design a database for a ChatGPT app

## Tasks:
Imagine that you are building a ChatGPT app that allows users to ask questions and receive answers from the app.

1. Design a database using MySQL to store the questions and answers exchanged between users and the app.

2. Create a table for the questions with the following fields: id (Primary Key, Auto Increment), user_id (Foreign Key referencing the Users table), question, and timestamp.

3. Create a table for the answers with the following fields: id (Primary Key, Auto Increment), question_id (Foreign Key referencing the Questions table), answer, and timestamp.

4. Create a table for the users, with the following fields: id (Primary Key, Auto Increment), username, password, and email.

## Answer:
TODO: you need to add your sql query to each task here.

CREATE DATABASE IF NOT EXISTS chatgpt;
use chatgpt;

create table if not exists users (
  id int auto_increment,
  username varchar(15),
  password varchar(15),
  email varchar(20),
  primary key(id)
);

create table if not exists conversations (
  id int auto_increment,
  user_id int,
  question varchar(200),
  answer varchar(200),
  timestamp char(10),
  primary key(id),
  constraint question_fk1 foreign key (user_id) references users(id)
);