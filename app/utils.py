import smtplib, os, csv
from django.conf import settings


def send_email(subject, body, to_email="info@allievapharma.com"):
	SMTP_SERVER = "mail.allievapharma.com"
	SMTP_PORT = 465
	USERNAME = "info@allievapharma.com"
	PASSWORD = "Allieva@0908"
	FROM_EMAIL = USERNAME
	
	try:
		# print("Connecting to SMTP server...")
		server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=3)
		server.login(USERNAME.strip(), PASSWORD)
		# print(" Login successful!")
		
		email_content = f"Subject: {subject}\n\n{body}"
		server.sendmail(FROM_EMAIL, to_email, email_content)
		# print("Email sent successfully!")
		server.quit()
		return True, "Email sent successfully"
	except smtplib.SMTPAuthenticationError as e:
		print(" Authentication failed:", e)
		return False, "Email authentication failed"
	except smtplib.SMTPConnectError as e:
		print(" Connection failed:", e)
		return False, "Could not connect to email server"
	except Exception as e:
		print(" Error:", e)
		return False, f"Unexpected error: {e}"


# Where to look for the CSV:
# 1) settings.MEDICINE_CSV_PATH if set
# 2) <BASE_DIR>/data/products.csv as a default

# MEDICINE_CSV_PATH = os.path.join(settings.BASE_DIR, "data", "products.csv")

def _csv_path():
	if hasattr(settings, "MEDICINE_CSV_PATH") and settings.MEDICINE_CSV_PATH:
		return settings.MEDICINE_CSV_PATH
	return os.path.join(settings.BASE_DIR, "data", "products.csv")


def _get_first_nonempty(row, *keys):
	for k in keys:
		if k in row and row[k] and str(row[k]).strip():
			return str(row[k]).strip()
	return ""


def get_product_by_code(code: str):
	"""
	Returns a dict with product details if 'Verification Code' matches.
	CSV columns we try (case-sensitive per DictReader):
		- Product Name / Product
		- Batch Name / Batch / Batch No / Batch Number
		- Manufacture Date / Mfg Date / Manufacturing Date
		- Expiry Date / Exp Date
		- Verification Code / Code
	"""
	code = (code or "").strip()
	
	path = _csv_path()
	if not os.path.exists(path):
		# You can choose to raise or return None; we return None and let the view message this gracefully.
		return None
	
	try:
		with open(path, newline="", encoding="utf-8") as f:
			reader = csv.DictReader(f)
			for row in reader:
				vcode = _get_first_nonempty(row, "Verification code", "Code")
				if vcode and vcode.strip().upper() == code.upper():
					product_name = _get_first_nonempty(row, "Product Name", "Product")
					batch = _get_first_nonempty(row, "Batch name", "Batch", "Batch No", "Batch Number")
					mfg = _get_first_nonempty(row, "Manufacture date", "Mfg Date", "Manufacturing Date")
					exp = _get_first_nonempty(row, "Expiry date", "Exp Date")
					# print(product_name,batch,mfg,exp)
					return {
						"product_name": product_name,
						"batch": batch,
						"mfg_date": mfg,
						"exp_date": exp,
						"verification_code": vcode,
						# "has_full_details" means newer stock with complete info
						"has_full_details": bool(product_name or batch or mfg or exp),
					}
	except Exception:
		# Keep quiet for users; log if you want.
		return None
	
	return None
