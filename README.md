# Bot Discord en Python

# Requirement
discord.py==2.3.2
python-dotenv==1.0.0 

Un bot Discord simple créé avec discord.py qui répond à plusieurs commandes basiques, de modération, de divertissement et de sécurité.

## Installation

1. Installez les dépendances requises :
```bash
pip install -r requirements.txt
```

2. Créez un fichier `.env` à la racine du projet et ajoutez votre token Discord :
```
BOT_TOKEN=votre_token_ici
```

## Commandes disponibles

### Commandes générales
- `!hello` : Le bot vous salue
- `!ping` : Vérifie la latence du bot
- `!info` : Affiche des informations sur le serveur

### Commandes de modération
- `!ban <membre> [raison]` : Bannir un membre du serveur
- `!unban <id_membre>` : Débannir un membre du serveur
- `!warn <membre> [raison]` : Avertir un membre
- `!warns <membre>` : Voir les avertissements d'un membre
- `!mute <membre> [durée]` : Mettre en sourdine un membre (durée en minutes, défaut: 10)
- `!unmute <membre>` : Retirer la sourdine d'un membre
- `!blacklist <membre> [raison]` : Mettre un membre sur liste noire
- `!unblacklist <membre>` : Retirer un membre de la liste noire

### Commandes de divertissement
- `!roll [NdM]` : Lance des dés (ex: !roll 2d6)
- `!choose <option1, option2, ...>` : Choisit aléatoirement parmi plusieurs options
- `!poll <question> <option1> <option2> ...` : Crée un sondage avec des réactions
- `!8ball <question>` : Pose une question au bot
- `!reverse <texte>` : Inverse le texte donné
- `!ascii <texte>` : Convertit le texte en art ASCII
- `!countdown <secondes>` : Démarre un compte à rebours
- `!randomcolor` : Génère une couleur aléatoire
- `!flip` : Lance une pièce
- `!rps <pierre/papier/ciseaux>` : Joue à pierre, papier, ciseaux
- `!quote` : Affiche une citation aléatoire

### Commandes de sécurité
- `!lockdown` : Active le mode lockdown sur un canal
- `!unlock` : Désactive le mode lockdown
- `!raidcheck` : Vérifie les membres en quarantaine
- `!config <paramètre> <valeur>` : Configure les paramètres de sécurité
- `!setautorole <rôle>` : Définit le rôle automatique pour les nouveaux membres
- `!setwelcome <canal>` : Définit le canal de bienvenue

### Protection automatique
- Anti-raid : Détecte et gère automatiquement les raids
- Anti-spam : Protège contre le spam de messages
- Anti-mentions : Limite le nombre de mentions par message
- Anti-emojis : Limite le nombre d'emojis par message
- Anti-caps : Limite le pourcentage de majuscules

### Paramètres de sécurité configurables
- `raid_threshold` : Nombre de joins avant activation de l'anti-raid
- `raid_timeframe` : Fenêtre de temps pour la détection de raid
- `spam_threshold` : Nombre de messages avant détection de spam
- `spam_timeframe` : Fenêtre de temps pour la détection de spam
- `max_mentions` : Nombre maximum de mentions par message
- `max_emojis` : Nombre maximum d'emojis par message
- `max_caps` : Pourcentage maximum de majuscules

## Permissions requises
- Pour les commandes de ban/unban : Permission "Bannir des membres"
- Pour les commandes warn/mute : Permission "Expulser des membres"
- Pour les commandes blacklist et sécurité : Permission "Administrateur"

## Comment obtenir un token Discord

1. Allez sur [Discord Developer Portal](https://discord.com/developers/applications)
2. Cliquez sur "New Application"
3. Donnez un nom à votre application
4. Allez dans la section "Bot"
5. Cliquez sur "Add Bot"
6. Copiez le token et collez-le dans votre fichier `.env`

## Lancer le bot

```bash
python bot.py
``` 
