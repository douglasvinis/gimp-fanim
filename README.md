__GIMP Frame Animation Tool (FAnim)__  

FAnim is a GIMP plugin to help on frame by frame animation.   
![alt tag](http://i.imgur.com/O5LhTH7.png)  

__Features:__  
-Frame Timeline, based on layers. [DONE]  
-Play the animation on screen, without the need of open a new window. [DONE]  
-dynamic onionskin backward and forward with adjustable depth level. [DONE]  
-format to spritesheet.  [WIP]  
-format to gif. [DONE]  
-frames with fixed visibility (backgrounds & foregrounds) [DONE]  
-adjustable framerate. [DONE]  
-consistent settings. [DONE]  
  
__Know issues:__  
-possible gtk performance problems on windows.  
-performance problems with big images.  
-incomplete undo/rendo sync with GIMP.  
  
__Instalation:__  
you can copy the fanim.py and fanim_timeline.py into you gimp plugin directory
the path is shown below.  
  
Linux: ~/.gimp-[version]/plug-ins/  
Mac: $HOME/Library/Application Support/Gimp/[version]/plug-ins/  
Windows: %HOMEPATH%\.gimp-[version]\plug-ins\  
  
with the files in the correct place you can open GIMP. if everything is alright you 
will see in the tool bar the "FAnim" menu.  
  
__Using:__  
you have to create a new image to start the timeline window,you can open just
one timeline by image. after open it the timeline is ready to work, you can create new 
"frames", delete, select and so on.  
