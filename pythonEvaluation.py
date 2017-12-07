from uuid import uuid4
import time
import inspect
import os

import Executables
from SwergioUtility.SocketIOClient import SocketIOClient
from SwergioUtility.MessageUtility import  MessageInterface
from SwergioUtility.Settings import getBasicSettings

class PythonEvaluation():
    def __init__ (self, custom_settings_path = None):
        self._socketIONamespaces = ['PythonEvaluation']
        self._socketIOSenderID = uuid4()
        self._socketIOClient = SocketIOClient(self._socketIONamespaces)

        self.safe_list = inspect.getmembers(Executables,inspect.isfunction)
        self.safe_dict = dict(self.safe_list)

        self.exec_reward  = os.getenv('EXEC_REWARD') or -1
        self.error_reward  = os.getenv('ERROR_REWARD') or -10
        self.canthandle_reward  = os.getenv('CANTHANDLE_REWARD') or -50

        custom_settings_path = custom_settings_path or os.getenv('CUSTOM_SETTINGS_PATH')

        max_length_message_text, self.MessageTypeEnum  = getBasicSettings(custom_settings_path)
        
    def On_PythonEvaluation_Message(self,data):
        msg = MessageInterface.from_document(data)
        comID = msg.CommunicationID
        doAction = True
        if msg.SenderID != str(self._socketIOSenderID):
            if self.MessageTypeEnum[msg.MessageType] == self.MessageTypeEnum.QUESTION:
                command = msg.Data
                self.act(command,comID)
            else:
                self.canthandle(comID)

    def ListenToSocketIO(self):
        self._socketIOHandler = [self.On_PythonEvaluation_Message]
        self._socketIOClient.listen(self._socketIOHandler)

    def act(self,command,CommunicationID):
        try:
            result = eval(command, {"__builtins__" : None }, self.safe_dict)
            if result != str:
                result = str(result)
            reward = self.exec_reward
        except:
            result = 'error'
            reward = self.error_reward

        self.emitObservation(result,reward, False, CommunicationID)

    def canthandle(self,comID):
        ob = '?'
        reward = self.canthandle_reward
        self.emitObservation(ob,reward,False,comID)

    def emitObservation(self,result,reward, done,CommunicationID):
        msgTyp = self.MessageTypeEnum.ANSWER.name
        namespace = self._socketIONamespaces[0]
        if type(result) != str:
            if type(result)  == int:
                result = str(result)
            else:
                result = str(list(result))
        Message = MessageInterface(namespace,self._socketIOSenderID, msgTyp,CommunicationID,Data = result, Reward = reward, DoneFlag = done)
        self._socketIOClient.emit(Message,namespace)  
        