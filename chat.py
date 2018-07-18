from message import Message
class Chat:
    channel_name= "";
    messages = []
    def __init__(self,):
        pass

    def add_message(self, nickname, message):
        message =  Message(nickname= nickname, message= message)
        self.messages.append(message)
