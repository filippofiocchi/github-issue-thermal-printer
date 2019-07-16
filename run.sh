#!/bin/sh
cd /home/pi/github-issue-thermal-printer
PATH=/usr/local/bin:$PATH
export TOKEN_GITHUB='your github token'
export TOKEN_BITLY='your bitlytoken'
export DATABASE_NAME='the name of your database'
export NAME_ORGANIZZATION='the name of the organizzation on github'
echo $(date) > tmp.txt
/usr/local/bin/pipenv run python printer.py > error.txt 2>error2.txt
