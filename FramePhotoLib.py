import sys, os, re
from PIL import Image

ORIENTATIONS = ["landscape", "portrait", "square"]

class BasicPicture:
  # Basic information of an image object
  def __init__(self, image):
    self.image = image
    self.lookupBasicInfo()
  def lookupBasicInfo(self):
    self.fullpath = self.image.filename
    self.filename = os.path.basename(self.fullpath)
    (self.width, self.height) = self.image.size


class Mockup(BasicPicture):
  # Information specific to mockups
  def __init__(self, image):
    super().__init__(image)
    self.valid = True
    self.lookupMockupInfo()
  def lookupMockupInfo(self):
    info = re.search("(portrait|landscape|square)-s([0-9]+)x([0-9]+)c([0-9]+)x([0-9]+)", self.filename)
    try:
      self.frameorientation = info.group(1)
      self.framewidth = int(info.group(2))
      self.frameheight = int(info.group(3))
      self.framecoordinatex = int(info.group(4))
      self.framecoordinatey = int(info.group(5))
      print(self.frameorientation)
      print(self.framewidth)
      print(self.frameheight)
      print(self.framecoordinatex)
      print(self.framecoordinatey)
    except:
      # Could not find info
      self.valid = False
    else:
      # Check results
      if not (
        self.frameorientation in ORIENTATIONS and
        self.framewidth > 0 and self.frameheight > 0 and
        self.framecoordinatex > 0 and self.framecoordinatey > 0
      ):
        self.valid = False


class Photo(BasicPicture):
  # Information specific to photos
  def __init__(self, image):
    super().__init__(image)
    self.lookupPhotoInfo()
  def lookupPhotoInfo(self):
    if self.height > self.width:
      self.orientation = 'portrait'
    elif self.height == self.width:
      self.orientation = 'square'
    else:
      self.orientation = 'landscape'


# The big photo framer class
class PhotoFramer:
  mockupList = []
  photoList = []
  def __init__(self, mockupDir, photoDir, resultDir, blunt):
    print("Setting up photo framer...")
    self.beBlunt = blunt
    self.mockupDirectory = mockupDir
    self.photoDirectory = photoDir
    self.resultDirectory = resultDir
    self.lookupMockups()
    self.lookupPhotos()


  def lookupMockups(self):
    print("Looking for mockups...")
    for root, dirs, files in os.walk(self.mockupDirectory):
      for file in files:
        try:
          mockup_im = Image.open(os.path.join(root,file))
        except:
          pass
        else:
          mockup = Mockup(mockup_im)
          if mockup.valid:
            self.mockupList.append(mockup)
      break # Don't look in subdirs

    if len(self.mockupList) > 0:
      print("Found the following mockups: (",len(self.mockupList),")")
      for mockup in self.mockupList:
        sys.stdout.write("  "+mockup.filename)
      sys.stdout.flush()
      print()
    else:
      print("Nada mockup found.")


  def lookupPhotos(self):
    print("Looking for photos...")
    for root, dirs, files in os.walk(self.photoDirectory):
      for file in files:
        try:
          photo_im = Image.open(os.path.join(root,file))
        except:
          pass
        else:
          self.photoList.append(Photo(photo_im))
      break # Don't look in subdirs

    if len(self.photoList) > 0:
      print("Found the following photos: (",len(self.photoList),")")
      for photo in self.photoList:
        sys.stdout.write("  "+photo.filename)
      sys.stdout.flush()
      print()
    else:
      print("Niet photo found.")
  

  def assemble(self):
    print("Getting ready to frame...")

    if self.beBlunt:
      print("Blunt mode on - photo ratio could change to fit frame")

    total = len(self.mockupList)*len(self.photoList)
    progress = 0
    number_framed = 0

    if len(self.photoList) == 0 or len(self.mockupList) == 0:
      print("Nothing to assemble. No photo detected or mockup detected (well, or both).")
      return

    if total > 150:
      printstring = "LOTS AND LOTS! "+str(len(self.photoList))+" photos and "+str(len(self.mockupList))+" mockups found. Continue? [Enter]"
      input(printstring)

    # Will parse through photos and mockups
    for photo in self.photoList:

      for mockup in self.mockupList:

        photocount = int(progress/len(self.mockupList))+1
        progress += 1

        # Progress bar
        sys.stdout.write("\rFraming photos: %d%% (photo %d/%d)" % (progress*100/total,photocount,len(self.photoList)))
        sys.stdout.flush()

        # Match?
        if photo.orientation != mockup.frameorientation:
          continue

        # Add mockup to framed image
        framed = Image.new('RGB', (mockup.width, mockup.height))
        framed.paste(mockup.image)

        # Set for blunt mode, will be overwritten if not blunt mode
        (coordx,coordy) = (mockup.framecoordinatex,mockup.framecoordinatey)
        resizer = (mockup.framewidth,mockup.frameheight)

        if not self.beBlunt:
          # If not blunt mode, will keep image ratio

          # Resize photo to enter the frame
          frameratio = mockup.framewidth/mockup.frameheight
          photoratio = photo.width/photo.height
          resizer = (mockup.framewidth,mockup.frameheight)
          if photoratio > frameratio:
            resizer = (mockup.framewidth,int(mockup.framewidth/photoratio))
          elif photoratio < frameratio:
            resizer = (mockup.frameheight*photoratio,mockup.frameheight)

          # If one side doesn't stick, implement padding
          resizer = tuple(int(x*0.95) for x in resizer)

          # Resize image
          resizedimage = photo.image.resize(resizer)

          # Work out coordinates
          coordx = int(mockup.framecoordinatex+(mockup.framewidth-resizer[0])/2)
          coordy = int(mockup.framecoordinatey+(mockup.frameheight-resizer[1])/2)

        # Resize and place image
        resizedimage = photo.image.resize(resizer)
        framed.paste(resizedimage, (coordx, coordy))

        # Save resulting image
        number_framed += 1
        framed.save(os.path.join(self.resultDirectory, "framed-"+os.path.splitext(photo.filename)[0]+".jpg"))

    print("\nFramed! Check for result in directory "+self.resultDirectory)

