# keep_alive.py
import os
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Le bot est en ligne !", 200

def run():
    port = int(os.environ.get("PORT", 8080))
    # Écoute bien sur 0.0.0.0, port dynamique ou 8080 par défaut
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()
