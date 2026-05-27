import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from flask import Flask, jsonify, request
from flask_cors import CORS

import config

app = Flask(__name__)
CORS(app)

SERVICES = [
    {
        "id": "business-websites",
        "title": "Business Websites",
        "description": "High-performance, mobile-ready websites engineered for brand credibility, SEO, and conversion — built to enterprise quality standards.",
        "icon": "globe",
    },
    {
        "id": "cloud-deployment",
        "title": "Cloud Deployment",
        "description": "AWS, Docker, Terraform, and CI/CD pipelines — structured deployments with documentation and production-grade controls.",
        "icon": "cloud",
    },
    {
        "id": "server-monitoring",
        "title": "Server Monitoring",
        "description": "Grafana and Zabbix dashboards with proactive alerting — operational visibility before incidents impact users.",
        "icon": "bar-chart",
    },
    {
        "id": "vps-linux-setup",
        "title": "VPS & Linux Setup",
        "description": "Hardened Ubuntu/Debian servers with Nginx, SSL, firewall policies, and complete operational documentation.",
        "icon": "server",
    },
    {
        "id": "automation-scripts",
        "title": "Automation Scripts",
        "description": "Python and Bash automation for backups, reporting, and scheduled operations — reducing manual overhead at scale.",
        "icon": "settings",
    },
    {
        "id": "api-integrations",
        "title": "API Integrations",
        "description": "Secure integrations with payment gateways, CRMs, WhatsApp Business APIs, and third-party enterprise systems.",
        "icon": "link",
    },
]


def send_email(name, email, phone, service, message):
    if not config.MAIL_SERVER or not config.MAIL_USERNAME:
        return False

    subject = f"New Contact Form: {service} from {name}" if service else f"New Contact Form from {name}"

    body = f"""
New consultation request from Cloudsynq website

Name:    {name}
Email:   {email}
Phone:   {phone or '—'}
Service: {service or '—'}

Message:
{message or '—'}
"""

    msg = MIMEMultipart()
    msg["From"] = config.MAIL_FROM
    msg["To"] = config.MAIL_TO
    msg["Subject"] = subject
    msg.attach(MIMEText(body.strip(), "plain"))

    try:
        if config.MAIL_USE_TLS:
            with smtplib.SMTP(config.MAIL_SERVER, config.MAIL_PORT) as server:
                server.starttls(context=ssl.create_default_context())
                server.login(config.MAIL_USERNAME, config.MAIL_PASSWORD)
                server.send_message(msg)
        else:
            with smtplib.SMTP_SSL(config.MAIL_SERVER, config.MAIL_PORT) as server:
                server.login(config.MAIL_USERNAME, config.MAIL_PASSWORD)
                server.send_message(msg)
        return True
    except Exception as e:
        print(f"Email send failed: {e}")
        return False


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/api/services", methods=["GET"])
def get_services():
    return jsonify(SERVICES)


@app.route("/api/contact", methods=["POST"])
def contact():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400

    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    phone = (data.get("phone") or "").strip()
    service = (data.get("service") or "").strip()
    message = (data.get("message") or "").strip()

    errors = {}
    if not name:
        errors["name"] = "Please enter your name."
    if not email:
        errors["email"] = "Please enter your email."
    if not service:
        errors["service"] = "Please select a service."

    if errors:
        return jsonify({"error": "Validation failed", "fields": errors}), 422

    email_sent = send_email(name, email, phone, service, message)

    return jsonify({
        "success": True,
        "email_sent": email_sent,
        "detail": f"We'll reach out to {email}{' or ' + phone if phone else ''} within 24 hours.",
    })


if __name__ == "__main__":
    app.run(debug=config.DEBUG, host="0.0.0.0", port=5000)
