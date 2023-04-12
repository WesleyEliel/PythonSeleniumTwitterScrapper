# PythonSeleniumTwitterScrapper

## Table of contents
* [General info](#info)
* [Technologies](#technologies)
* [Prepare Env](#prepare-env)
* [Setup](#setup)

## Info

A project about scrapping an user tweets from Twitter.

Actually the project work only for user medias, images files for the moment. 

Next Step wil be handling videos files, and offer possibility to user to choose what kind of data they want

Video Step Archived
	
## Technologies
This Project is based on:
* twitter-scraper-selenium version: 4.1.4
* selenium version: 4.7.0
## Prepare Env
* Create an .env.master file with, and add this attrs USERNAME, PASSWORD [Twitter]
* Add the username of the user you want to scrapp data to .env.master with MODEL attr

## Setup
To run this project, install it locally using npm:

```
$ cd ../{BaseDir}
$ pipenv shell
$ pipenv install
$ python main.py
```