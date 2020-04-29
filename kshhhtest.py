import sys, os, signal
from PIL import Image

def help(message = ""):
  print('Help - parameters: path/to/mockup framewidth [frameheight] framestartx framestarty')
  print("Arguments are:")
  print(" - framewidth: width of frame the image will fit in")
  print(" - frameheight: (optional if for square) height of frame the image will fit in")
  print(" - framestartx: x coordinates where the frame starts int the mockup image from the top left corner")
  print(" - framestarty: y coordinates where the frame starts int the mockup image from the top left corner")

  print("\n"+message)

def testMockup(mockuppath, framesize, framecoordinates):
  testfilepath = os.path.join(os.path.dirname(os.path.realpath(__file__)),"imageformockuptest.jpg")
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
  framed_im.save(os.path.join(os.getcwd(), 'isItFramedOk.jpg'))

  # Helper for frame name in case it's good
  print("If this result is good (meaning you dimensioned the frame correctly and the photo fits perfectly in it), you should rename the frame as follows in order to use it as a frame for kshhhactivate:")
  mockupnameadd = "landscape"
  if framesize[0] < framesize[1]:
    mockupnameadd = "portrait"
  elif framesize[0] == framesize[1]:
    mockupnameadd = "square"
  mockupnameadd += "-s"+str(framesize[0])+"x"+str(framesize[1])
  mockupnameadd += "c"+str(framecoordinates[0])+"x"+str(framecoordinates[1])
  (mockupnamenoext, ext) = os.path.splitext(os.path.basename(mockuppath))
  mockupname = mockupnamenoext+"-"+mockupnameadd+ext
  print(mockupname)

  signal.alarm(2)
  answer = input("Rename mockup to suggested name? y/N ")
  signal.alarm(0)
  if answer == 'Y' or answer == 'y':
    resultfile = os.path.join(os.path.dirname(mockuppath),mockupname)
    os.rename(r''+mockuppath, r''+resultfile)
    print("File renamed, now ready to use with kshhhactivate.py")

def main(argv):
  if not 4 <= len(argv) <= 5:
    help('Not the right number of arguments were given')
    return

  # Check mockup is an image
  mockuppath = argv[0]
  try:
    Image.open(mockuppath)
  except:
    help('Mockup is not an image file')
    return

  # Check frame in mockup dimensions are all numbers
  (framewidth,frameheight,framestartx,framestarty) = (0,0,0,0)
  try:
    framewidth = int(argv[1])

    # If 3 arguments, frameheight is framewidth -> square
    # If 4 arguments, different argument for framewidth
    frameheightindex = len(argv) - 3

    frameheight = int(argv[frameheightindex])
    framestartx = int(argv[frameheightindex+1])
    framestarty = int(argv[frameheightindex+2])
  except:
    help('Some frame dimensions are not numbers')
    return

  if framewidth <= 0 or frameheight <= 0 or framestartx <= 0 or framestarty <= 0:
    help('Some frame dimensions are negative')
    return

  # Go do the job!
  testMockup(mockuppath, (framewidth, frameheight), (framestartx, framestarty))

# Will handle main here before handing off to mockup test function
if __name__ == "__main__":
  main(sys.argv[1:])
