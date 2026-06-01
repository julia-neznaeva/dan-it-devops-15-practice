#!/bin/bash
set -ex
echo "DB provisioning started"

apt update
apt install mysql-server -y

sed -i '/^bind-address[[:space:]]*=/c\bind-address = 192.168.56.11' /etc/mysql/mysql.conf.d/mysqld.cnf

grep "bind-address = 192.168.56.11" /etc/mysql/mysql.conf.d/mysqld.cnf > /dev/null

systemctl restart mysql

mysql <<EOF
CREATE DATABASE IF NOT EXISTS petclinic;

CREATE USER IF NOT EXISTS 'petclinic'@'192.168.56.%'
IDENTIFIED BY 'password';

GRANT ALL PRIVILEGES
ON petclinic.*
TO 'petclinic'@'192.168.56.%';

EOF