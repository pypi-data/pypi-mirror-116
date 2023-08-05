import requests
import json
import asyncio

from tnzapi.get._common import Common
from tnzapi.base import SMSReceivedResult

class SMSReceived(Common):

    TimePeriod  = 1440

    """ Constructor """
    def __init__(self, kwargs):

        #super().__init__(kwargs)

        self.SetArgs(kwargs)

    """ Set Args """
    def SetArgs(self, kwargs):

        super().SetArgs(kwargs)

        for key, value in kwargs.items():

            if key == "TimePeriod":
                self.TimePeriod = value

    """ API Data """
    @property
    def APIData(self):
        return {
            "Sender": self.Sender,
            "APIKey": self.APIKey,
            "APIVersion": self.APIVersion,
            "Type": "SMSReceived",
            "TimePeriod" : self.TimePeriod
        }


    """ Private function to POST message to TNZ REST API """
    def __PostMessage(self):

        try:
            r = requests.post(self.APIURL+"/get/sms/received", data=json.dumps(self.APIData), headers=self.APIHeaders)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return SMSReceivedResult(response=r)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            return SMSReceivedResult(error=str(e))

        return SMSReceivedResult(response=r)

    """ Private async function to POST message to TNZ REST API """
    async def __PostMessageAsync(self):

        return self.__PostMessage()

    """ Function to send message """
    def Poll(self, **kwargs):

        self.SetArgs(kwargs)
        
        """ Checking validity """
        if not self.Sender :
            return SMSReceivedResult(error="Missing Sender")
        
        if not self.APIKey :
            return SMSReceivedResult(error="Missing APIKey")
        
        if not self.MessageID:
            return SMSReceivedResult(error="Missing MessageID")
        
        return self.__PostMessage()

    """ Function to send message """
    async def PollAsync(self, **kwargs):

        self.SetArgs(kwargs)
        
        """ Checking validity """
        if not self.Sender :
            return SMSReceivedResult(error="Missing Sender")
        
        if not self.APIKey :
            return SMSReceivedResult(error="Missing APIKey")
        
        if not self.MessageID:
            return SMSReceivedResult(error="Missing MessageID")
        
        return await asyncio.create_task(self.__PostMessageAsync())

    def __repr__(self):
        return self.__pretty__(self.APIData)

    def __str__(self):
        return 'SMSReceived(Sender='+self.Sender+', APIKey='+str(self.APIKey)+ ')'