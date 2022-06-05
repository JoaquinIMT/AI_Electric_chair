class StoreValues():
    def __init__(self):
        self.feature_limit = 10
        self.mouth_arr = ['neutral']*self.feature_limit
        self.eyes_arr = ['neutral']*self.feature_limit
        self.sensor = 0
        self.count = 0
        self.esperar_instruccion = True
        self.evaluate_sign()

    def evaluate_sign(self):
        if self.mouth_arr.count(self.mouth_arr[0]) == self.feature_limit:
            self.mout = self.mouth_arr[0]
        if self.eyes_arr.count(self.eyes_arr[0]) == self.feature_limit:
            self.eye = self.eyes_arr[0]
    
    def put_next_sign(self,sign_m,sign_e):
        self.mouth_arr[self.count] = sign_m
        self.eyes_arr[self.count] = sign_e
        self.count = self.count + 1 if self.count < self.feature_limit-1 else 0
        print(self.count)