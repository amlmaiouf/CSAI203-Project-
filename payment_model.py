import csv
import os

class Payment:
    def __init__(self, service_name, full_name, phone, payment_method, card_number=None, expiry_date=None, cvv=None, vodafone_number=None):
        self.service_name = service_name
        self.full_name = full_name
        self.phone = phone
        self.payment_method = payment_method
        self.card_number = card_number
        self.expiry_date = expiry_date
        self.cvv = cvv
        self.vodafone_number = vodafone_number

    def save_to_csv(self):
        # Save CSV in project root
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(BASE_DIR, "payments.csv")

        if not os.path.exists(file_path):
            with open(file_path, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "Service Name", "Full Name", "Phone", "Payment Method",
                    "Card Number", "Expiry Date", "CVV", "Vodafone Number"
                ])

        with open(file_path, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                self.service_name,
                self.full_name,
                self.phone,
                self.payment_method,
                self.card_number or "",
                self.expiry_date or "",
                self.cvv or "",
                self.vodafone_number or ""
            ])
