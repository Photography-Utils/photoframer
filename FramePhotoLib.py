import sys, os
from PIL import Image

class BasicPicture:
  def __init__(self, image):
    self.image = image
    self.orientation = 'landscape'
    self.lookupBasicInfo()
  def lookupBasicInfo(self):
    self.fullpath = self.image.filename
    self.filename = os.path.splitext(os.path.basename(self.fullpath))[0]
    (self.width, self.height) = self.image.size

class Frame(BasicPicture):
  def __init__(self, image):
    super().__init__(image)
    self.lookupFrameInfo()
  def lookupFrameInfo(self):
    if 'portrait' in self.filename:
      self.orientation = 'portrait'
    elif 'square' in self.filename:
      self.orientation = 'square'
    self.placeCoordinates = (91, 205)
    self.sizeMax = (700,467)

class Photo(BasicPicture):
  def __init__(self, image):
    super().__init__(image)
    self.lookupPhotoInfo()
  def lookupPhotoInfo(self):
    if self.height > self.width:
      self.orientation = 'portrait'
    elif self.height == self.width:
      self.orientation = 'square'


class PhotoFramer:
  frameList = []
  photoList = []
  def __init__(self, frameDir, photoDir, resultDir):
    print("Set up photo framer")
    self.frameDirectory = frameDir
    self.photoDirectory = photoDir
    self.resultDirectory = resultDir
    self.lookupFrames()
    self.lookupPhotos()

  def lookupFrames(self):
    print("Looking for frames...")
    for root, dirs, files in os.walk(self.frameDirectory):
      for file in files:
        if 'jpg' not in file:
          continue
        self.frameList.append(Frame(Image.open(os.path.join(root,file))))
      break
    print("Found the following frames: ")
    for frame in self.frameList:
      sys.stdout.write(frame.filename+" ")
    sys.stdout.flush()
    print()
  def lookupPhotos(self):
    print("Looking for photos...")
    for root, dirs, files in os.walk(self.photoDirectory):
      for file in files:
        if 'jpg' not in file:
          continue
        self.photoList.append(Photo(Image.open(os.path.join(root,file))))
      break
    print("Found the following photos: ")
    for photo in self.photoList:
      sys.stdout.write(photo.filename+" ")
    sys.stdout.flush()
    print()
  
  def assemble(self):
    print("Getting ready to frame")
    totalToGoThrough = len(self.frameList)*len(self.photoList)
    i = 0
    for frame in self.frameList:
      for photo in self.photoList:
        i = i + 1
        sys.stdout.write("\rFraming photos: %d%%" % (i*100/totalToGoThrough))
        sys.stdout.flush()
        if photo.orientation != frame.orientation:
          continue
        if i > 50:
          return
        framed = Image.new('RGB', (frame.width, frame.height))
        framed.paste(frame.image)
        resizedImage = photo.image.resize(frame.sizeMax)
        framed.paste(resizedImage, frame.placeCoordinates)
        framed.save(os.path.join(self.resultDirectory, "framed-"+str(i)+".jpg"))
    print("\nFramed! Check in directory "+self.resultDirectory)

