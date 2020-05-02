#!/bin/sh

if [ -z "$1" ]; then
  echo "Usage: $0 version";
  exit 1;
fi;

set -x
set -v

# Get version from script arguments
version = $1

echo "Clean up before packaging"
rm -rf frame.spec
rm -rf test.spec
rm -rf dist
rm -rf build

echo "Create frame.py executable"
pyinstaller frame.py
pyinstaller frame.spec

echo "Create test.py executable"
pyinstaller test.py
pyinstaller test.spec

echo "Include RELEASE.md file"
cp RELEASE.md dist/

tarballdirname = photoframer-$version
echo "Prepare to create the tarball from dir $tarballdirname/"
mv dist $tarballname

tarballname = $tarballdirname.tar.gz
echo "Create the tarball $tarballname"
tar -cvzf $tarballname.tar.gz $tarballdirname

echo "Create version git tag if result tarball exists"
if [ -f "$tarballname" ]; then
    git tag
fi

echo "Clean up after itself"
rm -rf frame.spec
rm -rf test.spec
rm -rf dist
rm -rf build
