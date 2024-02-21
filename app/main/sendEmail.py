import smtplib
from email.mime.text import MIMEText
def send_email():
    try:
        mailServer = smtplib.SMTP('smtp-mail.outlook.com',587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login('recoveraisunergpassword@outlook.com','132344xdd')
        mensaje = MIMEText("""Este es el mensaje de las narices""")
        mensaje['From']="recoveraisunergpassword@outlook.com"
        mensaje['To']="blackrvalera@gmail.com"
        mensaje['Subject']="Tienes un correo"   
        mailServer.sendmail("recoveraisunergpassword@outlook.com",
                            "blackrvalera@gmail.com",
                            mensaje.as_string())
        print('Correo enviado correctamente') 
    except Exception as e:
        print(e)
send_email()