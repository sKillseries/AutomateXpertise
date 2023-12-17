# Utilisation de l'image kali linux de base
FROM kalilinux/kali-rolling

# Mise a jour du système de base
RUN apt-get update && apt-get upgrade -y

# Installation des packages Apache, PHP, SSH, Git et NPM
RUN apt-get install -y apache2 mariadb-server
RUN apt-get install -y php8.2 libapache2-mod-php8.2 php8.2-mbstring php8.2-xml php8.2-zip php8.2-mysql
RUN apt-get install -y openssh-server git
RUN apt-get install -y npm

# Installation des outils nécessaires
RUN apt-get install -y nmap dnsrecon nbtscan samba-common-bin impacket-scripts enum4linux masscan
RUN apt-get install -y curl hakrawler assetfinder amass httprobe subjack wafw00f nikto wapiti
RUN apt-get install -y python3-pip golang-go
RUN apt-get install -y openvpn
RUN pip3 install droopescan

# Installation de composer
RUN php8.2 -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
RUN php8.2 composer-setup.php --install-dir=bin --filename=composer
RUN php8.2 -r "unlink('composer-setup.php');"

# Activation module Apache (nécessaire pour Laravel)
RUN a2enmod php8.2
RUN a2enmod rewrite
RUN a2enmod ssl
RUN a2ensite default-ssl
RUN a2enmod headers
RUN a2enmod http2

# Installation script démarrage mariadb et apache2
COPY init-services.sh /usr/local/bin/
COPY start-services.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/init-services.sh
RUN chmod +x /usr/local/bin/start-services.sh

# Exposition ports Apache et SSH
EXPOSE 80
EXPOSE 443
EXPOSE 2222

# Récupération AutomateXpertise
RUN rm /var/www/html/index.html
RUN git clone https://github.com/sKillseries/AutomateXpertise-Webapp.git /var/www/html/AutomateXpertise
COPY 000-default.conf /etc/apache2/sites-available/000-default.conf
COPY default-ssl.conf /etc/apache2/sites-available/default-ssl.conf
WORKDIR /var/www/html/AutomateXpertise
RUN rm .gitignore
RUN rm .gitattributes
RUN rm -rf .git
RUN rm -rf tests
RUN composer install --no-dev
RUN npm install
RUN npm run build
RUN mv .env.example .env
RUN php artisan key:generate
RUN php artisan storage:link
RUN php artisan config:cache
RUN php artisan route:cache
RUN php artisan optimize
RUN chown -R www-data:www-data /var/www/html/AutomateXpertise

# Configuration Apache2
RUN sed -i 's/ServerTokens OS/ServerTokens Prod/' /etc/apache2/conf-available/security.conf
RUN sed -i 's/ServerSignature On/ServerSignature Off/' /etc/apache2/conf-available/security.conf
RUN echo 'Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"' >> /etc/apache2/conf-available/security.conf
RUN echo 'Header set X-XSS-Protection "1; mode=block"' >> /etc/apache2/conf-available/security.conf
RUN echo 'Header always append X-Frame-Options SAMEORIGIN' >> /etc/apache2/conf-available/security.conf

# Configuration SSH
RUN mkdir /var/run/sshd
RUN echo 'root:kali' | chpasswd
RUN sed -i 's/#LoginGraceTime 2m/LoginGraceTime 2m/' /etc/ssh/sshd_config
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/#MaxAuthTries 6/MaxAuthTries 5/' /etc/ssh/sshd_config
RUN sed -i 's/#MaxSessions 10/MaxSessions 10/' /etc/ssh/sshd_config
RUN sed -i 's/#Port 22/Port 2222/' /etc/ssh/sshd_config
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config
RUN sed -i 's/#PermitEmptyPasswords no/PermitEmptyPasswords no/' /etc/ssh/sshd_config

# Démarrage du service ssh
CMD ["/usr/sbin/sshd", "-D"]