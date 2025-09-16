from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# HTML template
HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Weather App</title>
    <style>
      body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; background: #f0f8ff; }
      input { padding: 10px; width: 250px; font-size: 16px; }
      button { padding: 10px 15px; font-size: 16px; cursor: pointer; }
      .result { margin-top: 20px; font-size: 18px; color: #333; }
      .error { color: red; }
    </style>
  </head>
  <body>
    <h1>Weather App</h1>
    <form method="POST">
      <input name="city" placeholder="Enter city (e.g., Dhaka or Dhaka,BD)" required>
      <button type="submit">Get Weather</button>
    </form>
    {% if result %}
      <div class="result">{{ result|safe }}</div>
    {% endif %}
  </body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    if request.method == "POST":
        city = request.form.get("city").strip()
        api_key = "84d90302884f86fc2c2a1ec93191c52b"  # Your API key
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        try:
            response = requests.get(url)
            data = response.json()
            if response.status_code == 200:
                temp = data['main']['temp']
                description = data['weather'][0]['description']
                result = f"<b>{city}</b><br>Temperature: {temp}°C<br>Description: {description}"
            else:
                result = f"<span class='error'>Error: {data.get('message', 'City not found')}</span>"
        except requests.exceptions.RequestException:
            result = "<span class='error'>Network error. Check your connection.</span>"
    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == "__main__":
    # Required for Replit hosting
    app.run(host="0.0.0.0", port=3000)
