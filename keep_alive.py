from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot sedang berjalan!"

def run():
    # Render biasanya kasih port di environment variable, atau default 8080
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()