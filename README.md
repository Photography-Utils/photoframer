This little personal project helps frame photos into frames of mockup rooms (mockup rooms not provided except small sample).
You can use any mockup you want, portrait, square or landscape, and frame any photo you want to the right frames. The program will help you calibrate your mockups (to map where the frame is in the mockup room) and then assemble photos to them - it will automatically frame all landscape photos into landscape frame mockups, portraits into portrait frame mockups and square into square frame mockups.

~~It's all automatic and simple!~~ __It's all automatic and simple if it's set right (easy).__


## Prerequisites
- Python 3: https://docs.python-guide.org/starting/install3/osx/
- Python PIL library: ```python3 -m pip install Pillow ```

## 1. Get the mockup frame information

Take a mockup file with a frame in it. You need to know where the actual photo frame is in the mockup file.
To do so, use the program kshhhtest.py.

It runs as such in a terminal:
```bash
python3 kshhhtest.py path/to/mockup framewidth [frameheight] framestartx framestarty
```

Where you started the command, check the file __isItFramedOk.jpg__.
If the photo fits perfectly into the mockup frame, then rename your mockup file with the suggestion in the terminal.
If not perfect, reiterate with different parameters. Bear in mind, DO NOT allow for white spaces inside the frame - in other words, make your photo stick to the frame as accurately as possible, you will have the possibility to enter a mode later that puts white spaces as passepartouts.


## 2. Frame all your photos

Now that you have your mockups renamed okay, put all your mockups in the same directory.
Put all your photos you want to incorporate into these mockups in another directory.

In a terminal, run:
```bash
python3 kshhhactivate.py path/to/mockupdir path/to/photodir path/to/resultdir [blunt]
```

All paths must exist, even the path/to/resultdir. All your framed photos will be available in path/to/resultdir. There is a blunt mode you can use by adding the word __blunt__ as an extra parameter to this command. This mode will not incorporate a white space between photo and frame, cost of that is that the photos may be changed ratios to fit perfectly into the frames.


__/!\ Don't work with originals, work with copies! Original photos are never modified, BUT I'd advise to have a copy of them.__

Enjoy!
