This repository contains a set of automatic VST synthesizer programmers, as described in:

"Automatic Programming of VST Sound Synthesizers using Deep Networks and Other Techniques"  
IEEE TRANSACTIONS ON EMERGING TOPICS IN COMPUTATIONAL INTELLIGENCE  
Matthew Yee-King, Leon Fedden, and Mark d'Inverno

This code was developed by Leon Fedden under supervision by Matthew Yee-King.

This fork try to improve and update the original project.  

---  
# RenderMan Compilation
## Windows
### Prerequisites

You need to install the Boost C++ library. You can follow the instructions on their website to install it on Windows:  
[https://www.boost.org/doc/libs/1_85_0/more/getting_started/windows.html](https://www.boost.org/doc/libs/1_85_0/more/getting_started/windows.html)

Then compile boost using the following commands in boost directory:
```./bootstrap.bat vc143```  
```./b2 --build-type=complete --prefix=C:\Boost install```  

### Visual Studio Build
You can now open the solution (*located in Renderman/Builds*) using the latest Visual Studio version and build the project.  
  
Once the solution is opened go to *Project -> Properties* then in *VC++ directories* and chang the paths in *Library directories* to target boost and python libraries on your system.  
  
Then, do the same in the *C/C++* tab in *Other include directories* to target boost and python include folders on your system.

### MacOs build

Check to have the latests MacOs version. I've tested Sonoma 14.5 (may 2024).
It is important also to match this version with the correponding XCode version. 
For Sonoma 14.5 I have Xcode 15.4.

RenderMan has the following dependences:

- VST SDK 2.4: source code to compile with access to VST 2.4 by JUCE (instead of VST3)
- Python : need the latest Python development library
- boost_python : this library from Boost Org, facilitate the inclusion of C++ 

#### VST DSK 2.4
Because the Python apps of deepvstprogrammers still use VST2 with RenderMan instead of VST3, it is necessary to upload VST SDK 2.4.
Get it from : 

	https://github.com/R-Tur/VST_SDK_2.4

Set the directory VST_SDK_2.4 **at the same directory level** than the directory deepvstprogrammers.

#### Python

You can use Python installed for MacOS, but yiy do not have the latests version.
With Sonoman 14.5 the localisation of pyhton is :

	/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/Headers

I think it is installed with XCode.

If you prefer the latest Python the simplest is to get it using brew.
First, update and upgrade brew, and have a cofee, beacause it may spend a long time:

	brew update
	brew upgrade

The install the latest Python3 release:

	brew install python3
	
Then the localisation of the new version is :

	/usr/local/Cellar/python@3.12/3.12.3/Frameworks/Python.framework/Headers

Install also boost C++ library:

 	brew install boost
	brew install boost-python3


To compile RenderMan, go on Renderman/Builds/MacOSX/build and open RenderMan.xcodeproj.
On Xcode, select on to left the RenderMan Dynamic Library and check the following on the **Build Setting** pannel :

- On **Search Paths**, at **Header Search Paths** remove the previous path to python header (ex: /usr/include/python2.7) and set either one of the two previous paths, depending if you use the installed Xcode Python or the one installed by brew.

- Again at **Header Search Paths**, set the boost include path ```/usr/local/Cellar/boost/1.85.0/include```.

- Again at **Header Search Paths**, if you locate VST_SDK_2.4 at the same level of the project, add the following path: ```$(SRCROOT)/../../../../VST_SDK_2.4```. Note that ```$(SRCROOT)```refers to the location of the ```RenderMan.xcodeproj```file.

- On **Search Paths**, at **Library Search Paths** configure the path to find the compiled libraries ```python3```. For exemple if you use ```brew``` version add the paths ```/usr/local/Cellar/python@3.12/3.12.3/Frameworks/Python.framework/Versions/3.12/lib```for the file ```libpython3.12.dylib```.

- Again at **Library Search Paths** add the path to ```boost-python3```lib for exemple the path ```/usr/local/Cellar/boost-python3``` set to ```recursive```

- Select the library to link on **Linking - General** at **Other Linker Flags**, and name the lib file to kink (without "lib" prefix and extensionb. Ex.: ```-lpython3.12 -lboost_python312```


