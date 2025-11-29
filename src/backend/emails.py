import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Email(smtplib.SMTP):
    # Hereda de la clase SMTP; revisar https://docs.python.org/3/library/smtplib.html
    def __init__(self, server: str, port: int, user: str, password: str):
        # Configura todo e intenta iniciar sesión
        super().__init__(host=server, port=port)
        if port == 587:
            self.ehlo()
            self.starttls()
        self.login(user, password)

        self.senderEmail = user

    def prepareMessage(self, address: str, subject: str, body: str, textType: str) -> MIMEMultipart:
        # Configura la estructura del mensaje que se enviará en el correo.
        message = MIMEMultipart()
        message["From"] = self.senderEmail
        message["To"] = address
        message["Subject"] = subject

        message.attach(MIMEText(body, textType))

        return message
    
    def sendMessage(self, address: str, subject: str, body: str, textType: str) -> None:
        # Envía el correo
        message = self.prepareMessage(address, subject, body, textType)
        self.send_message(message)