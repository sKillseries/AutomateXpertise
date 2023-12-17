### Utilisation du wrapper Python

#### Installation du wrapper

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

