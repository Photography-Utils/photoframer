import sys, os, time
import multiprocessing
from PIL import Image
import FramePhotoHelpers

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
          mockup = FramePhotoHelpers.Mockup(mockup_im, self.debug)
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
          self.photoList.append(FramePhotoHelpers.Photo(photo_im, self.debug))
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

    # Time start save for stats
    starttime = time.time()

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
    numberframed = multiprocessing.Value("i", 0)
    progressbar = FramePhotoHelpers.ProgressBar(pretext="Framing photos: ",
                                                # progresschar="■",
                                                # remainingbarchar=" ",
                                                # loadingchars="▄▀",
                                                # startendchar="",
                                                progresschar="·",
                                                remainingbarchar="•",
                                                loadingchars="ᗧ",
                                                startendchar="·🍒",
                                                barwidth=33,
                                                displaypercentage=True,
                                                displaycount=True)
    pr = multiprocessing.Process(target=progressbar.inThread, args=(numberframed,total,0.1))
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
    print("Happy with the result? Just like Pacman, we need to eat (cherries and more).\nSupport us at https://github.com/Photography-Utils/photoframer")
    print("Thank you (:")

