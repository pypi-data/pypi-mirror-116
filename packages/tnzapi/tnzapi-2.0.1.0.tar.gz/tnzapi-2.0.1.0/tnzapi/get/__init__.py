class Get(object):

    def __init__(self):
        self._status = None
        self._sms_received = None
        self._sms_reply = None
        self._result = None

    def Status(self,**kwargs):

        if self._status == None:
            from tnzapi.get.status import Status
            self._status = Status(kwargs)

        return self._status
    
    def SMSReceived(self,**kwargs):

        if self._sms_received == None:
            from tnzapi.get.sms_received import SMSReceived
            self._sms_received = SMSReceived(kwargs)

        return self._sms_received

    def SMSReply(self, **kwargs):

        if self._sms_reply == None:
            from tnzapi.get.sms_reply import SMSReply
            self._sms_reply = SMSReply(kwargs)

        return self._sms_reply
    
    def Result(self, **kwargs):

        if self._result == None:
            from tnzapi.get.result import Result
            self._result = Result(kwargs)

        return self._result