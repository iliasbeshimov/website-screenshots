from html2image import Html2Image
from flask import Flask, request, jsonify
import os
import base64

app = Flask(__name__)
hti = Html2Image(output_path='.', custom_flags=['--no-sandbox', '--disable-gpu', '--virtual-time-budget=10000'])

@app.route('/screenshot', methods=['POST'])
def take_screenshot():
    try:
        # Get URL from the POST request (sent by Make.com)
        data = request.get_json()
        url = data.get('url')
        if not url:
            return jsonify({'error': 'No URL provided'}), 400

        # Generate a unique filename
        filename = f"screenshot_{url.replace('http://', '').replace('https://', '').replace('/', '_')}.png"
        output_path = os.path.join('.', filename)

        # Take screenshot using html2image
        hti.screenshot(url=url, save_as=filename)

        # Read the image and convert to base64
        with open(output_path, 'rb') as image_file:
            image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

        # Delete the temporary file
        os.remove(output_path)

        # Return the base64 string
        return jsonify({'message': 'Screenshot generated', 'image_base64': image_base64}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
