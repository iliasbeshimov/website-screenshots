from quart import Quart, request, jsonify
from playwright.async_api import async_playwright
import base64

app = Quart(__name__)

# Explicitly set the PROVIDE_AUTOMATIC_OPTIONS configuration
app.config['PROVIDE_AUTOMATIC_OPTIONS'] = True

@app.route('/screenshot', methods=['POST'])
async def take_screenshot():
    data = await request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({"error": "URL is required"}), 400

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        screenshot = await page.screenshot()
        await browser.close()

    encoded_string = base64.b64encode(screenshot).decode('utf-8')
    return jsonify({"screenshot": encoded_string})
