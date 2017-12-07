"""
This script runs the PythonEvaluation Workeron an infinit loop.
""" 

from pythonEvaluation import PythonEvaluation

def start():
    print('PythonEvaluation  is starting...')  
    client = PythonEvaluation()
    client.ListenToSocketIO()

if __name__ == '__main__':
    start()