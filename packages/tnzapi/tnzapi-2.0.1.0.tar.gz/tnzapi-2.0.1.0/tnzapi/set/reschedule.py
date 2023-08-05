import requests
import json
import asyncio

from tnzapi.set._common import Common
from tnzapi.base import SetRequestResult

class Reschedule(Common):

    SendTime    = ""

    """ Constructor """
    def __init__(self, kwargs):

        #super().__init__(kwargs)

        self.SetArgs(kwargs)

    """ Destructor """
    def __del__(self):
        self.SendTime = ""

    """ Update Data """
    def SetArgs(self, kwargs):

        super().SetArgs(kwargs)

        for key, value in kwargs.items():

            if key == "SendTime":
                self.SendTime = value

    """ API Data """
    @property
    def APIData(self):
        return {
            "Sender": self.Sender,
            "APIKey": self.APIKey,
            "APIVersion": self.APIVersion,
            "Type": "Reschedule",
            "MessageID" : self.MessageID,
            "SendTime": self.SendTime
        }

    """ Private function to POST message to TNZ REST API """
    def __PostMessage(self):

        try:
            r = requests.post(self.APIURL+"/set/reschedule", data=json.dumps(self.APIData), headers=self.APIHeaders)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return SetRequestResult(response=r)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            return SetRequestResult(error=str(e))

        return SetRequestResult(response=r)

    """ Private async function to POST message to TNZ REST API """
    async def __PostMessageAsync(self):

        return self.__PostMessage()

    """ Function to send message """
    def SendRequest(self,**kwargs):

        self.SetArgs(kwargs)

        if not self.Sender :
            return SetRequestResult(error="Empty Sender")
        
        if not self.APIKey :
            return SetRequestResult(error="Empty API Key")
        
        if not self.MessageID:
            return SetRequestResult(error="Empty Message ID")

        if not self.SendTime:
            return SetRequestResult(error="Empty Send Time")
        
        return self.__PostMessage()

    """ Async Function to send message """
    async def SendRequest(self,**kwargs):

        self.SetArgs(kwargs)

        if not self.Sender :
            return SetRequestResult(error="Empty Sender")
        
        if not self.APIKey :
            return SetRequestResult(error="Empty API Key")
        
        if not self.MessageID:
            return SetRequestResult(error="Empty Message ID")

        if not self.SendTime:
            return SetRequestResult(error="Empty Send Time")
        
        return await asyncio.create_task(self.__PostMessageAsync())

    def __repr__(self):
        return self.__pretty__(self.APIData)

    def __str__(self):
        return 'Reschedule(Sender='+self.Sender+', APIKey='+str(self.APIKey)+ ')'