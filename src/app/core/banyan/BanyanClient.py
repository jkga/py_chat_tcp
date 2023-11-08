import sys
from functools import partial
from python_banyan.banyan_base import BanyanBase


class BanyanClient(BanyanBase):

    def __init__(self):
        self.connectedCallback = None
        self.onMessageCallback = None

    def start (self):

        # initialize the parent
        super(BanyanClient, self).__init__(process_name='BanyanClient')

        self.set_subscriber_topic('hi')
        self.set_subscriber_topic('biddingResponse')

        # send the first message - make sure that the server is already started
        self.publish_payload({'message': 'hello'}, 'hello')

        # get the reply messages
        try:
            self.receive_loop()
        except KeyboardInterrupt:
            self.clean_up()
            sys.exit(0)
        except Exception as e:
            if type(e).__name__ == 'ZMQError':
                self.clean_up ()
                sys.exit(0)
        
        return self

    def incoming_message_processing(self, topic, payload):
        """
        Process incoming messages received from the echo client
        :param topic: Message Topic string
        :param payload: Message Data
        """

        if topic == 'hi':
            # When a message is received and its number is zero, finish up.
            if 'connected' in payload:
                print(self.connectedCallback)
                if self.connectedCallback:
                    print('Connected to the Banyan Server')
                    self.connectedCallback (payload)

                # get initial data
                self.publish_payload({'message': 'data'}, 'bidding')

        else:
            if "data" in payload:
                print(payload)
                if self.onMessageCallback:
                    print('Connected to the Banyan Server')
                    self.onMessageCallback (topic, payload)
                

    def setConnectedCallback (self, **args):
        self.connectedCallback = args["callback"]
    
    def setOnMessageCallback(self, **args):
        self.onMessageCallback = args["callback"]
    
    def stop (self):
        try:
            self.publisher.close ()
            self.subscriber.close ()
            self.clean_up ()
        except Exception:
            pass

    def send (self, topic, payload):
        self.publish_payload(payload, topic)