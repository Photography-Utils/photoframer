This little personal project helps frame photos into frames of mockup rooms (mockup rooms not provided except small sample).
You can use any mockup you want, portrait, square or landscape, and frame any photo you want to the right frames. The program will help you calibrate your mockups (to map where the frame is in the mockup room) and then assemble photos to them - it will automatically frame all landscape photos into landscape frame mockups, portraits into portrait frame mockups and square into square frame mockups.

~~It's all automatic and simple!~~ __It's all automatic and simple if it's set right (easy).__


## Prerequisites
- Python 3: [https://docs.python-guide.org/starting/install3/osx/]
- Python PIL library: ```python3 -m pip install Pillow ```

## 1. Set the mockup frame information

Take a mockup file with a frame in it. You need to know where the actual photo frame is in the mockup file.
To do so, use the program kshhhtest.py.

It runs as such in a terminal:
```bash
./test-mockup.sh [-h] [-n] path/to/mockup framewidth [frameheight] framestartx framestarty
```
- -h/--help:
	Print this message
- -n/--no:
	Automatically say no to renaming the mockup file to the recommended name

- framewidth: width of frame the image will fit in
- frameheight: (optional if for square) height of frame the image will fit in
- framestartx: x coordinates where the frame starts int the mockup image from the top left corner
- framestarty: y coordinates where the frame starts int the mockup image from the top left corner
  
Where you started the command, check the file __isItFramedOk.jpg__.
If the photo fits perfectly into the mockup frame, then rename your mockup file with the suggestion in the terminal.
If not perfect, reiterate with different parameters. Bear in mind, DO NOT allow for white spaces inside the frame - in other words, make your photo stick to the frame as accurately as possible, you will have the possibility to enter a mode later that puts white spaces as passepartouts*.


## 2. Frame all your photos

Now that you have your mockups renamed okay, put all your mockups in the same directory.
Put all your photos you want to incorporate into these mockups in another directory.

In a terminal, run:
```bash
./assemble.sh
    [-h] [-d] [-r] [-y] [-p] [--passepartout[=%off_frame_size]]
    path/to/mockupdir path/to/photodir path/to/resultdir
```
- -h/--help:
	Print this message
- -d/--debug:
	Enable debug messages
- -r/--resize:
	Allow resizing of original photo to fit the frame
- -y/--yes:
	Will not ask any question
- -p:
	Set passepartout* on frames to 95% of frame longest edge
- --passepartout=off_frame_size:
	Set passepartout* on frames to off_frame_size% of frame longest edge

Bear in mind, passepartout* cannot be constant all around the photo if you don't enable the --resize option along with it.

Mandatory arguments are:
- mockupdir: path to the directory containing the mockups - mockup files mush have the information on where the frame is in the following format: filename-\<orientation\>-s\<framewidth\>x\<frameheight\>c\<coordinatesframestartx\>x\<coordinatesframestarty\>.ext - orientation can be *portrait*, *landscape* or *square*
```
Example: blue-wall-basic-11-square-s1279x1279c862x273.jpg livingroom-square-s1279x1279c862x273.jpg
```
- photodir: path to the directory containing the photos to frame
- resultdir: existing path to the directory where the result images will be saved

All paths must exist, even the path/to/resultdir. All your framed photos will be available in path/to/resultdir.


__/!\ Don't work with originals, work with copies! Original photos are never modified, BUT I'd advise to have a copy of them.__

Enjoy!
You like this? Be a sponsor at [https://github.com/Photography-Utils/photoframer].

Notes:
* What is a passepartout? It's the space left between the side of the frame and the photo, and it is optional. See more at [https://en.wikipedia.org/wiki/Mat_(picture_framing)]

<img src="examples/resultexample.png" />
