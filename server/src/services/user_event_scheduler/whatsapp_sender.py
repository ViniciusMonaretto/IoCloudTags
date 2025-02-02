from twilio.rest import Client

class TwilioWhatsAppSender:
    """Send messages using Twilio WhatsApp API"""

    def __init__(self, account_sid, auth_token, twilio_whatsapp_number):
        """
        :param account_sid: Twilio Account SID
        :param auth_token: Twilio Auth Token
        :param twilio_whatsapp_number: Twilio WhatsApp sender number (e.g., "whatsapp:+14155238886")
        """
        self.client = Client(account_sid, auth_token)
        self.twilio_whatsapp_number = twilio_whatsapp_number

    def send_message(self, recipient_number, message):
        """
        Sends a message using Twilio API.
        :param recipient_number: Recipient's phone number in WhatsApp format (e.g., "whatsapp:+1234567890")
        :param message: Message text
        """
        response = self.client.messages.create(
            from_=self.twilio_whatsapp_number,
            body=message,
            to=f"whatsapp:{recipient_number}"
        )
        return response.sid  # Twilio message ID