import time

class waitAns:
    def __init__(self, user_id, wait_resp):
        self.start_wait_time = time.time()
        self.user_id = user_id
        self.waiting_response = wait_resp
        self.first_notify = False
        self.second_notify = False