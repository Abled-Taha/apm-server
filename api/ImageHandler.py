import os
from PIL import Image

class ImageHandler(object):
  def __init__(self, BASE_DIR, width, height):
    self.pp_width = width
    self.pp_height = height
    self.BASE_DIR = BASE_DIR

  def updatedImage(self, username, image):
    path = f"{self.BASE_DIR}/users-data/{username}/pp.jpg"
    if os.path.exists(path):
      os.remove(path)
    if os.path.exists(f"{self.BASE_DIR}/users-data/{username}") == False:
      os.mkdir(f"{self.BASE_DIR}/users-data/{username}")
    with open(path, 'wb') as f:
      f.write(image)
    self.resizeImage(path)
    return True

  def getImagePath(self, username):
    path = f"{self.BASE_DIR}/users-data/{username}/pp.jpg"
    if os.path.exists(path) == False:
      path = f"{self.BASE_DIR}/users-data/default/pp.jpg"
    return path

  def resizeImage(self, imagePath):
    img = Image.open(imagePath)
    img = img.resize((self.pp_width, self.pp_height), Image.Resampling.LANCZOS)
    img.save(imagePath)