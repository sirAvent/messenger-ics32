import socket
import ds_protocol
import time


class DirectMessage(dict):
    '''
    The DirectMessage class is responsible for working with individual user directmessages.
    It currently supports two features: 
    A timestamp property that is set upon instantiation and when the entry object
    is set and an entry property that stores the direct message.
    '''
    def __init__(self):
        self.recipient = None
        self.message = None
        self.timestamp = None

        # Subclass dict to expose DirectMessage properties for serialization
        dict.__init__(self, message=self.message, recipient=self.recipient, timestamp=self.timestamp)
    
    def set_message(self, message:str):
        '''
        Set the message attribute as specified string.
        '''
        self._message = message
        dict.__setitem__(self, 'message', message)

        # If timestamp has not been set, generate a new from time module
        if self._timestamp == 0:
            self._timestamp = time.time()

    def get_message(self):
        '''
        Return a message entry.
        '''
        return self._message
    
    def set_time(self, time:float):
        '''
        Set the value of timestamp to current time.
        '''
        self._timestamp = time
        dict.__setitem__(self, 'timestamp', time)
    
    def get_time(self):
        '''
        Return the value of timestamp.
        '''
        return self._timestamp

    """
    The property method is used to support get and set capability for entry and time values.
    When the value for entry is changed, or set, the timestamp field is updated to the
    current time.
    """ 
    entry = property(get_message, set_message)
    timestamp = property(get_time, set_time)

class DirectMessenger:
    '''
    An object for a person's account.
    Responsible for creating an instance of a DirectMessenger "account"
    '''
    def __init__(self, dsuserver=None, username=None, password=None):
        self.token = ''
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        self.port = 3021

		
    def send(self, message:str, recipient:str) -> bool:
        '''
        Send a directmessage to another DS user
        Return true if message successfully sent, false if send failed.
        Send a JSON String in this format:
        {"token":"user_token", "directmessage": {"entry": "Hello World!","recipient":"ohhimark", "timestamp": "1603167689.3928561"}}
        '''
        self.message = message
        self.recipient = recipient

        join_msg = ds_protocol.join(self.username, self.password, self.token)
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((self.dsuserver, self.port))
                
                client.sendall(join_msg.encode('utf-8'))
                srv_msg = client.recv(4096)
                userToken = ds_protocol.extract_json(srv_msg.decode('utf-8')).token
                response = ds_protocol.extract_json(srv_msg.decode('utf-8')).userType
                 
                if response == 'ok':
                    send_msg = ds_protocol.sendMSG(userToken, message, recipient)
                    client.sendall(send_msg.encode('utf-8'))
                    srv_msg2 = client.recv(4096)
                    
                    return True
                else:
                    return False
        except Exception as e:
            print(e)

                    
    def retrieve_new(self) -> list:
        '''
        Request unread message from the DS server and
        Return a list of DirectMessage objects containing all new messages
        Send JSON String in this format:
        {"token":"user_token", "directmessage": "new"}
        '''
        join_msg = ds_protocol.join(self.username, self.password, self.token)
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((self.dsuserver, self.port))
                
                client.sendall(join_msg.encode('utf-8'))
                srv_msg = client.recv(4096)
                userToken = ds_protocol.extract_json(srv_msg.decode('utf-8')).token
                response = ds_protocol.extract_json(srv_msg.decode('utf-8')).userType
                msg = ds_protocol.extract_json(srv_msg.decode('utf-8')).message
                
                if response == 'ok':
                    retrieve_msg = '{"token": "' + userToken + '", "directmessage": "new"}'
                    client.sendall(retrieve_msg.encode('utf-8'))
                    srv_msg2 = client.recv(4096)
                    response2 = ds_protocol.postextract_json(srv_msg2.decode('utf-8')).message
                    return response2
                else:
                    print(msg)
        except Exception as e:
            print(e)

 
    def retrieve_all(self) -> list:
        '''
        Request all messages from the DS server and
        Return a list of DirectMessage objects containing all messages
        
        Send JSON String in this format:
        {"token":"user_token", "directmessage": "all"}
        '''
        join_msg = ds_protocol.join(self.username, self.password, self.token)
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((self.dsuserver, self.port))
                    
                client.sendall(join_msg.encode('utf-8'))
                srv_msg = client.recv(4096)
                userToken = ds_protocol.extract_json(srv_msg.decode('utf-8')).token
                response = ds_protocol.extract_json(srv_msg.decode('utf-8')).userType
                msg = ds_protocol.extract_json(srv_msg.decode('utf-8')).message
                    
                if response == 'ok':
                    retrieve_msg = '{"token": "' + userToken + '", "directmessage": "all"}'
                    client.sendall(retrieve_msg.encode('utf-8'))
                    srv_msg2 = client.recv(4096)
                    response2 = ds_protocol.postextract_json(srv_msg2.decode('utf-8')).message
                    return response2
                else:
                    return []
        except Exception:
            print(DeniedConnection(Exception).message)
            return []
            


class DeniedConnection(Exception):
    '''
    A custom exception class used for handling specific errors
    such as RefusedConnection. Print a string to handle the exception.
    '''
    def __init__(self, message):
        self.message = 'Connection Denied. Server Refused.'


    
