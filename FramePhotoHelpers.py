import os, re
from ProgressBar.ProgressBar import ProgressBar

SQUARE_RATIO_DEFAULT_TOLERANCE = 0.02
MOCKUP_EXTENSION_INFO = r"-(portrait|landscape|square)-s([0-9]+)x([0-9]+)c([0-9]+)x([0-9]+)"


#
# Role: return orientation from width and height
# Return:
#  - "square" if within square tolerance
#  - "portrait" if height > width
#  - "landscape" otherwise
#
def getOrientation(width, height, squaretolerance = SQUARE_RATIO_DEFAULT_TOLERANCE):
  if 1-squaretolerance <= height/width <= 1+squaretolerance:
    return  "square"
  elif width > height:
    return "portrait"
  else:
    return "landscape"


#
# Check if filename contains mockup frame information
#
def hasMockupInfo(filename):
  return re.search(MOCKUP_EXTENSION_INFO, filename)


#
# Delete mockup frame information from filename
#
def deleteMockupInfo(filename):
  return re.sub(MOCKUP_EXTENSION_INFO, "", filename)


#
# Return mockup frame information from filename
#  Generates an exception if information not valid or filename doesn't contain information
#
def getMockupInfo(filename):
  info = hasMockupInfo(filename)
  if info:
    return (info.group(1),int(info.group(2)),int(info.group(3)),int(info.group(4)),int(info.group(5)))
  else:
    raise Exception("Could find mockup information")


#
# Return a filename with mockup frame information embedded in it
#
def addMockupInfo(filename, framesize, framecoordinates):
  mockupnameadd = ""

  # Orientation
  if framesize[0] > framesize[1]:
    mockupnameadd += "landscape"
  elif framesize[0] < framesize[1]:
    mockupnameadd += "portrait"
  elif framesize[0] == framesize[1]:
    mockupnameadd += "square"

  # Make frame position and size suffix
  mockupnameadd += "-s"+str(framesize[0])+"x"+str(framesize[1])
  mockupnameadd += "c"+str(framecoordinates[0])+"x"+str(framecoordinates[1])

  # Get mockupname and ext
  (mockupnamenoext, ext) = os.path.splitext(os.path.basename(filename))

  # Remove already present extension
  mockupnamenoext = deleteMockupInfo(mockupnamenoext)

  # Return result
  return (mockupnamenoext+"-"+mockupnameadd+ext)


#
# Role: hold information every image will need
#
class BasicPicture:
  # Basic information of an image object
  def __init__(self, image, debug=False):
    self.image = image
    self.debug = debug
    self.lookupBasicInfo()
  def lookupBasicInfo(self):
    self.fullpath = os.path.abspath(self.image.filename)
    (self.filename, self.extension) = os.path.splitext(os.path.basename(self.fullpath))
    (self.width, self.height) = self.image.size

#
# Role: hold information on mockups
#   - mockup image size
#   - frame orientation and size
#
class Mockup(BasicPicture):
  # Information specific to mockups
  def __init__(self, image, debug=False):
    super().__init__(image, debug)
    self.valid = True
    self.lookupMockupInfo()
  def lookupMockupInfo(self):
    try:
      (self.frameorientation,
      self.framewidth,
      self.frameheight,
      self.framecoordinatex,
      self.framecoordinatey) = getMockupInfo(self.filename)
    except:
      # Could not find info
      if self.debug:
        print("Mockup "+self.filename+" not valid")
      self.valid = False
    else:
      # Check results
      if not (
        self.framewidth > 0 and self.frameheight > 0 and
        self.framecoordinatex > 0 and self.framecoordinatey > 0
      ):
        self.valid = False
      else:
        # Work out orientation
        self.frameorientation = getOrientation(self.framewidth,self.frameheight)

#
# Role: hold information on photos
#   - orientation and size
#
class Photo(BasicPicture):
  # Information specific to photos
  def __init__(self, image, debug=False):
    super().__init__(image, debug)
    self.lookupPhotoInfo()
  def lookupPhotoInfo(self):
    self.orientation = getOrientation(self.width, self.height)
