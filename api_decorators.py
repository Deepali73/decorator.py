from flask import Flask, request, redirect, jsonify
from functools import wraps

app = Flask(__name__)

# ✅ Built-in decorator to validate API key
def require_api_key(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        api_key = request.args.get("key")
        if api_key != "openai123":
            return jsonify({"error": "Invalid or missing API key"}), 403
        return f(*args, **kwargs)
    return wrapper

# ✅ Unified website redirector
website_links = {
    "google": "https://www.google.com",
    "gmail": "https://mail.google.com",
    "linkedin": "https://www.linkedin.com",
    "instagram": "https://www.instagram.com"
}

@app.route("/visit/<platform>", methods=["GET"])
@require_api_key
def visit_platform(platform):
    url = website_links.get(platform.lower())
    if url:
        return redirect(url)
    else:
        return jsonify({"error": f"Unknown platform: {platform}"}), 404

@app.route("/")
def home():
    return "✅ Visit /visit/google, /visit/gmail, etc. with ?key=openai123"

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0", port=5000)
