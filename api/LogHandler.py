import datetime

class LogHandler(object):
  def __init__(self, BASE_DIR):
    self.BASE_DIR = BASE_DIR

  def read(self):
    with open(f'{self.BASE_DIR}/logs.txt', 'r') as f:
      return f.read()

  def write(self, text, data):
    if data.get("apiToken") == None or data.get("apiToken") == False:
      data["apiToken"] = ""
    
    with open(f'{self.BASE_DIR}/logs.txt', 'a') as f:
      f.write(f"{datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")} | {text} | {data["apiToken"]}")
      f.write('\n')
    return True