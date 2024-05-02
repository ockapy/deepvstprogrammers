# Easy install with Docker
To install the project with docker you need to build a docker image using the dockerfile:  
`docker build . -t IMAGE_NAME`  
Then you can start the container using this command:  
`docker run -it IMAGE_NAME bash`  
  
The compilation of renderman is not automatic you need to do it yourself (will be changed soon):  
```bash 
mv /RenderMan/Builds/LinuxMakefile
make
mv build/librenderman.so ../../../Program/utils
cd ../../../Program
```  
  
If you have a problem like this: `ImportError: libboost_python39.so.1.85.0: cannot open shared object file: No such file or directory`  
run this command: `export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH`
