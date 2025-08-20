import csv
import os

csv_path = os.path.join("data", "products.csv")


def get_product_by_code(code: str):
	code = (code or "").strip().upper()
	
	if not os.path.exists(csv_path):
		print("CSV file not found:", csv_path)
		return None
	
	with open(csv_path, newline="", encoding="utf-8") as f:
		reader = csv.DictReader(f)
		for row in reader:
			vcode = (row.get("Verification code") or row.get("Code") or "").strip().upper()
			if vcode == code:
				print("---- Product Details ----")
				for key, value in row.items():
					print(f"{key}: {value}")
				print("-------------------------\n")
				return row  # return full dict if needed
	print("No product found with code:", code)
	return None


if __name__ == "__main__":
	user_code = input("Enter Verification Code: ")
	get_product_by_code(user_code)
