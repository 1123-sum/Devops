# backend/app.py
from flask import Flask, request, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix
import hashlib
import re
import logging

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)

# Configure logging (mask sensitive data)
logging.basicConfig(
    filename="audit.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s"
)

# Tokenize card number (never store raw PAN)
def tokenize_card(card_number: str) -> str:
    return hashlib.sha256(card_number.encode("utf-8")).hexdigest()

# Simple Luhn check for card validity
def valid_card(card_number: str) -> bool:
    digits = [int(x) for x in card_number if x.isdigit()]
    checksum = 0
    double = False
    for d in reversed(digits):
        if double:
            d = d * 2
            if d > 9:
                d -= 9
        checksum += d
        double = not double
    return checksum % 10 == 0

@app.route("/api/payment", methods=["POST"])
def process_payment():
    data = request.json
    card_number = data.get("cardNumber")
    cvv = data.get("cvv")
    expiry = data.get("expiry")

    if not card_number or not cvv or not expiry:
        return jsonify({"error": "Invalid payload"}), 400

    # Validate format (never log raw PAN or CVV)
    if not valid_card(card_number) or not re.match(r"^\d{3,4}$", cvv):
        return jsonify({"error": "Invalid card details"}), 400

    # Tokenize card
    token = tokenize_card(card_number)

    # Log only masked card + token
    masked_card = "**** **** **** " + card_number[-4:]
    app.logger.info(f"Payment processed for card {masked_card}, token={token}")

    return jsonify({"status": "Payment processed securely", "token": token}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
