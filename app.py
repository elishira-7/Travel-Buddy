from flask import Flask, send_from_directory, request, jsonify, render_template
import pandas as pd
import os



app = Flask(
    __name__,
    static_folder="website_html",
    static_url_path=""
)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_DIR = os.path.join(BASE_DIR, "website_html")
IMG_DIR = os.path.join(HTML_DIR, "images")
DATA_FILE = os.path.join(BASE_DIR, "files", "tour_stats.csv")

# Load data
df = pd.read_csv(DATA_FILE, on_bad_lines="skip")
df.columns = df.columns.str.strip()


@app.route("/")
def home():
    return send_from_directory(HTML_DIR, "index.html")

@app.route("/search")
def search_page():
    return send_from_directory(HTML_DIR, "search.html")

@app.route("/about")
def about_page():
    return send_from_directory(HTML_DIR, "about.html")

@app.route("/style.css")
def css():
    return send_from_directory(HTML_DIR, "style.css")

@app.route("/images/<filename>")
def serve_images(filename):
    return send_from_directory(IMG_DIR, filename)

@app.route("/api/search")
def api_search():
    filtered = df.copy()

    region = request.args.get("region", "").strip().lower()
    budget = request.args.get("max_budget", "").strip()
    nightlife = request.args.get("nightlife", "").strip().lower()
    lgbtq = request.args.get("lgbtq", "").strip().lower()
    min_safety = request.args.get("min_safety", "").strip()
    min_temp = request.args.get("min_temp", "").strip()
    max_temp = request.args.get("max_temp", "").strip()
    visa = request.args.get("visa", "").strip().lower()

    if region:
        filtered = filtered[
            filtered["Region"].astype(str).str.lower().str.contains(region)
        ]

    if budget:
        try:
            mb = float(budget)
            filtered = filtered[filtered["AvgDailyCostUSD"] <= mb]
        except:
            pass

    if nightlife == "yes":
        filtered = filtered[filtered["Nightlife"] == True]

    if lgbtq == "yes":
        filtered = filtered[filtered["LGBTQFriendly"] == True]

    if min_safety:
        try:
            ms = float(min_safety)
            filtered = filtered[filtered["SafetyIndex"] >= ms]
        except:
            pass

    if min_temp:
        try:
            tmin = float(min_temp)
            filtered = filtered[filtered["Avgtemp"] >= tmin]
        except:
            pass

    if max_temp:
        try:
            tmax = float(max_temp)
            filtered = filtered[filtered["Avgtemp"] <= tmax]
        except:
            pass

    if visa:
        filtered = filtered[
            filtered["Visa"].astype(str).str.lower().str.contains(visa)
        ]

    output = filtered[[
        "Country",
        "Region",
        "AvgDailyCostUSD",
        "SafetyIndex",
        "LGBTQFriendly",
        "Nightlife",
        "Visa",
        "Avgtemp"
    ]]

    return jsonify(output.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)
