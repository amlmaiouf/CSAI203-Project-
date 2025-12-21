class CustomizedRequest:
    def __init__(self, service_name, name, phone, email, address, date, request, notes, price=200):
        self.service_name = service_name
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
        self.date = date
        self.request = request
        self.notes = notes
        self.price = price 