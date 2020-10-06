#!/bin/bash

# Read Inputs from Command Line
unset MYSQL_USER
unset MYSQL_PASS
unset MYSQL_DB_NAME

read -p 'MySQL USERNAME: ' MYSQL_USER
read -sp 'MySQL PASSWORD: ' MYSQL_PASS
echo
read -p 'MySQL Database Name: ' MYSQL_DB_NAME

# Create new MYSQL database
WHICH_MYSQL=$(which mysql)

if ! mysql -u$MYSQL_USER -p$MYSQL_PASS -e "use $MYSQL_DB_NAME"; then
    SQL="CREATE DATABASE IF NOT EXISTS $MYSQL_DB_NAME;"
    $WHICH_MYSQL -u$MYSQL_USER -p$MYSQL_PASS -e "$SQL";
fi

# Initial Database
WHICH_PYTHON=$(which python)

# Create `$MYSQL_DB_NAME` database
$WHICH_PYTHON manage.py init-db

# Initial Admin User
$WHICH_PYTHON manage.py init-admin

# Initial Uncategorized Category
$WHICH_PYTHON manage.py init-category

# Initial Hello World Post
$WHICH_PYTHON manage.py init-post
