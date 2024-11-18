import os, base64
from PIL import Image

class ImageHandler(object):
  def __init__(self, BASE_DIR, width, height):
    self.pp_width = width
    self.pp_height = height
    self.BASE_DIR = BASE_DIR

  def writeBytesObjToImage(self, username, imageBytesObj):
    path = f"{self.BASE_DIR}/users-data/{username}/pp.jpg"
    if os.path.exists(path):
      os.remove(path)
    if os.path.exists(f"{self.BASE_DIR}/users-data/{username}") == False:
      os.mkdir(f"{self.BASE_DIR}/users-data/{username}")
    with open(path, 'wb') as f:
      f.write(imageBytesObj)
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

  def getImageBytes(self, imagePath):
    with open(imagePath, "rb") as image_file:
      imageBytesObj = base64.standard_b64encode(image_file.read())
    return imageBytesObj