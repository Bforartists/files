#!/usr/bin/env bash

# Script runs above the actual git directory.
dir="bforartists"
branch=
clean=false

usage()
{
  cat << EOF 
Usage: bfa-build [[[-b branch ] | [-d]] | [-h]]

Specify a specific branch using -b [branch-name], otherwise, use -d to buld a
development release from current master.
  
This script requires create-dmg. To install via homebrew:

  brew install create-dmg

More info: https://github.com/create-dmg/create-dmg
EOF
}

while [ "$1" != "" ]; do
  case $1 in
    -b | --branch )         shift
                            branch="$1"
                            build="$1"
                            ;;
    -d | --dev )            branch=master
                            build="2.x-dev" # TODO: generate this properly.
                            ;;
    -c | --clean )          clean=true
                            ;;
    -h | --help )           usage
                            exit
                            ;;
    * )                     usage
                            exit 1
  esac
  shift
done

if [ $branch != "" ]; then
  # Prepare everything from git:
  git -C $dir stash # We may wish to pull this out of the stash after.
  git -C $dir fetch --all --tags
  git -C $dir checkout $branch
  git -C $dir pull
  
  # Kill off lib if we need a truly clean build.
  if [ $clean = true ]; then
    rm -rf lib
  fi
  # Update and compile.
  make -C $dir update
  make -C $dir
  
  # Create the folder from which to build the image.
  mkdir Bforartists-$branch
  cp -r build_darwin/bin/Bforartists.app Bforartists-$branch/
  
  # We can generate the icon set from an svg if we need to.
  #./svg2icns.sh bforartists.svg # https://gist.github.com/Canorus/1bc13e4b9ced1df79d396141de6178e4
  
  # Build the disk image. Uses create-dmg installed via `brew install create-dmg`
  create-dmg --volname "Bforartists" --volicon "bforartists.icns" --background "Bforartists-$build.png" --window-pos 200 120 --window-size 800 495 --icon-size 100 --icon "Bforartists.app" 200 295 --hide-extension "Bforartists.app" --app-drop-link 600 295 "Bforartists-$build-Mac" "Bforartists-$build/"
fi