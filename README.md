# AutomateXpertise

> L'assistant automatisé du Pentester

AutomateXpertise est un outil ayant pour vocation d'automatiser les phases de reconnaissance et de scan d'une cible donnée.
Dans sa version actuelle, elle effectue les différents scan de reconnaissance et d'énumération de la cible avec l'enregistrement des résultats dans un simple fichier txt.

Dans sa prochaine version, elle analysera les résultats et cherchera par elle-même les différentes manière d'exploité les vulnérabilités, qui seront retranscrits afin que le pentester puisse essayer l'exploitation ou non de la ou des vulnérabilité(s).
L'application pourra aussi générer automatiquement des KPI qui pourront être utile dans la rédaction du rapport de pentest.

L'application étant sous docker vous pouvez récupérer l'image à cet endroit: https://hub.docker.com/r/skillseries/automatexpertise (cependant inutile de le faire à la main car le package python le fait de façon automatique).

Afin de vous simplifier la tâche vous avez à votre disposition un package python qui vous permettra de configurer automatiquement votre environnement de pentest en fonction de vos besoins disponible sur Pypi: https://pypi.org/project/automatexpertise/

A noter que pour un confort optimal d'utilisation, je préconise l'usage de Linux via un poste physique ou via une VM.

Cette outil peut être un complément à Exegol qui s'utilise également avec Docker: https://exegol.readthedocs.io/en/latest/index.html

En combinant l'usage d'automatexpertise et d'exegol vous n'aurez plus jamais à reconfigurer votre machine ou VM de A à Z avant de partir effectuer un pentest chez un client, c'est un gain de temps assuré.

---

### Configuration nécessaire

Pour installer Docker suivez les instructions suivantes:

#### Installation de docker

```
curl -fsSL "https://get.docker.com/" -o get-docker.sh
sh get-docker.sh
```

#### Permissions docker

```
# add the sudo group to the user
sudo usermod -aG docker $(id -u -n)

# "reload" the user groups with the newly added docker group
newgrp docker
```

---

### Utilisation du wrapper Python

Afin de faciliter l'initialisation du conteneur docker, veuillez installer le wrapper automatexpertise.

Pour cela il vous faudra d'abord installer python

#### Installation de Python

```
sudo apt install python3
```

#### Installation de pip

```
sudo apt install python3-pip
```

#### Installation de pipx

```
# install pipx from system package:
sudo apt update && sudo apt install pipx

# install from pip method 1
python3 -m pip install pipx

# install from pip method 2
pip install pipx
```

#### Installation du package automatexpertise

```
# Installation via pipx (preferred)
pipx install automatexpertise

# Installation via pip
pip install automatexpertise
```

#### Ajout AutomateXpertise dans le PATH

##### if installed via pipx

```
pipx ensurepath
```

##### If installed via pip

``` 
export PATH=~/.local/bin:$PATH
```


/!\ Nota Bene: Le package automatexpertise ne fonctionne que sous Linux (le mode macvlan n'étant pas disponible sous Windows, n'ayant pas de mac je n'ai pu effectué aucun test sur MacOS).

#### Créer un conteneur

```
automatexpertise create <cible/entreprise>
```

Veuillez donner un nom qui permettra d'identifier le conteneur. Votre conteneur aura comme nom final automatexpertise-<cible/entreprise>.

Ex: Pour une utilisation hackthebox réaliser la commande `automatexpertise create hackthebox` ce qui donnera automatexpertise-hackthebox.

La fonction create va récupérer automatiquement la dernière version de l'image docker et créer votre conteneur afin qu'il soit utilisable.


#### Lister les conteneurs

```
automatexpertise list
```

La fonction list va lister tout les conteneurs commençant par "automatexpertise-" et les triés en fonction de leurs états (Actif ou Inactif).

#### Démarrer un conteneur éteint

```
automatexpertise start <nomduconteneur>
```

La fonction start permet de démarrer un conteneur étant dans un état inactif. Il vous faudra taper la commande avec le nom complet du conteneur ex: `automatexpertise start automatexpertise-hackthebox`.

#### Arrêter un conteneur

```
automatexpertise stop <nomduconteneur>
```

La fonction stop permet d'arrêter un conteneur. Il vous faudra taper la commande avec le nom complet du conteneur ex: `automatexpertise stop automatexpertise-hackthebox`.

#### Supprimer un conteneur

```
automatexpertise delete <nomduconteneur>
```

La fonction delete permet de supprimer définitivement un conteneur. Il vous faudra taper la commande avec le nom complet du conteneur ex: `automatexpertise delete automatexpertise-hackthebox`.

Cela vous permetta dans le cas d'un nouveau pentest pour la même entreprise cliente de récréer un conteneur avec le même nom.

---

### Utilisation du conteneur

#### Comment se connecter à un conteneur

Pour se connecter à un conteneur vous pouvez utiliser ssh via la commande:

```
ssh -p 2222 root@ipconteneur
```

Le mot de passe par défaut est `kali` vous pouvez le changer avec la commande `chpasswd`.

Dans le cas où vous créez un nouveau conteneur avec une ip qui a déjà été utilisé auparavant il vous faudra utiliser la commande:

```
ssh-keygen -f "~/.ssh/known_hosts" -R "[ipconteneur]:2222"
```

#### Initialisation des services

Au démarrage du conteneur seul le service ssh sera actif.

Afin que l'application web soit utilisable après la création du conteneur (`automatexpertise create`) il faudra vous connecter à celui-ci et taper la commande: `/usr/local/bin/init-services.sh`.

Une fois cela fait vous pourrez vous connecter sur l'interface web d'AutomateXpertise à l'adresse `https://<ipconteneur>`.

#### Démarrage des services

Lorsque vous démarrez le conteneur (`automatexpertise start`) il faudra vous connecter à celui-ci et taper la commande: `/usr/local/bin/start-services.sh`.

Une fois cela fait vous pourrez vous connecter sur l'interface web d'AutomateXpertise à l'adresse `https://<ipconteneur>`.

---

### Se connecter sur l'interface web

Pour se connecter dans l'application web les identifiants par défauts sont:

Login: `admin@automatexpertise.local`

Mot de passe: `Autom@teXpert1$e`

Rendez-vous dans la liste déroulante avec le nom d'utilisateur `admin`, cliquez sur `Profile` et vous pourrez modifier le mot du compte par défaut.

#### Créer un compte utilisateur

Pour créer un compte utilisateur, dans la liste déroulante avec le nom d'utilisateur `admin`, cliquez sur `Register`, remplissez le formulaire et cliquez sur Register.

Vous pourrez vous déconnecter et vous connectez avec le nouveau compte utilisateur.

Tous les comptes créés auront accès aux mêmes données, cela permet de travailler en équipe sur le même test d'intrusion sans devoir faire de transfert de fichiers.
