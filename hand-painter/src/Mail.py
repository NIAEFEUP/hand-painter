from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl

global CONFIG
import os
from dotenv import dotenv_values

from mailjet_rest import Client
import os
import base64

TEXT_PART = '''Olá!

Obrigado por teres passado na nossa banca e teres ficado a conhecer aquilo que fazemos!

Para mais informações sobre o curso, podes consultar https://paginas.fe.up.pt/~estudar/cursos/licenciatura-engenharia-informatica/

Segue-nos nas nossas redes sociais para estares a par de tudo aquilo que fazemos! @niaefeup

Enviamos em anexo os teus desenhos!
'''


class Mail:
    def __init__(self):
        self.port = 465
        self.smtp_server_domain_name = "smtp.gmail.com"

        config = {
            **dotenv_values("../.env"),
            **os.environ,
        }

        api_key = config.get('MJ_APIKEY_PUBLIC', None)
        api_secret = config.get('MJ_APIKEY_PRIVATE', None)

        self.mailjetClient = Client(auth=(api_key, api_secret), version='v3.1')

        self.sender_mail = config.get("EMAIL", None)
        self.password = config.get("PASSWORD", None)

    # Not recommended
    def send_using_auth(self, to, images):
        try:
            if to != "":
                ssl_context = ssl.create_default_context()
                service = smtplib.SMTP_SSL(
                    self.smtp_server_domain_name, self.port, context=ssl_context
                )
                service.login(self.sender_mail, self.password)

                msg = MIMEMultipart()
                msg["Subject"] = "NIAEFEUP - Semana Profissão Engenheiro"
                msg["From"] = self.sender_mail
                msg["To"] = to

                text = MIMEText(
                    """
                Olá!

                Obrigado por teres passado na nossa banca e teres ficado a conhecer aquilo que fazemos no curso de Informática!

                Para mais informações sobre o curso, podes consultar https://paginas.fe.up.pt/~estudar/cursos/licenciatura-engenharia-informatica/
                
                Segue-nos nas nossas redes sociais para que estejas a par de tudo aquilo que fazemos! @niaefeup

                Enviamos em anexo os teus desenhos!
                """
                )
                msg.attach(text)

                for image in images:
                    with open(image, "rb") as f:
                        img_data = f.read()
                        image = MIMEImage(img_data, name=image.split("/")[-1])
                        msg.attach(image)

                service.sendmail(self.sender_mail, to, msg.as_string())

                service.quit()
        except Exception as e:
            print("Error sending email: ", e)

    def send_using_api(self, to, images):
        # Converting images to base64
        attachments = []
        for image in images:
            with open(image, "rb") as f:
                img_data = f.read()
                img_data_base64 = base64.b64encode(img_data).decode('utf-8')
                attachments.append(
                    {
                        "ContentType": "image/png",
                        "Filename": image.split("/")[-1],
                        "Base64Content": img_data_base64,
                    }
                )

        # Creating the email
        data = {
            'Messages': [
                {
                    "From": {
                        "Email": "banca@no-reply.niaefeup.pt",
                        "Name": "NIAEFEUP"
                    },
                    "To": [{
                        "Email": to,
                        "Name": "Futuro Engenheiro Informático"
                    }],
                    "Subject": "NIAEFEUP - Banca",
                    "TextPart": TEXT_PART,
                    "Attachments": attachments
                }
            ]
        }
        
        # Sending the email
        result = self.mailjetClient.send.create(data=data)
        print(result.status_code)
        print(result.json())
