# Mac build script
Usage: bfa-build [[[[-b | --branch branch ] | [-d | --dev]]] [-c | --clean] | [-h]]

  -b, --branch               specify the branch to build
  -d, --dev                  build a dev build off master
  -c, --clean                clean all previous build artifacts

## Setup
Copy this script your the directory containing your bforartists clone and ensure it is executable. In my case, this is in `~/Projects/bforartists-git` (with `bforartists` a subdirectory of that).


## Build
To build BFA and create the disk image, execute this script as follows:

  `./bfa-build.sh -b [branch]`

where [branch] is the name of the current release branch. For 2.6.0, this would be:
  `./bfa-build.sh -b 2.6.0`

This will result in the application being built in `./build_darwin`.

## Additional information and options
If you've previously built this application, the previous build will be moved to `./build_darwin-old`, **replacing the previous backup** if one exists. To reset the libraries as well, downloading fresh copies, use the `-c` flag:

  `./bfa-build.sh -b [branch] -c`