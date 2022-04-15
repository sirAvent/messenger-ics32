import json
from collections import namedtuple
import time


# Create a namedtuple to hold the values we expect to retrieve from json messages.
DataTuple = namedtuple('DataTuple', ['userType','message','token'])


def extract_json(json_msg:str) -> DataTuple:
    '''
    Call the json.loads function on a json string and convert it to a DataTuple object
    '''
    try:
        json_obj = json.loads(json_msg)
        userType = json_obj['response']['type']
        message = json_obj['response']['message']
        if userType == 'ok':
            token = json_obj['response']['token']
            return DataTuple(userType, message, token)
        elif userType == 'error':
            token = ''
            return DataTuple(userType, message, token)
    except json.JSONDecodeError:
        print("Json cannot be decoded.")
    

def postextract_json(json_msg:str) -> DataTuple:
    '''
    Call the json.loads function on a json string and convert it to a DataTuple
    object.
    Same as extract_json function and used after it has been called because
    the server sends a different JSON string format.
    '''
    try:
        json_obj = json.loads(json_msg)
        userType = json_obj['response']['type']
        try:
            message = json_obj['response']['message']
        except:
            message = json_obj['response']['messages']
        if userType == 'ok':
            token = ''
            return DataTuple(userType, message, token)
        elif userType == 'error':
            token = ''
            return DataTuple(userType, message, token)
    except json.JSONDecodeError:
        print("Json cannot be decoded.")


def join(username, password, public_key):
    '''Format a JSON object as a string for user to join server.'''
    joinMSG = '{"join": {"username": "' + str(username) + '","password": "' + str(password) + '", "token":"' + (public_key) + '"}}'
    return joinMSG

def post(token, post):
    '''Format a JSON object as a string for user to post to server.'''
    postMSG = '{"token": "' + token + '", "post": {"entry": "'+ post + '", "timestamp": "' + str(time.time()) + '"}}'
    return postMSG


def bio(token, bio):
    '''Format a JSON object as a string for bio information recieved by server.'''
    bioMSG = '{"token": "' + token + '", "bio": {"entry": "'+ bio + '", "timestamp": ""}}'
    return bioMSG

def sendMSG(token, msg, reciever):
    '''Format a JSON object as a string for user to post to server.'''
    MSG = '{"token": "' + token + '", "directmessage": {"entry": "'+ msg + '", "recipient":"' + reciever + '", "timestamp": "' + str(time.time()) + '"}}'
    return MSG

