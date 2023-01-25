# Let's start with some default (for me) imports...
from cx_Freeze import setup,Executable



# Process the includes, excludes and packages first
includes = []
excludes = []
packages = []
path = []

includefiles = ['README.txt','LICENSE.txt','imageformats']

# This is a place where the user custom code may go. You can do almost
# whatever you want, even modify the data_files, includes and friends
# here as long as they have the same variable name that the setup call
# below is expecting.

# No custom code added



# The setup for cx_Freeze is different from py2exe. Here I am going to
# use the Python class Executable from cx_Freeze

exe = Executable(
      script="imagetools.py",
      base="Win32GUI",
      icon = "appicon.ico",
      initScript = None,
      targetName = "imagetools.exe",
      compress = False,
      copyDependentFiles = True,
      appendScriptToExe = False,
      appendScriptToLibrary = False
	)

#targetDir = "",




# That's serious now: we have all (or almost all) the options cx_Freeze
# supports. I put them all even if some of them are usually defaulted
# and not used. Some of them I didn't even know about.

setup(
	 name             = "Imagetools",
      author           = "Jorrit Vander Mynsbrugge",
      author_email     = "jorrit.vm@gmail.com",
      version          = "2.5",
      license          = "GPL2",
      platforms        = "Windows",
      description      = "Image number-rename-resize-webalbum tool",
      url              = "",
      options = { 'build_exe': {'includes':includes,
						'excludes':excludes,
						'packages':packages,
						'include_files':includefiles,
						'path': path
						}
			}, 
      executables = [exe]
      )



# This is a place where any post-compile code may go.
# You can add as much code as you want, which can be used, for example,
# to clean up your folders or to do some particular post-compilation
# actions.

# No post-compilation code added



# And we are done. That's a setup script :-D
