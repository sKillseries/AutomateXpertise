# AutomateExpertise

> L'assistant automatisé du Pentester

AutomateExpertise est un outil ayant pour vocation d'automatiser les phases de reconnaissance et de scan d'une cible donnée.
Dans sa version actuelle, elle effectue les différents scan de reconnaissance et d'énumération de la cible avec l'enregistrement des résultats dans un simple fichier txt.

Dans sa prochaine version, elle analysera les résulteras et chercheras par elle-même les différentes manière d'exploité les vulnérabilités, qui seront retranscrits afin que le pentester puisse essayer de prouver si la vulnérabilité a été exploitable ou non.
L'application pourra aussi générer automatiquement des KPI qui pourront être utile dans la rédaction du rapport de pentest.

L'application étant sous docker vous pouvez récupérer l'image à cet endroit: https://hub.docker.com/r/skillseries/automatexpertise

Afin de vous simplifier la tâche vous avez à votre disposition les scripts qui vous permettront de configurer automatiquement votre environnement de pentest en fonction de vos besoins.

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

### Utilisation des scripts Python

Pour installer les packages nécessaires pour l'utilisation des scripts python veuillez utiliser la commande ci-dessous:

```
pip install -r requirements.txt
```

Pour utiliser AutomateExpertise deux possibilités s'ouvre à vous:

#### En local

Dans le cas d'une utilisation sur votre machine  ou au sein de votre réseau local vous pouvez utiliser le script qui permet de configurer le réseau docker en mode macvlan, cela vous permettra de définir une adresse IP à votre conteneur qui possédera une adresse mac, ce qui lui permettra d'être reconnu comme une machine physique au sein de votre réseau. Ainsi vous utilisez différents conteneurs AutomateExpertise en simultanée sur votre machine ou sur votre réseau.

#### Sur un VPS

Dans le cas d'une utilisation d'un serveur VPS vous pouvez utiliser le script qui permet de configurer le réseau docker en mode host, dès lors elle possédera la même IP que votre serveur VPS, vous serez limité qu'à un conteneur AutomateExpertise à la fois.
