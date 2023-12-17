#!/bin/bash

# Démarrage du service MariaDB
service mariadb start

# Autorisation pour le socket MySQL
chmod 755 /var/run/mysqld/mysqld.sock

# démarrage apache2
apache2ctl -D foreground 2>/dev/null