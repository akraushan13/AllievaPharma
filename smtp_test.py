import smtplib

# SMTP server settings (BigRock typical)
SMTP_SERVER = "mail.allievapharma.com"  # or your BigRock SMTP host
SMTP_PORT = 465                         # 465 for SSL, 587 for TLS
USERNAME = "info@allievapharma.com"     # full email address
PASSWORD = "Allieva@0908"          # your actual email password

TO_EMAIL = "it@allievapharma.com"  # where to send the test mail
FROM_EMAIL = USERNAME
SUBJECT = "SMTP Test from Python"
BODY = "Hello! This is a test email sent via BigRock SMTP."

try:
    print("Connecting to server...")
    server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)  # Use SMTP_SSL for port 465
    server.login(USERNAME.strip(), PASSWORD)
    print("✅ Login successful!")

    # Prepare the email
    message = f"Subject: {SUBJECT}\n\n{BODY}"

    server.sendmail(FROM_EMAIL, TO_EMAIL, message)
    print(f"✅ Email sent successfully to {TO_EMAIL}")
    server.quit()

except smtplib.SMTPAuthenticationError as e:
    print("❌ Authentication failed:", e)
except smtplib.SMTPConnectError as e:
    print("❌ Connection failed:", e)
except Exception as e:
    print("❌ Error:", e)
