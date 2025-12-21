class Payment:
    def __init__(self,service_name,full_name,phone,email,date,price,
                 payment_method,card_number=None,expiry_date=None,cvv=None,
                 cardholder_name=None,vodafone_number=None):
        self.service_name = service_name
        self.full_name = full_name
        self.phone = phone
        self.email = email
        self.date = date
        self.price = price
        self.payment_method = payment_method
        self.card_number = card_number
        self.expiry_date = expiry_date
        self.cvv = cvv
        self.cardholder_name = cardholder_name
        self.vodafone_number = vodafone_number
