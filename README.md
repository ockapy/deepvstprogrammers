This repository contains a set of automatic VST synthesizer programmers, as described in 

Automatic Programming of VST Sound Synthesizers using Deep Networks and Other Techniques
IEEE TRANSACTIONS ON EMERGING TOPICS IN COMPUTATIONAL INTELLIGENCE
Matthew Yee-king, Leon Fedden and Mark d'Inverno

This code was developed by Leon Fedden under supvision by Matthew Yee-King


## RenderMan compilation
To compile RenderMan we need some adjustment to the program.  

### Windows
If you are on Windows you can open the solution *in Builds/VisualStudion2019/RenderMan.sln* using Visual Studio 2019 or newer versions.

#### Prerequisites
For it to work properly you will need to install Windows SDK 8.1 that you can found here:  
[https://developer.microsoft.com/en-us/windows/downloads/sdk-archive/](https://developer.microsoft.com/en-us/windows/downloads/sdk-archive/#:~:text=Downloads-,Windows%208.1%20SDK,-Released%20in%20October)  
  
Next you need to install boost C++ library you can follow the instructions on their website to install on Windows:  
https://www.boost.org/doc/libs/1_85_0/more/getting_started/windows.html  
  
Once boost is installed, for the solution to compile we need to change some build settings in Visual Studio.  

#### Visual Studio build
First thing first, open RenderMan.sln with Visual Studio. 
Inside Visual Studio, right click on the solution and go to Properties.  
  
Click on VC++ repositories then on the right panel click on library repositories and select modify.  
The path to the libraries of python to fit your python version.  
And if not present add the path to boost libraries (should be C:\Boost\lib).  
Then confirm the changes.  
  
Next in properties click the C/C++ tab and General tab.  
Here You need to change the include repertories to add:  
- *Path to Boost*\include\boost*version number*
- *Path to python*\include   
  
And then confirm the changes.  
  
Finaly, because boost don't want to mix static and dynamic libraries you also need to change the preprocessor instructions.  
You can find this in C/C++ tab and preprocessor -> preprocessor definition.  
You just need to add one line at the end:  
- BOOST_PYTHON_STATIC_LIB
  
---  




 
