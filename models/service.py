class Service:
    def __init__(self, service_id, service_name, type, price, description, is_available=True):
        self.service_id = service_id
        self.service_name = service_name
        self.type = type
        self.price = price
        self.description = description
        self.is_available = is_available

    def to_dict(self):
        """Helper to convert object to dictionary for templates"""
        return {
            'service_id': self.service_id,
            'service_name': self.service_name,
            'type': self.type,
            'price': self.price,
            'description': self.description,
            'is_available': self.is_available
        }