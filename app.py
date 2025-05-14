import os
from flask import Flask, request, jsonify
from html2image import Html2Image

app = Flask(__name__)
hti = Html2Image()

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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
