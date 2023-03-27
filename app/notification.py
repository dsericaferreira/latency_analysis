import pandas as pd
import random
import datetime
import json
from trycourier import Courier

# Usaremos Courier para notificações via email, mas poderiam ser sms, embedded em apps, etc.

class Notification():

  def __init__(self):

      with open('auth_token_courier.json', 'r') as js:
          self.token = json.load(js)
      
      self.email = self.token['email']
      self.template = self.token['template']

      self.client = Courier(auth_token=str(self.token['auth_token']))


  def send_email(self, cluster):
      if cluster != 'Boa':
        resp = self.client.send_message(
        message={
          "to": {
            "email": self.email,
          },
          "template": self.template,
          "data": {
          },
        }
      )
      
