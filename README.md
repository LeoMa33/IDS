# IDS | Python

## 📌 Sommaire
1. [Description du Projet](#📋-description)
2. [Fonctionnalités](#🌟-fonctionnalités)
3. [Installation](#🛠️-installation)
4. [Utilisation](#💻-utilisation)

## 🎯 Badges

[![Compatible Linux](https://img.shields.io/badge/Compatible-Linux-red.svg)](https://www.ibm.com/docs/fr/aix/7.3?topic=protocol-tcpip-protocols)
[![Langage Python](https://img.shields.io/badge/Langage-Python-blue.svg)](https://www.python.org)

## 📋 Description

Ce projet est un IDS est lié à une API qui permet de vérifier si l'état des fichiers est le même depuis la dernière sauvegarde réaliser depuis l'invite de commande, dans le cas contraire, l'ids a la possibilité d'envoyer une alerte sur discord si le lien d'un webhook a était renseigné par l'utilisateur.

## 🌟 Fonctionnalités

- Sauvegarde de l'état des fichiers/dossiers à surveiller

- Vérification de l'état des fichiers/dossiers à surveiller

- Envoie d'alerte en cas de différences entre la sauvegarde et la vérification

- Sauvegarde des rapports

- Utilisation par API


## 🛠️ Installation

```bash
pip install flask
pip install discord-webhook

git clone git@gitlab.com:_LeoM/ids.git
```

## 💻 Utilisation

### Modification de la configuration IDS

```json
{
    "discord_webhook":"<DiscordWebHook>",
    "logFile":"ids.log",
    "buildFile":"db.json",
    "reportsFolder":"reports",
    "toCheck":[
        "<FileToCheck>",
        "<FileToCheck>"
    ]
}
```

| Entrée  | Valeur |
| :--------------- | -----:|
| **\<DiscordWebHook>** | Renseigner le liens du [WebHook](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) de votre discord. |
| **\<FileToCheck>** | Renseigner le chemin vers un fichier/dossier à observer. |



### Utilisation de l'IDS CLI :

```bash
py ids <parametre>
```

| Paramètre  | Fonctionalité |
| :--------------- | -----:|
| **--build** | Créer un sauvegarde d'état dans le fichier renseigner en valeur de la clef ```buildFile``` du fichier ```conf.json```. |
| **--check** | Réalise une vérification de l'état des fichiers/dossiers à surveiller et sauvegarde le rapport dans le fichier ```check.json``` présent dans le dossier renseigner en valeur de la clef ```reportsFolder``` du fichier ```conf.json```. |

### Utilisation de l'IDS via l'API :

#### Lancement de l'API :

```bash
py ids-api.py
```

L'api se lance automatiquement sur le port ```80``` de votre machine.

#### Utilisation de l'API :

| Action  | Type de Requête | Chemin de la Requête |
| :- | :-| :-|
| Réaliser une vérification d'état | ```POST``` | /check |
| Récupération de tous les rapports | ```GET``` | /reports |
| Récupération d'un rapport par son ID | ```GET``` | /reports/<id_rapport> |
