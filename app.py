from flask import Flask, request, render_template_string, redirect, url_for, session
import sqlite3
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = "funkeyy_secret_2026"

DB = "/tmp/funkeyy.db"

# ================= ADMIN LOGIN =================

ADMIN_USER = "dinesh×funkeyy"
ADMIN_PASSWORD = "20622"

TELEGRAM_LINK = "https://t.me/funkeyy_dinesh_bot"
WHATSAPP_LINK = "https://wa.me/9779765936556"
TELEGRAM_BOT_TOKEN = "8852511502:AAGlo6IPNgy2NFQiVzPzOMuyqcJO93Vps1c"

# ================= DATABASE =================

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            service TEXT NOT NULL,
            price TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending',
            created_at TEXT NOT NULL
        )
    """)

    try:
        conn.execute("ALTER TABLE requests ADD COLUMN price TEXT")
    except sqlite3.OperationalError:
        pass

    conn.commit()
    conn.close()


# ================= LOGIN CHECK =================

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin"):
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated


# ================= MAIN PANEL =================

MAIN_HTML = """
<!DOCTYPE html>
<html>
<head>
<title>FUNKEYY PANEL</title>

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #1c2636;
    color: white;
}

.nav {
    background: #27364b;
    padding: 18px;
    text-align: center;
    font-size: 22px;
    font-weight: bold;
}

.container {
    max-width: 500px;
    margin: 30px auto;
    padding: 15px;
}

.box {
    background: #303d51;
    padding: 25px;
    border-radius: 20px;
}

h1, h2, h3 {
    text-align: center;
}

.price-list {
    background: #1e2939;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 20px;
}

.price-list p {
    border-bottom: 1px solid #445064;
    padding-bottom: 10px;
}

input, select, button {
    width: 100%;
    padding: 14px;
    margin-top: 15px;
    border: none;
    border-radius: 10px;
    font-size: 16px;
}

input, select {
    background: #1e2939;
    color: white;
}

button {
    background: #3b82f6;
    color: white;
    font-weight: bold;
}

.success {
    color: #65d6a4;
    text-align: center;
}

.order-id {
    background: #1e2939;
    padding: 12px;
    border-radius: 10px;
    text-align: center;
    margin-top: 15px;
}

.contact {
    display: flex;
    gap: 10px;
    margin-top: 20px;
}

.contact a {
    flex: 1;
    text-align: center;
    padding: 12px;
    border-radius: 10px;
    text-decoration: none;
    color: white;
    background: #3b82f6;
}

.admin-link {
    display: block;
    text-align: center;
    margin-top: 20px;
    color: #8ab4f8;
    text-decoration: none;
}

</style>
</head>

<body>

<div class="nav">
FUNKEYY PANEL
</div>

<div class="container">

<div class="box">

<h1>FUNKEYY PANEL</h1>

<div class="price-list">

<h3>PRICE LIST</h3>

<p>100 Like = Rs. 40 (1 Day)</p>
<p>700 Like = Rs. 180 (7 Days)</p>
<p>1500 Like = Rs. 270 (15 Days)</p>
<p>3000 Like = Rs. 430 (30 Days)</p>
<p>6000 Like = Rs. 680 (60 Days)</p>

</div>

<form method="POST">

<input
type="text"
name="uid"
placeholder="Enter User ID"
required
>

<select name="service" required>

<option value="">Select Service</option>

<option value="Like Service">👍 Like Service</option>
<option value="Top Up">💎 Top Up</option>
<option value="Level Up">⬆️ Level Up</option>

</select>

<button type="submit">
SUBMIT REQUEST
</button>

</form>

{% if message %}

<div class="success">
<h3>{{ message }}</h3>
</div>

<div class="order-id">
<b>Order ID: #{{ order_id }}</b>
<br><br>
Status: <b>Pending ⏳</b>
</div>

{% endif %}

<div class="contact">

<a href="{{ telegram }}">
TELEGRAM
</a>

<a href="{{ whatsapp }}">
WHATSAPP
</a>

</div>

</div>

<a class="admin-link" href="/admin">
ADMIN PANEL
</a>

</div>

</body>
</html>
"""


# ================= LOGIN PAGE =================

LOGIN_HTML = """
<!DOCTYPE html>
<html>
<head>
<title>FUNKEYY ADMIN LOGIN</title>

<style>

body {
    margin: 0;
    font-family: Arial;
    background: #1c2636;
    color: white;
}

.box {
    max-width: 400px;
    margin: 100px auto;
    background: #303d51;
    padding: 30px;
    border-radius: 20px;
}

h1 {
    text-align: center;
}

input, button {
    width: 100%;
    padding: 14px;
    margin-top: 15px;
    border: none;
    border-radius: 10px;
}

input {
    background: #1e2939;
    color: white;
}

button {
    background: #3b82f6;
    color: white;
    font-weight: bold;
}

