# Pocket Signal Bot 🤖

Bot Telegram pour les signaux de trading Pocket Option avec analyse technique en temps réel.

## 🚀 Fonctionnalités

- **Signaux de trading en temps réel** pour les timeframes 1m, 2m et 5m
- **Interface utilisateur interactive** avec menus en ligne
- **Système de vérification** des comptes Pocket Option
- **Analyse technique avancée**:
  - Bandes de Bollinger
  - MACD
  - RSI
  - Moyennes Mobiles
  - Bougies Heikin Ashi
- **Gestion automatique des signaux** avec filtrage des actifs OTC (payout ≥ 87%)
- **Logging complet** avec rotation des fichiers
- **Architecture asynchrone** pour hautes performances

## 📦 Installation

1. Clonez le dépôt:
```bash
git clone https://github.com/yourusername/pocket-signal-bot.git
cd pocket-signal-bot

2. Installez les dépendances:
```bash
pip install -r requirements.txt

3. Configurez le fichier . env:
env

```TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN
POCKET_SSID=YOUR_SSID
POCKET_DEMO=true

4. Lancez le bot:
```bash
python run.py
