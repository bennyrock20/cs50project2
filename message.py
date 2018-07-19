import datetime

class Message:

    def __init__(self, nickname, channel, message):
        self.nickname = nickname
        self.channel = channel
        self.message = message
        self.date =  datetime.datetime.now()
        self.hours = datetime.datetime.now().strftime("%H:%M:%S")
    def __str__(self):
        return  str(self.hours)
