import time

class waitAns:
    def __init__(self, user_id, wait_resp,theme_id):
        self.start_wait_time = time.time()
        self.user_id = user_id
        self.waiting_response = wait_resp
        self.first_notify = False
        self.second_notify = False
        self.sended_theme = theme_id

class motification:
    def __init__(self,id,text,wait_time):
        self.user_id = id
        self.text = text
        self.time = wait_time
        self.start_wait_time = time.time()
        self.first_notify = False
        self.second_notify = False