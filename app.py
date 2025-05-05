from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# Email credentials
EMAIL = "no-reply@aarkshsystems.com"
PASSWORD = "Robot@132"  # Use App Password if 2FA is enabled
SMTP_SERVER = "smtp.zoho.in"
SMTP_PORT = 587

@app.route('/send-email', methods=['POST'])
def send_email():
    # Get data from request
    data = request.json
    name = data.get("name")
    email = data.get("email")
    order_number = data.get("order_number")
    status = data.get("status")
    tracking_link = data.get("tracking_link")

    # Check if all fields are provided
    if not all([name, email, order_number, status, tracking_link]):
        return jsonify({"error": "Missing information"}), 400

    # Professional message with emojis
    subject = f"🚚 Order Update: #{order_number} - {status} 📦"
    message = f"""
    Dear {name},

    We are pleased to inform you that the status of your order **#{order_number}** has been updated.

    📦 **Order Status:** {status}  
    🔗 **Tracking Link:** {tracking_link}

    You can use the link above to track your shipment in real-time.  
    If you have any questions regarding your order, we’re here to help. Feel free to reach out! 🤝

    ---

    ⚠️ *This is an automated email. Please do not reply to this message.*  
    For any support or inquiries, please contact us at **support@aarkshsystems.com**.

    Thank you for choosing **Aarksh Systems**.  
    We appreciate your trust and look forward to serving you again soon. 🙏

    Warm regards,  
    ✨ Team Aarksh Systems 🌱
    """

    try:
        msg = MIMEText(message, "plain")
        msg['Subject'] = subject
        msg['From'] = EMAIL
        msg['To'] = email

        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, email, msg.as_string())

        return jsonify({"message": f"Email successfully sent to {email}"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