.error {
    color: #ff7777;
    text-align: center;
}

</style>
</head>

<body>

<div class="box">

<h1>ADMIN LOGIN</h1>

{% if error %}
<p class="error">{{ error }}</p>
{% endif %}

<form method="POST">

<input
type="text"
name="username"
placeholder="Username"
required
>

<input
type="password"
name="password"
placeholder="Password"
required
>

<button type="submit">
LOGIN
</button>

</form>

</div>

</body>
</html>
"""


# ================= ADMIN PANEL =================

ADMIN_HTML = """
<!DOCTYPE html>
<html>
<head>
<title>FUNKEYY ADMIN</title>

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial;
    background: #1c2636;
    color: white;
}

.nav {
    background: #27364b;
    padding: 18px;
    text-align: center;
    font-size: 22px;
    font-weight: bold;
}

.container {
    max-width: 1100px;
    margin: 25px auto;
    padding: 15px;
}

.box {
    background: #303d51;
    padding: 20px;
    border-radius: 20px;
}

.status-online {
    text-align: center;
    color: #65d6a4;
}

.stats {
    display: flex;
    justify-content: center;
    gap: 15px;
    flex-wrap: wrap;
    margin: 20px 0;
}

.stat {
    background: #1e2939;
    min-width: 120px;
    padding: 18px;
    border-radius: 12px;
    text-align: center;
}

.stat b {
    font-size: 28px;
}

.pending {
    color: #ffd166;
}

.completed {
    color: #65d6a4;
}

.controls {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin: 20px 0;
}

.controls input,
.controls select,
.controls button,
.controls a {
    padding: 12px;
    border: none;
    border-radius: 8px;
}

.controls input,
.controls select {
    background: #1e2939;
    color: white;
}

.controls button,
.controls a {
    background: #3b82f6;
    color: white;
    text-decoration: none;
}

.table-box {
    overflow-x: auto;
}

table {
    width: 100%;
    min-width: 850px;
    border-collapse: collapse;
}

th, td {
    padding: 14px;
    border-bottom: 1px solid #4b596c;
    text-align: center;
}

select {
    padding: 8px;
    border-radius: 7px;
    border: none;
}

.action-btn {
    padding: 8px 12px;
    border: none;
    border-radius: 7px;
    color: white;
    background: #dc3545;
}

.status-btn {
    padding: 8px;
    border: none;
    border-radius: 7px;
    background: #3b82f6;
    color: white;
}

.bottom-buttons {
    text-align: center;
    margin-top: 25px;
}

.bottom-buttons a,
.bottom-buttons button {
    display: inline-block;
    margin: 5px;
    padding: 12px 18px;
    background: #3b82f6;
    color: white;
    border: none;
    border-radius: 8px;
    text-decoration: none;
}

.danger {
    background: #dc3545 !important;
}

</style>

</head>

<body>

<div class="nav">
FUNKEYY ADMIN
</div>

<div class="container">

<div class="box">

<h2 style="text-align:center;">
FUNKEYY ADMIN
</h2>

<div class="status-online">
● Panel: Online
</div>


<div class="stats">

<div class="stat">
<b>{{ total }}</b>
<br>Total
</div>

<div class="stat">
<b class="pending">{{ pending }}</b>
<br>Pending
</div>

<div class="stat">
<b class="completed">{{ completed }}</b>
<br>Completed
</div>

</div>


<form method="GET">

<div class="controls">

<input
type="text"
name="search"
value="{{ search }}"
placeholder="Search User ID"
>

<select name="service">

<option value="">All Services</option>

<option value="Like Service"
{% if service == "Like Service" %}selected{% endif %}
>
Like Service
</option>

<option value="Top Up"
{% if service == "Top Up" %}selected{% endif %}
>
Top Up
</option>

<option value="Level Up"
{% if service == "Level Up" %}selected{% endif %}
>
Level Up
</option>

</select>

<select name="status">

<option value="">All Status</option>

<option value="Pending"
{% if status == "Pending" %}selected{% endif %}
>
Pending
</option>

<option value="Completed"
{% if status == "Completed" %}selected{% endif %}
>
Completed
</option>

</select>

<button type="submit">
SEARCH
</button>

<a href="/dashboard">
REFRESH
</a>

</div>

</form>


<h2 style="text-align:center;">
REQUEST HISTORY
</h2>


<div class="table-box">

<table>

<tr>
<th>#</th>
<th>User ID</th>
<th>Service</th>
<th>Price</th>
<th>Status</th>
<th>Date</th>
<th>Action</th>
</tr>

{% for row in requests %}

<tr>

<td>#{{ row["id"] }}</td>

<td>{{ row["user_id"] }}</td>

<td>{{ row["service"] }}</td>

<td>{{ row["price"] }}</td>

<td>

{% if row["status"] == "Pending" %}
<span class="pending">⏳ Pending</span>
{% else %}
<span class="completed">✓ Completed</span>
{% endif %}

