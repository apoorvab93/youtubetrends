# Information -
Welcome to my kodi add on.
This add on is a plugin type of video add-on.
It fetches the latest sample videos from a webpage and dislays them to the user in kodi
These can then be played from within Kodi itself.
# Code structure 
The addon.py is the code that gets executed when kodi add on is clicked in the KODI UI
# Addon.xml
This is the main description file that explains to Kodi how to execute the plugin.
It has a main section called <addon></addon>. This describes the add-on's name, unique id, version and author details
Within this section, there are 2 main sections
1) <requires> section - This contains the name of all other add-ons that my addon depends on. It can also contain any external libraries that are used by the addon.
2) <extension> section - This contains information about where to start the python code execution and what capabilities are "extended" by this plugin.
In my example the capabilities extended are videos because the plugin displays the top 20 trending videos for us to see
