#!/usr/bin/env bash
sudo service mysql start
cat db_env.sql | sudo mysql
