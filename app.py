import os

from flask import Flask, request, render_template_string

from google import genai

app = Flask(name)

API_KEY = os.environ.get("GEMINI_API_KEY")

HTML_TEMPLATE = """

<!DOCTYPE html>

<html>

<head>

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>iPhone 4 AI</title>

<style>

body { font-family: sans-serif; padding: 10px; background: #f0f0f0; }

.box { background: white; padding: 15px; border-radius: 8px; }

textarea { width: 95%; height: 80px; font-size: 16px; }

input[type="submit"] { padding: 12px; font-size: 16px; width: 100%; background: #007aff; color: white; border: none; }

.response { margin-top: 15px; background: #eef; padding: 10px; white-space: pre-wrap; }

</style>

</head>

<body>

<div class="box">

<h2>iPhone 4 AI Helper</h2>

<form method="POST" enctype="multipart/form-data">

<label>Prompt:</label>



<textarea name="prompt" required></textarea>





<label>Photo (Optional):</label>



<input type="file" name="image" accept="image/*">





<input type="submit" value="Send to AI">

</form>

{% if response_text %}

<hr>

<h3>Answer:</h3>

<div class="response">{{ response_text }}</div>

{% endif %}

</div>

</body>

</html>

"""

@app.route('/', methods=['GET', 'POST'])

def home():

response_text = None

if request.method == 'POST':

prompt_text = request.form.get('prompt', '')

uploaded_file = request.files.get('image')

try:

client = genai.Client(api_key=API_KEY)

contents = []

if uploaded_file and uploaded_file.filename != '':

image_bytes = uploaded_file.read()

mime_type = uploaded_file.mimetype or 'image/jpeg'

contents.append({'mime_type': mime_type, 'data': image_bytes})

contents.append(prompt_text)

res = client.models.generate_content(

model='gemini-2.5-flash',

contents=contents

)

response_text = res.text

except Exception as e:

response_text = f"Error: {str(e)}"

return render_template_string(HTML_TEMPLATE, response_text=response_text)

if name == 'main':

port = int(os.environ.get('PORT', 5000))

app.run(host='0.0.0.0', port=port)
