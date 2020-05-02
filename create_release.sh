#!/bin/sh

if [ -z "$1" ]; then
  echo "Usage: $0 version";
  exit 1;
fi;

set -x

echo "Get version from script argument"
version="$1"
tarballdirname="photoframer-$version"
tarballname="$tarballdirname.tar.gz"

echo "Clean up before packaging"
rm -rf "$tarballname"
rm -rf "$tarballdirname"
rm -rf *.spec
rm -rf dist/ build/
rm -rf __pycache__

echo "Create frame.py executable"
pyinstaller -y frame.py
pyinstaller -y frame.spec

echo "Create test.py executable"
pyinstaller -y test.py
pyinstaller -y test.spec
cp -rf imageformockuptest.jpg dist/test/

echo "Include RELEASE.md and example files"
cp -rf RELEASE.md dist/
cp -rf examples/resultexample.png dist/

echo "Prepare to create the tarball from dir $tarballdirname/"
mv dist $tarballdirname

echo "Create the tarball $tarballname"
tar -cvzf $tarballname $tarballdirname

echo "Create version git tag if result tarball exists"
test -f "$tarballname" && git tag $version

echo "Clean up after itself"
rm -rf *.spec
rm -rf dist/ build/
rm -rf __pycache__
rm -rf "$tarballdirname"

echo "Don't forget to sync the new tag : git push --tags"
echo "Now go to https://github.com/Photography-Utils/photoframer/releases and add your release to the new tag"
