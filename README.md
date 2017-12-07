# Python Code Evaluation Worker

This is an example worker for a swergio set-up.  The worker will try to evaluate the text of a question in python.

All callable functions are defined in "\Executables".

It is possible to set the reward/cost for "execution", "error on execution" and "can't handle request" in enviroment varibales. The default values are:
    EXEC_REWARD = -1
    ERROR_REWARD = -10
    CANTHANDLE_REWARD = -50

To use a custom settings file, add the file path as enviroment varibale CUSTOM_SETTINGS_PATH.


To start the worker execute "run.py". 
