# Python Progress Bar
Prints an all customisable **easy-to-use** progress bar. It can be the thread target or a normal function call.


## Import in your code
```python
from *folderclone*.ProgressBar import ProgressBar
```
Now use as class ProgressBar.
/!\ folderclone should not contain character "-". Make sure not to clone in default git clone dir for this repo.


## Use
### As a simple function call
```python
max = 30
progressbar = ProgressBar()
for i in range(0,max):
  progressbar.print(i,max)
  time.sleep(1) # To see progress
```

### As a separate thread target
```python
max = 30
progressbar = ProgressBar()
number = multiprocessing.Value("i", 0)
multiprocessing.Process(target=progressbar.inThread, args=(number,max))
for i in range(0,max)
  number.value = i
  time.sleep(1) # To see progress
```


## Go further: customise your bar
### Style parameters
You can give the following optional arguments to the ProgressBar constructor:
- pretext: Text to print before the bar (default "")
- progresschar: Character to show progress (default '█')
- loadingchars: Last character of bar moving as bar loads (moves even if no progress) (default "█▓▒░▒▓")
- startendchar: Characters going around the bar (default "||")
- barwidth: Length of the bar in characters (does not include optionally printed pretext, progresschar, percentage and count) (default terminal width/2)
- displaypercentage: Show percentage as well or not (default False)
- displaycount: Show count as well or not (default False)

### Thread parameters
If you use the thread version, you can customise the refresh time of your progress bar.
To do this, give an extra argument (type float) representing the refreshing period of the bar.
```python
multiprocessing.Process(target=progressbar.inThread, args=(number,max,0.2))
```
