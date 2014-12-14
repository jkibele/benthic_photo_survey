---
layout: page
title: Installation
permalink: /installation/
---

If you want to use BPS on Windows, just take a look at the Windows Installation section below. BPS can run on Linux and Mac too. Installation on Mac can be tricky and if you want to go that route, you'll have to go it alone using the Linux Installation section below as a guide.

### Windows Installation

Installing BPS on Windows is simply a matter of downloading a zip file, uncompressing it, and double clicking the `bps_gui.exe` executable file. The only caveat is that `bps_gui.exe` must not be moved from its directory. Here are the necessary steps in excruciating detail:

1. Direct your web browser to [the latest BPS release](https://github.com/jkibele/benthic_photo_survey/releases/latest) and download `bps_windows.zip`.

2. Unzip the `bps_gui` directory onto your hard drive. You can put it wherever you'd like but these instructions will assume it's going to `C:\bps_gui`. 

	* Double click the `bps_windows.zip` file that you downloaded
	* Right click the `bps_gui` folder and choose copy
	* Navigate to `C:\` (or wherever you want) and paste the `bps_gui` folder <br /><br />

3. Navigate to the `C:\bps_gui` and double click `bps_gui.exe` (this may show up as `bps_gui` if Windows is configured to hide extensions). A command prompt will open followed by the BPS application. The command prompt window will stay open in the background and display some extra information that you are free to completely ignore.

4. That's it! Just remember to always run BPS from within the `bps_gui` folder. It needs all those other files in the same directory in order to function. Check out the Tutorial section of the [Documentation]({{ site.baseurl }}/docs) to learn how to set your preferences and start using BPS.

### Linux Installation

BPS was developed on [Ubuntu](http://www.ubuntu.com/). The following installation steps were tested on 64-bit Ubuntu 14.04:

1. Satisfy the prerequisites for BPS by entering the following commands in the terminal (you may need to use `sudo` to get the necessary permissions):

		apt-get update
		apt-get install python-scipy python-matplotlib python-qt4 python-gdal python-pip git python-pyexiv2
		pip install pynmea slugify
2. Direct your web browser to [the latest BPS release](https://github.com/jkibele/benthic_photo_survey/releases/latest) and download and extract the source code. I felt compelled to detail how to extract an archive for the Windows users but you're using Ubuntu so I'm going to assume you can take care of it.

3. Go to the `bps_package` directory and run `python bps_gui.py`.

4. That should start BPS. Check out the Tutorial section of the [Documentation]({{ site.baseurl }}/docs) to learn how to set your preferences and start using BPS.

If you want the very latest version, you can just do step 1 and then go to the [BPS Repository](https://github.com/jkibele/benthic_photo_survey) and clone it. If you do that, there's no guarantee that BPS will work with out crashing. ...actually, there are no guarantees of any kind with any version of BPS but the development version is likely to be less stable than the release version.

