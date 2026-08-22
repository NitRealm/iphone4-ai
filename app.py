import os
from flask import Flask, request
from google import genai
from PIL import Image

app = Flask(__name__)

API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY) if API_KEY else None

HTML_TEMPLATE = '<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Gemini Mobile</title><style>body{font-family:sans-serif;margin:10px;padding:0;background:#f0f0f0;}form{background:#fff;padding:10px;border-radius:5px;}textarea{width:95%;height:60px;margin-bottom:10px;}input[type=file]{margin-bottom:10px;}input[type=submit]{width:100%;padding:10px;background:#007bff;color:#fff;border:none;border-radius:3px;font-size:16px;}.result{margin-top:15px;background:#fff;padding:10px;border-radius:5px;white-space:pre-wrap;}</style></head><body><h3>Gemini Mobile</h3><form method="POST" enctype="multipart/form-data"><textarea name="prompt" placeholder="Ask something..." required></textarea><br><input type="file" name="image" accept="image/*"><br><input type="submit" value="Send"></form>{result_html}</body></html>'

@app.route("/", methods=["GET", "POST"])
def index():
    result_html = ""
    if request.method == "POST":
        if not client:
            result_html = '<div class="result"><strong>Error:</strong> GEMINI_API_KEY is not set.</div>'
        else:
            prompt = request.form.get("prompt", "")
            image_file = request.files.get("image")
            contents = [prompt]
            
            if image_file and image_file.filename != "":
                try:
                    img = Image.open(image_file.stream)
                    contents.append(img)
                except Exception as e:
                    result_html = f'<div class="result"><strong>Image Error:</strong> {e}</div>'
            
            if not result_html:
                try:
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=contents
                    )
                    result_html = f'<div class="result"><strong>Response:</strong><br>{response.text}</div>'
                except Exception as e:
                    result_html = f'<div class="result"><strong>API Error:</strong> {e}</div>'
                    
    return HTML_TEMPLATE.format(result_html=result_html)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
