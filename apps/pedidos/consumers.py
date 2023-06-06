from channels.consumer import SyncConsumer


class appsConsumer(SyncConsumer):

    def app1_message(self, message):
        # do something with message
        pass