import smtplib  # Simple Mail Transfer Protocol
import ssl      #Secure socket layer (encryption service)

smtp_server = "smtp.gmail.com"
port = 465 # For SSL
sender_email = "studytool.support.carl@gmail.com"
receiver_email = "recklord1701@gmail.com"
app_password = "vmvc sdgl fyst lhfq"

subject = "ur app suks"
body = "omg lol...never seen a worse ap in my life...you're mom's gay...yor dad's a hoe...get punked"

message = f"Subject: {subject}\n\n{body}"

# Create a secure SSL context
context = ssl.create_default_context()

try: 
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, message)
    print("Email sent sucessfully")
except Exception as e:
    print(f"An error occured: {e}")

