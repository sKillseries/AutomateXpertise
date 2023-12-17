#!/bin/bash

# Récupération du nom d'hôte de la machine
hostname=$(hostname)

# Récupération de l'adresse IP de la machine
ip=$(hostname -I | awk '{print $1}')

documentroot='DocumentRoot /var/www/html/AutomateXpertise/public'

redirect="Redirect permanent / https://$ip/"

# Répertoire où seront stockés les certificats
cert_dir="/etc/ssl/certs"
cert_key="/etc/ssl/private"

# Génération du certificat auto-signé au format PEM avec OpenSSL
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout "$cert_key/automatexpertise-cert.key" -out "$cert_dir/automatexpertise-cert.pem" -subj "/C=FR/ST=State/L=City/O=sKillseries/OU=Automatexpertise/CN=$hostname" 2>/dev/null

sed -i "s/ServerName automatexpertise/ServerName $hostname/" /etc/apache2/sites-available/000-default.conf
sed -i "s|$documentroot|$redirect|" /etc/apache2/sites-available/000-default.conf
sed -i "s/ServerName automatexpertise/ServerName $hostname/" /etc/apache2/sites-available/default-ssl.conf

# Démarrage du service MariaDB
service mariadb start

# Autorisation pour le socket MySQL
chmod 755 /var/run/mysqld/mysqld.sock

# Connexion à MariaDB en tant qu'utilisateur root
mariadb -u root <<EOF
DELETE FROM mysql.global_priv WHERE User='';
DELETE FROM mysql.global_priv WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');
DROP DATABASE IF EXISTS test;
DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';
CREATE DATABASE automatexpertise;
GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' IDENTIFIED VIA mysql_native_password WITH GRANT OPTION;
FLUSH PRIVILEGES;
EOF

# Exécution des migrations Laravel
cd /var/www/html/AutomateXpertise || exit
php artisan migrate:install
php artisan migrate

# démarrage apache2
apache2ctl -D foreground 2>/dev/null