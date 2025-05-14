from flask import Flask, request, jsonify
import base64
from html2image import Html2Image

app = Flask(__name__)

# Use default wkhtmltoimage renderer by not specifying a browser
# Optionally specify the executable path
hti = Html2Image(executable='/usr/bin/wkhtmltoimage')

@app.route('/screenshot', methods=['POST'])
def take_screenshot():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({"error": "URL is required"}), 400

    filename = "screenshot.png"
    hti.screenshot(url=url, save_as=filename)
    with open(filename, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return jsonify({"screenshot": encoded_string})
