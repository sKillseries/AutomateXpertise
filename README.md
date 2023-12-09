# AutomateExpertise

> L'assistant automatisé du Pentester

AutomateExpertise est un outil ayant pour vocation d'automatiser les phases de reconnaissance et de scan d'une cible donnée.
Dans sa version actuelle, elle effectue les différents scan de reconnaissance et d'énumération de la cible avec l'enregistrement des résultats dans un simple fichier txt.

Dans sa prochaine version, elle analysera les résultats et cherchera par elle-même les différentes manière d'exploité les vulnérabilités, qui seront retranscrits afin que le pentester puisse essayer l'exploitation ou non de la ou des vulnérabilité(s).
L'application pourra aussi générer automatiquement des KPI qui pourront être utile dans la rédaction du rapport de pentest.

L'application étant sous docker vous pouvez récupérer l'image à cet endroit: https://hub.docker.com/r/skillseries/automatexpertise

Afin de vous simplifier la tâche vous avez à votre disposition un package python qui vous permettra de configurer automatiquement votre environnement de pentest en fonction de vos besoins disponible sur Pypi: https://pypi.org/project/automatexpertise/

A noter que pour un confort optimal d'utilisation, je préconise l'usage de Linux via un poste physique ou via une VM.

Cette outil peut être un complément à Exegol qui s'utilise également avec Docker: https://exegol.readthedocs.io/en/latest/index.html

En combinant l'usage d'automatexpertise et d'exegol vous n'aurez plus jamais à reconfigurer votre machine ou VM de A à Z avant de partir effectuer un pentest chez un client, c'est un gain de temps assuré.

Pour installer Docker suivez les instructions suivantes:

### Linux

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

Afin de faciliter l'initialisation du conteneur docker, veuillez installer le wrapper automatexpertise:

```
pip install automatexpertise
```

#### Créer un conteneur

```
automatexpertise create <cible/entreprise>
```

Veuillez donner un nom qui permettra d'identifier le conteneur. Votre conteneur aura comme nom final automatexpertise-<cible/entreprise>


Ex: Pour une utilisation hackthebox réaliser la commande `automatexpertise create hackthebox` ce qui donnera automatexpertise-hackthebox


#### Lister les conteneurs

```
automatexpertise list
```

#### Démarrer un conteneur éteint

```
automatexpertise start <nomduconteneur>
```

#### Arrêter un conteneur

```
automatexpertise stop <nomduconteneur>
```

#### Supprimer un conteneur

```
automatexpertise delete <nomduconteneur>
```


