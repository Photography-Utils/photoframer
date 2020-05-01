import sys, os, re, time
import multiprocessing
from PIL import Image

ORIENTATIONS = ["landscape", "portrait", "square"]

#
# Role: hold information every image will need
class BasicPicture:
  # Basic information of an image object
  def __init__(self, image):
    self.image = image
    self.lookupBasicInfo()
  def lookupBasicInfo(self):
    self.fullpath = self.image.filename
    self.filename = os.path.basename(self.fullpath)
    (self.width, self.height) = self.image.size

#
# Role: hold information on mockups
#   - mockup image size
#   - frame orientation and size
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

#
# Role: hold information on photos
#   - orientation and size
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

#
# The big photo framer class
# Role: hold information on
#   - what to frame
#   - how to frame it
#  and frame everything together
class PhotoFramer:
  mockupList = []
  photoList = []
  def __init__(self, mockupDir, photoDir, resultDir, resizingallowed = False, noask = False, passepartout = 100, debug = False):
    print("Setting up photo framer...")
    # Options
    self.resizingallowed = resizingallowed
    self.noask = noask
    self.passepartout = passepartout
    self.debug = debug
    # Directories
    self.mockupDirectory = mockupDir
    self.photoDirectory = photoDir
    self.resultDirectory = resultDir
    # Lookup
    self.lookupMockups()
    self.lookupPhotos()

  # Role: look up mockups in self.mockupdirectory
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
      print("Found",len(self.mockupList),"mockups")
      if self.debug:
        for mockup in self.mockupList:
          sys.stdout.write("  "+mockup.filename)
        sys.stdout.flush()
        print()
    else:
      print("Nada mockup found.")

  # Role: look up photos in self.photodirectory
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
      print("Found",len(self.photoList),"photos")
      if self.debug:
        for photo in self.photoList:
          sys.stdout.write("  "+photo.filename)
        sys.stdout.flush()
        print()
    else:
      print("Niet photo found.")
  
  # Role: create the result image by
  #   - opening the mockup mockup
  #   - pasting the photo photo inside the mockup
  #   - saving the result file with framed photo with index numberframed
  def placePhotoInFrame(self,mockup,photo,numberframed):
    # Add mockup to framed image
    framed = Image.new('RGB', (mockup.width, mockup.height))
    framed.paste(mockup.image)

    if self.resizingallowed:
      # Fit to frame no matter what the photo image
      resizer = (mockup.framewidth,mockup.frameheight)
    else:
      # If resizing not allowed, will keep image ratio
      # Resize photo to enter the frame
      frameratio = mockup.framewidth/mockup.frameheight
      photoratio = photo.width/photo.height
      resizer = (mockup.framewidth,mockup.frameheight)
      if photoratio > frameratio:
        resizer = (mockup.framewidth,int(mockup.framewidth/photoratio))
      elif photoratio < frameratio:
        resizer = (mockup.frameheight*photoratio,mockup.frameheight)

    # Implement padding to rate of passepartout
    if mockup.frameorientation == "square":
      if photo.width > photo.height:
        totakeoff = resizer[0]-int(resizer[0]*self.passepartout/100)
      else:
        totakeoff = resizer[1]-int(resizer[1]*self.passepartout/100)
    elif mockup.frameorientation == "portrait":
      # take out % of height
      totakeoff = resizer[1]-int(resizer[1]*self.passepartout/100)
    else: # landscape
      # take out % of width
      totakeoff = resizer[0]-int(resizer[0]*self.passepartout/100)
    
    # But only apply if resizing allowed
    if self.resizingallowed:
      resizer = tuple(int(x-totakeoff) for x in resizer)
    else:
      resizer = tuple(int(x*self.passepartout/100) for x in resizer)

    # Work out coordinates
    coordx = int(mockup.framecoordinatex+(mockup.framewidth-resizer[0])/2)
    coordy = int(mockup.framecoordinatey+(mockup.frameheight-resizer[1])/2)

    # Resize and place image
    resizedimage = photo.image.resize(resizer)
    framed.paste(resizedimage, (coordx, coordy))

    # Save resulting image
    resultname = os.path.splitext(photo.filename)[0]+"-framed-"+str(numberframed.value)+".jpg"
    framed.save(os.path.join(self.resultDirectory, resultname), quality=98, optimize=True)

  # Role: progress bar thread
  def printProgress(self,numberframed,total):
    reduction = 2.5
    oldvalue = numberframed.value
    characteri = 0

    # Choose set of characters
    # characters = "-/|\"
    characters = "FRAMING"
    # characters = ["-_="]
    # characters = ["ᗣ••••••ᗤ","ᗣ•••••ᗤ_","ᗣ••••ᗤ__","ᗣ•••ᗤ___","ᗣ••ᗤ____","ᗣ•ᗤ_____","ᗣᗤ______"]

    self.printBar(True,numberframed.value,total,reduction,oldvalue,characters,characteri)
    while(numberframed.value != total):
      # Not moving in progress
      if numberframed.value == oldvalue:
        characteri = (characteri+1) % len(characters)
      self.printBar(False,numberframed.value,total,reduction,oldvalue,characters,characteri)
      time.sleep(0.1)
      oldvalue = numberframed.value
    self.printBar(False,total,total,reduction,0,characters,characteri)

  # Role: print progress bar info
  def printBar(self,start,number,total,reduction,oldvalue,characters,characteri):
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
      sys.stdout.write("(%d/%d)" % (number,total))
      sys.stdout.flush()

  # Role: handles assembling photos into what frames into what mockups
  #  from start to end, printing traces etc,
  #  essentially organising the framing altogether
  def assemble(self):
    print()
    print("Getting ready to frame...")

    # If no mockups or photos available, do nothing
    if len(self.photoList) == 0 or len(self.mockupList) == 0:
      print("Nothing to assemble. No photo detected or mockup detected (well, or both).")
      return

    # Multiprocessing stuff
    starttime = time.time()
    numberframed = multiprocessing.Value("i", 0)

    # Sum up options for assembling
    print("Passepartout on frames set to: "+str(self.passepartout)+"%")
    print("Resizing of photos to fit the frames allowed:",self.resizingallowed)

    # Count total to be assembled
    total = 0
    matches = []
    for photo in self.photoList:
      for mockup in self.mockupList:
        # Match?
        if photo.orientation != mockup.frameorientation:
          continue
        total += 1
        matches.append((photo,mockup))

    message = "Images to create: "+str(total)
    if total > 150 and not self.noask:
      input("LOTS AND LOTS! "+message+"... Continue? [Enter]")
    elif self.debug:
      print(message)

    # Start progress bar process
    pr = multiprocessing.Process(target=self.printProgress, args=(numberframed,total))
    pr.start()

    # Will parse through photos and mockups
    #  and assemble orientation matching ones
    for (photo,mockup) in matches:
      # Do the task
      self.placePhotoInFrame(mockup,photo,numberframed)
      numberframed.value += 1
  
    # Wait for progress bar to stop
    pr.join()

    timespent = int(time.time() - starttime)
    print("\n\nFramed "+str(total)+" photos in about "+str(timespent)+" seconds!")
    print("Result images at "+self.resultDirectory)
    print()
    print("Happy? Support us at https://github.com/Photography-Utils/photoframer")
    print("Thank you (:")

