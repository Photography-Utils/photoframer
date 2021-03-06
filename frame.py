
import sys, os, getopt
from FramePhotoLib import PhotoFramer

def help(message = ""):
  print('Help - parameters: [-h] [-d] [-r] [-y] [-p] [--passepartout[:%off_frame_size]] path/to/mockupdir path/to/photodir path/to/resultdir')
  print("Available options are:")
  print("-h/--help:\n\tPrint this message")
  print("-d/--debug:\n\tEnable debug messages")
  print("-r/--resize:\n\tAllow resizing of original photo to fit the frame")
  print("-y/--yes:\n\tWill not ask any question")
  print("-p:\n\tSet passepartout on frames to 95% of frame longest edge")
  print("--passepartout=off_frame_size:\n\tSet passepartout on frames to off_frame_size% of frame longest edge")
  print()
  print("Mandatory arguments are:")
  print("\tFirst a path to the directory with mockups")
  print("\tSecond a path to the directory with photos to frame")
  print("\tThird an existing path to the directory where to put result images")

  print("\n"+message)


def main(argv):
  # Look for options
  try:
    options, arguments = getopt.getopt(argv, 'hrypd', ["passepartout=","help","debug","resize","yes"])
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
    if opt in ('-h','--help'):
      help("Help was asked - will ignore other options and arguments")
      return
    elif opt in ('-d','--debug'):
      debug = True
    elif opt == '-p':
      passepartout = 95
    elif opt == '--passepartout':
      try:
        passepartout = int(arg)
      except:
        help("Passpartout option needs to be a number")
        return
    elif opt in ('-y','--yes'):
      noask = True
    elif opt in ('-r','--resize'):
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
