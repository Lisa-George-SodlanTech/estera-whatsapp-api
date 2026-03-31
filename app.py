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
        # JSON ya form data dono handle karega
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
        
        # Field mapping - aapke form ke hisaab se
        full_name = data.get('full_name') or data.get('Full Name') or data.get('name', 'Not provided')
        email = data.get('email') or data.get('Email Address') or data.get('Email', 'Not provided')
        phone = data.get('phone') or data.get('Phone Number') or data.get('Phone', 'Not provided')
        pickup = data.get('pickup') or data.get('Pickup Address') or data.get('Pickup', 'Not provided')
        destination = data.get('destination') or data.get('Destination Addresses') or data.get('Destination', 'Not provided')
        vehicle = data.get('vehicle') or data.get('Vehicle Type') or 'Not specified'
        date = data.get('date') or data.get('Date', 'Not provided')
        time = data.get('time') or data.get('Time', 'Not provided')
        
        message = f"""🔖 *ESTERA TRANSPORTATION* 🔖
━━━━━━━━━━━━━━━━━━━━━
*✨ NEW BOOKING REQUEST* ✨

👤 *Name:* {full_name}
📧 *Email:* {email}
📞 *Phone:* {phone}
📍 *Pickup:* {pickup}
🎯 *Destination:* {destination}
🚐 *Vehicle:* {vehicle}
📅 *Date:* {date}
⏰ *Time:* {time}

━━━━━━━━━━━━━━━━━━━━━
⚡ Reply to confirm booking"""
        
        client.messages.create(
            body=message,
            from_=TWILIO_WHATSAPP,
            to=YOUR_WHATSAPP
        )
        
        return jsonify({"status": "success", "message": "Booking notification sent"}), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
