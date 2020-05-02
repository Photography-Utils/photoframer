#!/bin/sh

# Just a wrapper for python
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
python3 "$DIR/frame.py" "$@"
