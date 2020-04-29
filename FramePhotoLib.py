import sys, os, re, time, copy
import multiprocessing
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
    # less than 2% side difference ratio - consider it square
    if 0.98 < self.height/self.width < 1.02:
      self.orientation = "square"
    elif self.height > self.width:
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
  

  def placePhotoInFrame(self,mockupinfo,photoinfo,frameinfo,numberframed):
    (mockupimage,mockupwidth,mockupheight) = mockupinfo
    (photoimage,photofilename,photowidth,photoheight) = photoinfo
    (mockupframecoordinatex,mockupframecoordinatey,mockupframewidth,mockupframeheight) = frameinfo
    # Add mockup to framed image
    framed = Image.new('RGB', (mockupwidth, mockupheight))
    framed.paste(mockupimage)

    # Set for blunt mode, will be overwritten if not blunt mode
    (coordx,coordy) = (mockupframecoordinatex,mockupframecoordinatey)
    resizer = (mockupframewidth,mockupframeheight)

    if not self.beBlunt:
      # If not blunt mode, will keep image ratio

      # Resize photo to enter the frame
      frameratio = mockupframewidth/mockupframeheight
      photoratio = photowidth/photoheight
      resizer = (mockupframewidth,mockupframeheight)
      if photoratio > frameratio:
        resizer = (mockupframewidth,int(mockupframewidth/photoratio))
      elif photoratio < frameratio:
        resizer = (mockupframeheight*photoratio,mockupframeheight)

      # If one side doesn't stick, implement padding
      resizer = tuple(int(x*0.95) for x in resizer)

      # Work out coordinates
      coordx = int(mockupframecoordinatex+(mockupframewidth-resizer[0])/2)
      coordy = int(mockupframecoordinatey+(mockupframeheight-resizer[1])/2)

    # Resize and place image
    resizedimage = photoimage.resize(resizer)
    framed.paste(resizedimage, (coordx, coordy))

    # Save resulting image
    with numberframed.get_lock():
      numberframed.value += 1
      framed.save(os.path.join(self.resultDirectory, os.path.splitext(photofilename)[0]+"-framed-"+str(numberframed.value)+".jpg"))


  def printProgress(self,numberframed,total):
    reduction = 2.5
    oldvalue = numberframed.value
    characteri = 0

    # Choose set of characters
    # characters = "-/|\"
    characters = "FRAMING"
    # characters = ["-_="]
    # characters = ["ᗣ••••••ᗤ","ᗣ•••••ᗤ_","ᗣ••••ᗤ__","ᗣ•••ᗤ___","ᗣ••ᗤ____","ᗣ•ᗤ_____","ᗣᗤ______"]

    self.printOutput(True,numberframed.value,total,reduction,oldvalue,characters,characteri)
    while(numberframed.value != total):
      # Not moving in progress
      if numberframed.value == oldvalue:
        characteri = (characteri+1) % len(characters)
      self.printOutput(False,numberframed.value,total,reduction,oldvalue,characters,characteri)
      time.sleep(0.1)
      oldvalue = numberframed.value
    self.printOutput(False,total,total,reduction,0,characters,characteri)

  def printOutput(self,start,number,total,reduction,oldvalue,characters,characteri):
    barlength = int(100/reduction)
    startstring = "Framing photos: "
    if start:
      sys.stdout.write(startstring+"["+ barlength*" " +"]")
    else:
      percentagebar = int( (number/total)*barlength )
      remainingbar = barlength - percentagebar
      sys.stdout.write("\r"+startstring+"["+percentagebar*"-")
      if number == oldvalue:
        sys.stdout.write(characters[characteri])
      sys.stdout.write(remainingbar*" "+"]")
      sys.stdout.write(" %d%% " % (number*100/total))
      sys.stdout.flush()

  def assemble(self):
    print("Getting ready to frame...")

    # Warning if blunt mode enabled
    if self.beBlunt:
      print("Blunt mode on - photo ratio could change to fit frame")

    # If no mockups or photos available, do nothing
    if len(self.photoList) == 0 or len(self.mockupList) == 0:
      print("Nothing to assemble. No photo detected or mockup detected (well, or both).")
      return

    # Check total not too much to assemble
    potentialtotal = len(self.mockupList)*len(self.photoList)
    if potentialtotal > 150:
      printstring = "LOTS AND LOTS! "+str(len(self.photoList))+" photos and "+str(len(self.mockupList))+" mockups found. Continue? [Enter]"
      input(printstring)

    # Multiprocessing stuff
    starttime = time.time()
    processes = []
    numberframed = multiprocessing.Value("i", 0)

    # Count total mto be assembled
    total = 0

    # Will parse through photos and mockups
    #  and assemble orientation matching ones
    for pi in range(0, len(self.photoList)):
      for mi in range(0, len(self.mockupList)):
        photo = self.photoList[pi]
        mockup = self.mockupList[mi]
        # Match?
        if photo.orientation != mockup.frameorientation:
          continue
        total += 1 # total that will be assembled increment if orientation matches
        # Dispatch task
        mockupinfo = (mockup.image.copy(),mockup.width,mockup.height)
        photoinfo = (photo.image.copy(),photo.filename,photo.width,photo.height)
        frameinfo = (mockup.framecoordinatex,mockup.framecoordinatey,mockup.framewidth,mockup.frameheight)
        self.placePhotoInFrame(mockupinfo,photoinfo,frameinfo,numberframed)
        # p = multiprocessing.Process(target=self.placePhotoInFrame, args=(mockupinfo,photoinfo,frameinfo,numberframed))
        # processes.append(p)

    # # Start processes
    # pr = multiprocessing.Process(target=self.printProgress, args=(numberframed,total))
    # pr.start()
    # for p in processes:
    #   p.start()

    # # Wait for process to end
    # for p in processes:
    #   p.join()
    # pr.join()

    timespent = int(time.time() - starttime)
    print("\nFramed "+str(total)+" photos in about "+str(timespent)+" seconds!")
    print("Check for results in directory "+self.resultDirectory)
    print()
    print("Happy with the result? Support us at https://github.com/Photography-Utils/photoframer")

