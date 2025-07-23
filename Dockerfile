# On part d'une image Python (Debian-based) qui contient déjà audioop
FROM python:3.11-slim

# On définit le dossier de travail
WORKDIR /app

# Copie du fichier des dépendances
COPY requirements.txt .

# Installation des dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copie de tout ton code
COPY . .

# Commande pour démarrer ton bot
CMD ["python", "main.py"]
