import smtplib, os, csv
from django.conf import settings

import smtplib, requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


def send_email(subject , body_html , to_email="info@allievapharma.com" , image_url=None):
	SMTP_SERVER = "mail.allievapharma.com"
	SMTP_PORT = 465
	USERNAME = "info@allievapharma.com"
	PASSWORD = "Allieva@0908"
	FROM_EMAIL = USERNAME
	
	try:
		msg = MIMEMultipart("related")
		msg["From"] = FROM_EMAIL
		msg["To"] = to_email
		msg["Subject"] = subject
		
		msg_alternative = MIMEMultipart("alternative")
		msg.attach(msg_alternative)
		
		msg_alternative.attach(MIMEText(body_html , "html" , "utf-8"))
		
		# Attach inline product image
		if image_url:
			try:
				img_data = requests.get(image_url , timeout=5).content
				img = MIMEImage(img_data)
				img.add_header("Content-ID" , "<productimage>")
				img.add_header("Content-Disposition" , "inline" , filename="product.jpg")
				msg.attach(img)
			except Exception as e:
				print("⚠️ Could not attach product image:" , e)
		
		server = smtplib.SMTP_SSL(SMTP_SERVER , SMTP_PORT , timeout=3)
		server.login(USERNAME.strip() , PASSWORD)
		server.sendmail(FROM_EMAIL , to_email , msg.as_string())
		server.quit()
		return True , "Email sent successfully"
	
	except Exception as e:
		return False , f"Unexpected error: {e}"


def _csv_path():
	if hasattr(settings , "MEDICINE_CSV_PATH") and settings.MEDICINE_CSV_PATH:
		return settings.MEDICINE_CSV_PATH
	return os.path.join(settings.MEDIA_ROOT, "data", "products.csv")


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
