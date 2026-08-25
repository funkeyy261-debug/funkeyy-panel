from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Funkeyy Panel</title>
    <style>
        body {
            background: #111827;
            color: white;
            font-family: Arial;
            text-align: center;
            padding: 20px;
        }
        .box {
            background: #1f2937;
            padding: 25px;
            border-radius: 15px;
            max-width: 400px;
            margin: auto;
        }
        input, select, button {
            width: 90%;
            padding: 12px;
            margin: 10px;
            border-radius: 8px;
            border: none;
        }
        button {
            background: #2563eb;
            color: white;
            font-weight: bold;
        }
    </style>
</head>
<body>

<div class="box">
    <h1>FUNKEYY PANEL</h1>

    <form method="POST">
        <input type="text" name="uid" placeholder="Enter User ID" required>

        <select name="service">
            <option>Like Service</option>
            <option>Top Up</option>
            <option>Level Up</option>
        </select>

        <button type="submit">SUBMIT</button>
    </form>

    {% if message %}
        <h3>{{ message }}</h3>
    {% endif %}
</div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    message = ""
    
    if request.method == "POST":
        uid = request.form.get("uid")
        service = request.form.get("service")
        message = f"Request received: {service} for ID {uid}"

    return render_template_string(HTML, message=message)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)