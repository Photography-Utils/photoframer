import sys, os, getopt
from PIL import Image
import FramePhotoHelpers


#
# Print help message
#
def help(message = ""):
  print('Help - parameters: path/to/mockup framewidth [frameheight] framestartx framestarty')
  print("Available options are:")
  print("-h/--help:\n\tPrint this message")
  print("-n/--no:\n\tAutomatically say no to renaming the mockup file to the recommended name")
  print("Arguments are:")
  print(" - framewidth: width of frame the image will fit in")
  print(" - frameheight: (optional if for square) height of frame the image will fit in")
  print(" - framestartx: x coordinates where the frame starts int the mockup image from the top left corner")
  print(" - framestarty: y coordinates where the frame starts int the mockup image from the top left corner")

  print("\n"+message)


#
# Test a mockup with frame size and coordinates
#  then propose a new name with parameters included
#
def testMockup(mockuppath, framesize, framecoordinates, noask):
  application_path = os.path.dirname(os.path.abspath(__file__))

  testfilepath = os.path.join(application_path,"imageformockuptest.jpg")
  print("Mockup file image for frame test: "+testfilepath)
  photo_im = Image.open(testfilepath)
  mockup_im = Image.open(mockuppath)

  # If trying portrait, transpose test image
  if framesize[1] > framesize[0]:
    photo_im = photo_im.transpose(Image.ROTATE_90)

  # Create result image
  framed_im = Image.new('RGB', mockup_im.size)
  # Add mockup
  framed_im.paste(mockup_im, (0,0))
  # Resize photo to space size
  resizedphoto_im = photo_im.resize(framesize)
  # Add photo to frame at coordinates
  framed_im.paste(resizedphoto_im, framecoordinates)
  # Save result in working dir
  testresultfilename = 'isItFramedOk.jpg'
  wheretosaveresultfile = os.getcwd()
  framed_im.save(os.path.join(wheretosaveresultfile, testresultfilename))

  # Helper for frame name in case it's good
  print("If this result is good (meaning you dimensioned the frame correctly and the photo fits perfectly in it), you should rename the frame as follows in order to use it as a frame for kshhhactivate:")
  mockupname = FramePhotoHelpers.addMockupInfo(mockuppath,framesize,framecoordinates)
  print(mockupname)

  if not noask:
    answer = input("Rename mockup to suggested name? y/N ")
    if answer == 'Y' or answer == 'y':
      resultfile = os.path.join(os.path.dirname(mockuppath),mockupname)
      os.rename(r''+mockuppath, r''+resultfile)
      print("File renamed, now ready to use with kshhhactivate.py")

  print("\nCheck file "+testresultfilename+" at "+wheretosaveresultfile)


#
# Main function, called with argv passed on command line
#
def main(argv):
  # Look for options
  try:
    options, arguments = getopt.getopt(argv, 'nh', ["no", "help"])
  except:
    help("Some options are invalid")
    return

  # Default options
  noask = False

  # Look for options set by user
  for opt, arg in options:
    if opt in ('-h','--help'):
      help("Help was asked - will ignore other options and arguments")
      return
    elif opt in ('-n','--no'):
      noask = True

  if not 4 <= len(arguments) <= 5:
    help('Not the right number of arguments were given')
    return

  # Check mockup is an image
  mockuppath = arguments[0]
  try:
    Image.open(mockuppath)
  except:
    help('Mockup is not an image file')
    return

  # Check frame in mockup dimensions are all numbers
  (framewidth,frameheight,framestartx,framestarty) = (0,0,0,0)
  try:
    framewidth = int(arguments[1])

    # If 3 arguments, frameheight is framewidth -> square
    # If 4 arguments, different argument for framewidth
    frameheightindex = len(arguments) - 3

    frameheight = int(arguments[frameheightindex])
    framestartx = int(arguments[frameheightindex+1])
    framestarty = int(arguments[frameheightindex+2])
  except:
    help('Some frame dimensions are not numbers')
    return

  if framewidth <= 0 or frameheight <= 0 or framestartx <= 0 or framestarty <= 0:
    help('Some frame dimensions are negative')
    return

  # Go do the job!
  testMockup(mockuppath, (framewidth, frameheight), (framestartx, framestarty), noask)


#
# Will handle main here before handing off to mockup test function
#
if __name__ == "__main__":
  main(sys.argv[1:])
