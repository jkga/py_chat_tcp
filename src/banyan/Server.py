import sys
import json
from python_banyan.banyan_base import BanyanBase
from datetime import datetime


class EchoServer(BanyanBase):

    def __init__(self, ):

        # initialize the parent
        super(EchoServer, self).__init__(process_name='EchoServer')

        self.set_subscriber_topic('hello')
        self.set_subscriber_topic('bidding')
        self.set_subscriber_topic('bid')

        self.startId = 1
        self.startBidId = 1

        self.bidding = {
            'total': 1,
            'data': [{
                'id': 1,
                'name': 'Welcome to the auction store!',
                'description': 'This is a demonstration of how python banyan works in a ncomputer network.\nAll the data are only stored in the server and will be automatically deleted once the process has stopped.',
                'status': 0,
                'totalBidCount': 0,
                'author': 'System Generated',
                'date': datetime.now().strftime('%B %d, %Y %I:%M%p'),
                'bids': [
                    {
                        'id': 1,
                        'amount': '',
                        'status': 0,
                        'date': datetime.now().strftime('%B %d, %Y %I:%M%p'),
                        'author': 'Welcome to the bidding section!'
                    }
                ]
            }]
        }

        # wait for messages to arrive
        try:
            self.receive_loop()
        except KeyboardInterrupt:
            self.clean_up()
            sys.exit(0)

    def incoming_message_processing(self, topic, payload):
        if(topic == 'hello'):
            self.publish_payload({'connected': 'true'}, 'hi')
            print('Message:', payload['message'])
            
        if(topic == 'bidding'):
            self.publish_payload(json.dumps(self.bidding), 'biddingResponse')
            print('Sending Bidding Data')
        
        if(topic == 'biddingRequest'):
            try:
                __data = json.loads(payload)

                __description = ''
                if not "name" in __data: return
                if not "author" in __data: return
                if not "description" in __data: __description = ''

                

                self.startId = self.startId + 1
                __id = self.startId

                # add new item
                __data["id"] = __id
                __data["date"] = datetime.now().strftime('%B %d, %Y %I:%M%p')
                __data["status"] = 1
                __data['totalBidCount'] = 0

                __data['bids'] = [
                    {
                        'id': 1,
                        'biddingRequestId': __id,
                        'amount': '',
                        'status': 0,
                        'date': datetime.now().strftime('%B %d, %Y %I:%M%p'),
                        'author': 'Welcome to the bidding section!'
                    }
                ]

                self.bidding["total"] = self.bidding["total"] + 1
                self.bidding["data"].insert(0,__data)
                    
                self.publish_payload(json.dumps(self.bidding), 'biddingResponse')
                print('Received a bid from client')
      
            except Exception as e:
                print(e)

        if(topic == 'bid'):

            try:
                __data = json.loads(payload)
                print(__data)

                if not "biddingRequestId" in __data: return

                for bidding in self.bidding["data"]:

                    if bidding["id"] == __data["biddingRequestId"]:
                        print('-------')
                        print(bidding)
                        
                        #self.startBidId  = self.startBidId + 1

                        __bidId = 2

                        # add bid to list
                        __date = datetime.now().strftime('%B %d, %Y %I:%M%p')
                        __data["id"] = __bidId
                        __data["date"] = __date,
                        __data["status"] = 0
                        bidding["bids"].insert(0,__data)
                        bidding["totalBidCount"] = bidding["totalBidCount"] + 1
                        
                self.publish_payload(json.dumps(self.bidding), 'biddingResponse')
                print('Received a bid from client')
      
            except Exception as e:
                print(e)

def echo_server():
    EchoServer()


if __name__ == '__main__':
    echo_server()
