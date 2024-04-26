This repository contains a set of automatic VST synthesizer programmers, as described in:

"Automatic Programming of VST Sound Synthesizers using Deep Networks and Other Techniques"  
IEEE TRANSACTIONS ON EMERGING TOPICS IN COMPUTATIONAL INTELLIGENCE  
Matthew Yee-King, Leon Fedden, and Mark d'Inverno

This code was developed by Leon Fedden under supervision by Matthew Yee-King.

## RenderMan Compilation

To compile RenderMan, we need to make some adjustments to the program.

### Windows

If you are on Windows, you can open the solution *in Builds/VisualStudio2019/RenderMan.sln* using Visual Studio 2019 or newer versions.

#### Prerequisites

For it to work properly, you will need to install Windows SDK 8.1, which you can find here:  
[https://developer.microsoft.com/en-us/windows/downloads/sdk-archive/](https://developer.microsoft.com/en-us/windows/downloads/sdk-archive/#:~:text=Downloads-,Windows%208.1%20SDK,-Released%20in%20October)

Next, you need to install the Boost C++ library. You can follow the instructions on their website to install it on Windows:  
[https://www.boost.org/doc/libs/1_85_0/more/getting_started/windows.html](https://www.boost.org/doc/libs/1_85_0/more/getting_started/windows.html)

Once Boost is installed, for the solution to compile, we need to change some build settings in Visual Studio.

#### Visual Studio Build

First things first, open RenderMan.sln with Visual Studio. Inside Visual Studio, right-click on the solution and go to Properties.

Click on VC++ Repositories, then on the right panel, click on Library Repositories and select Modify.  
Adjust the path to the libraries of Python to fit your Python version.  
If not present, add the path to Boost libraries (should be C:\Boost\lib).  
Then confirm the changes.

Next, in Properties, click the C/C++ tab and General tab.  
Here, you need to change the include directories to add:  
- *Path to Boost*\include\boost*version number*  
- *Path to Python*\include  
And then confirm the changes.

Finally, because Boost doesn't want to mix static and dynamic libraries, you also need to change the preprocessor instructions.  
You can find this in the C/C++ tab and Preprocessor -> Preprocessor Definition.  
You just need to add one line at the end:  
- BOOST_PYTHON_STATIC_LIB

---

Now you should be able to build the solution. Once it's done, go to the build files, copy renderman.dll, paste it in the app/utils folder, and rename it librenderman.pyd.
