from flask import Flask, request, jsonify
from twilio.rest import Client
import os

app = Flask(__name__)

# === APNI CREDENTIALS YAHAN DAALO ===
TWILIO_SID = os.environ.get("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")  # 🔑 YAHAN CHANGE KARO - jo Twilio se mila tha
TWILIO_WHATSAPP = "whatsapp:+14155238886"
YOUR_WHATSAPP = "whatsapp:+918923313578"

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

@app.route('/webhook/whatsapp', methods=['POST'])
def send_whatsapp():
    try:
        data = request.get_json()
        
        message = f"""🔖 *ESTERA TRANSPORTATION* 🔖
━━━━━━━━━━━━━━━━━━━━━

*✨ NEW BOOKING REQUEST* ✨

👤 *Name:* {data.get('full_name', 'Not provided')}
📧 *Email:* {data.get('email', 'Not provided')}
📞 *Phone:* {data.get('phone', 'Not provided')}
📍 *Pickup:* {data.get('pickup', 'Not provided')}
🎯 *Destination:* {data.get('destination', 'Not provided')}
🚐 *Vehicle:* {data.get('vehicle', 'Not provided')}
📅 *Date:* {data.get('date', 'Not provided')}
⏰ *Time:* {data.get('time', 'Not provided')}

💬 *Additional:* {data.get('additional', 'None')}
━━━━━━━━━━━━━━━━━━━━━
⚡ Reply to confirm booking"""
        
        client.messages.create(
            body=message,
            from_=TWILIO_WHATSAPP,
            to=YOUR_WHATSAPP
        )
        
        return jsonify({"status": "success"}), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)