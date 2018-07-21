import datetime

class Message:

    def __init__(self, nickname, channel, message, filename=""):
        self.nickname = nickname
        self.channel = channel
        self.message = message
        self.date =  datetime.datetime.now()
        self.hours = datetime.datetime.now().strftime("%H:%M:%S")
        self.filename = filename
    def __str__(self):
        return  str(self.nickname + " " +self.channel)
