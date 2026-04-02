from flask import Flask, request, jsonify
from twilio.rest import Client
import os
from datetime import datetime

app = Flask(__name__)

# Environment variables se read
TWILIO_SID = os.environ.get("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP = "whatsapp:+14155238886"
YOUR_WHATSAPP = "whatsapp:+18139932575"

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

@app.route('/webhook/whatsapp', methods=['POST'])
def send_whatsapp():
    try:
        # Form data get karo
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
        
        # Debug: Poora data print karo
        print(f"Received data: {data}")
        
        # Field mapping
        full_name = data.get('full_name') or data.get('Full Name') or data.get('your-name', 'Not provided')
        email = data.get('email') or data.get('Email Address') or data.get('your-email', 'Not provided')
        phone = data.get('phone') or data.get('Phone Number') or data.get('your-phone', 'Not provided')
        pickup = data.get('pickup') or data.get('Pickup Address') or data.get('pickup-address', 'Not provided')
        destination = data.get('destination') or data.get('Destination Address') or data.get('destination-address', 'Not provided')
        vehicle = data.get('vehicle') or data.get('How Many Passengers?') or data.get('passengers', 'Not specified')
        date = data.get('date') or data.get('Date', 'Not provided')
        
        # Time fix
        time_raw = data.get('time') or data.get('Time', 'Not provided')
        try:
            if time_raw and ':' in time_raw and 'AM' not in time_raw and 'PM' not in time_raw:
                time_obj = datetime.strptime(time_raw, '%H:%M')
                time = time_obj.strftime('%I:%M %p')
            else:
                time = time_raw
        except:
            time = time_raw
        
        additional = data.get('additional') or data.get('Additional Information', 'None')
        
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
💬 *Additional:* {additional}
━━━━━━━━━━━━━━━━━━━━━

        
        client.messages.create(
            body=message,
            from_=TWILIO_WHATSAPP,
            to=YOUR_WHATSAPP
        )
        
        return jsonify({"status": "success"}), 200
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
