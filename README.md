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