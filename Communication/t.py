import threading
import time

exitFlag = 0

#source = https://www.tutorialspoint.com/python/python_multithreading.htm
##STILL NOT FINISHED
class myThread (threading.Thread):
   
   def __init__(self, threadID, name, increment):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.increment = increment

   def run(self):
      print("Starting " + self.name)
      counter(self.increment)
      print("Exiting " + self.name)

def counter(threadName, counter, delay):
   while counter:
      if exitFlag:
         threadName.exit()
      time.sleep(delay)
      print(count)
      counter -= 1

# Create new threads
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)

# Start new Threads
thread1.start()
thread2.start()

print("Exiting Main Thread")