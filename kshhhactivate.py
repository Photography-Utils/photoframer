
import sys, os, getopt
from FramePhotoLib import PhotoFramer

def help(message = ""):
  print('Help: python kshhhactivate.py [-h] [-d] [-r] [-y] [-p] [--passepartout[:%off_frame_size]] path/to/mockupdir path/to/photodir path/to/resultdir')
  print("Available options are:")
  print("-h:\n\tPrint this message (help)")
  print("-d:\n\tEnable debug messages (debug)")
  print("-r:\n\tAllow resizing of original photo to fit the frame (resize)")
  print("-y:\n\tWill not ask any question (yes)")
  print("-p:\n\tSet passepartout on frames to 95% of frame size (passepartout)")
  print("--passepartout=%off_frame_size:\n\tSpecific percentage for passepartout on frames")
  print()
  print("Mandatory arguments are:")
  print("\tFirst a path to the directory with mockups")
  print("\tSecond a path to the directory with photos to frame")
  print("\tThird an existing path to the directory where to put result images")

  print("\n"+message)


def main(argv):
  # Look for options
  try:
    options, arguments = getopt.getopt(argv, 'hrypd', ["passepartout="])
  except:
    help("Some options are invalid")
    return

  # Default options
  resizing = False
  noask = False
  passepartout = 100
  debug = False

  # Look for options set by user
  for opt, arg in options:
    if opt == '-h':
      help("Help was asked - will ignore other options")
      return
    elif opt == '-d':
      debug = True
    elif opt == '-p':
      passepartout = 95
    elif opt == '--passepartout':
      try:
        passepartout = int(arg)
      except:
        help("Passpartout option needs to be a number")
        return
    elif opt == '-y':
      noask = True
    elif opt == '-r':
      resizing = True

  # Check we got all the mandatory arguments
  if len(arguments) != 3:
    help('Not all mandatory arguments were given')
    return

  # Check all mandaroty arguments are directories
  if not os.path.isdir(arguments[0]) or not os.path.isdir(arguments[1]) or not os.path.isdir(arguments[2]):
    help('Not all path are directories')
    return

  # Format directories to absolute path
  print()
  mockupdir = os.path.abspath(arguments[0])
  photodir = os.path.abspath(arguments[1])
  resultdir = os.path.abspath(arguments[2])
  print("Will use following directories:")
  print(" Mockup: "+mockupdir)
  print(" Photo: "+photodir)
  print(" Result: "+resultdir)
  print()

  # Go do the job!
  framer = PhotoFramer(mockupdir,photodir,resultdir,resizing,noask,passepartout,debug)
  framer.assemble()


if __name__ == "__main__":
  argv = sys.argv[1:]
  main(argv)