</td>

<td>{{ row["created_at"] }}</td>

<td>

<form
method="POST"
action="/status/{{ row['id'] }}"
style="display:inline;"
>

<select name="status">

<option value="Pending"
{% if row["status"] == "Pending" %}selected{% endif %}
>
Pending
</option>

<option value="Completed"
{% if row["status"] == "Completed" %}selected{% endif %}
>
Completed
</option>

</select>

<button class="status-btn" type="submit">
UPDATE
</button>

</form>


<form
method="POST"
action="/delete/{{ row['id'] }}"
style="display:inline;"
>

<button
class="action-btn"
type="submit"
onclick="return confirm('Delete this request?')"
>
DELETE
</button>

</form>

</td>

</tr>

{% endfor %}

</table>

</div>


{% if not requests %}
<p style="text-align:center;">
No requests found
</p>
{% endif %}


<div class="bottom-buttons">

<form
method="POST"
action="/clear"
style="display:inline;"
>

<button
class="danger"
type="submit"
onclick="return confirm('Delete ALL requests?')"
>
CLEAR ALL
</button>

</form>

<a href="/">
BACK TO PANEL
</a>

<a class="danger" href="/logout">
LOGOUT
</a>

</div>

</div>

</div>

</body>
</html>
"""


# ================= PRICE FUNCTION =================

def get_price(service):

    prices = {
        "Like Service": "Rs. 40",
        "Top Up": "Contact Admin",
        "Level Up": "Contact Admin"
    }

    return prices.get(service, "Contact Admin")


# ================= HOME =================

@app.route("/", methods=["GET", "POST"])
def home():

    message = ""
    order_id = None

    if request.method == "POST":

        uid = request.form.get("uid", "").strip()
        service = request.form.get("service", "").strip()

        if uid and service:

            price = get_price(service)

            conn = get_db()

            cursor = conn.execute(
                """
                INSERT INTO requests
                (user_id, service, price, status, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    uid,
                    service,
                    price,
                    "Pending",
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
            )

            order_id = cursor.lastrowid

            conn.commit()
            conn.close()

            message = "Request submitted successfully!"

    return render_template_string(
        MAIN_HTML,
        message=message,
        order_id=order_id,
        telegram=TELEGRAM_LINK,
        whatsapp=WHATSAPP_LINK
    )


# ================= ADMIN LOGIN =================

@app.route("/admin", methods=["GET", "POST"])
def admin_login():

    if session.get("admin"):
        return redirect(url_for("admin_panel"))

    error = ""

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username == ADMIN_USER and password == ADMIN_PASSWORD:

            session["admin"] = True

            return redirect(url_for("admin_panel"))

        else:
            error = "Wrong username or password!"

    return render_template_string(
        LOGIN_HTML,
        error=error
    )


# ================= DASHBOARD =================

@app.route("/dashboard")
@login_required
def admin_panel():

    search = request.args.get("search", "")
    service = request.args.get("service", "")
    status = request.args.get("status", "")

    conn = get_db()

    query = "SELECT * FROM requests WHERE 1=1"
    params = []

    if search:
        query += " AND user_id LIKE ?"
        params.append(f"%{search}%")

    if service:
        query += " AND service = ?"
        params.append(service)

    if status:
        query += " AND status = ?"
        params.append(status)

    query += " ORDER BY id DESC"

    requests_data = conn.execute(
        query,
        params
    ).fetchall()


    total = conn.execute(
        "SELECT COUNT(*) FROM requests"
    ).fetchone()[0]


    pending = conn.execute(
        "SELECT COUNT(*) FROM requests WHERE status = 'Pending'"
    ).fetchone()[0]


    completed = conn.execute(
        "SELECT COUNT(*) FROM requests WHERE status = 'Completed'"
    ).fetchone()[0]


    conn.close()


    return render_template_string(
        ADMIN_HTML,
        requests=requests_data,
        total=total,
        pending=pending,
        completed=completed,
        search=search,
        service=service,
        status=status
    )


# ================= UPDATE STATUS =================

@app.route("/status/<int:id>", methods=["POST"])
@login_required
def update_status(id):

    new_status = request.form.get("status")

    if new_status not in ["Pending", "Completed"]:
        new_status = "Pending"

    conn = get_db()

    conn.execute(
        "UPDATE requests SET status = ? WHERE id = ?",
        (new_status, id)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("admin_panel"))


# ================= DELETE ONE =================

@app.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete_request(id):

    conn = get_db()

    conn.execute(
        "DELETE FROM requests WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("admin_panel"))


# ================= CLEAR ALL =================

@app.route("/clear", methods=["POST"])
@login_required
def clear_requests():
    conn = get_db()
    conn.execute("DELETE FROM requests")
    conn.commit()
    conn.close()


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


# ================= START =================

init_db()

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )
