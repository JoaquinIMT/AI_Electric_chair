import threading
import time

class Test():
   def __init__(self):
      self.num = 0

   def print_num(self,to_sum):
      self.num += to_sum
      print(self.num)

class Store_values():
   def __init__(self):
      self.mouth = 'neutral'
      self.eyes = 'neutral'

test = Test()

def delayer(delay):
   test.print_num(delay)
   time.sleep(delay)
   test.print_num(delay)
   time.sleep(delay)
   print(test.num)

if False:
   delayer(1)
   delayer(2)
else:
   # Create new threads
   thread1 = threading.Thread(target=delayer,args=(1,))
   thread2 = threading.Thread(target=delayer,args=(2,))

   # Start new Threads
   thread1.start()
   thread2.start()

print ("Exiting Main Thread")