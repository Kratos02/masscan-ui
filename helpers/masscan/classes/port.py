class Port():
    def __init__(self, number, status, reason, protocol, ttl, banners):
        self.number = number
        self.status = status
        self.reason = reason
        self.protocol = protocol
        self.ttl = ttl
        self.banners = banners