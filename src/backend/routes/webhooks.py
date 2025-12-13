import os, stripe
from db import Database
from flask import Blueprint, request, jsonify
from interfaces import http_result

webhooks = Blueprint("webhooks", __name__)

stripe.api_key = os.getenv("STRIPE_KEY")
endpoint_key = os.getenv("STRIPE_WEBHOOK_KEY")

def complete_checkout(session):
    metadata = session["metadata"]
    
    print(metadata)

@webhooks.route("/", methods=["POST"])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        return http_result(400)
    except stripe.error.SignatureVerificationError:
        return http_result(400)

    if event["type"] != "checkout.session.completed":
        return

    handle_checkout_completed(event["data"]["object"])

    return http_result(200)