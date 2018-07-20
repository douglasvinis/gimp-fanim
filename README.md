__GIMP Frame by Frame Animation Tool (FAnim)__  

FAnim is an GIMP plugin that creates a simple timeline to help create frame by frame animations based on layers.  
![alt tag](https://i.imgur.com/S9rX2tu.png)  

**If you have found a good use to this piece of software that is wrote by me, you may recognize the hard
work behind it assisting me with a donation, so i can continue doing it better and better.  
Thank You!**  

<p align="center">
<a href="https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=JMF3ZCEPBRTY4&lc=US&item_name=douglasvini&currency_code=USD&bn=PP%2dDonationsBF%3abtn_donateCC_LG%2egif%3aNonHosted">
<img src="https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif"></img>
</a>
</p>

__Features:__  
* Full set of buttons to help visualize each frame, move and create.
* Play the animations on gimp own canvas.
* Dynamic onionskin functionality with backward and forward depth level adjustment.
* Fixed view frames functionality, that let you create background and foreground parts that stay visible.
* Adjustable framerate.
* Settings are remembered.
* Two format converters, that converts to redy to export gif and spritesheet format.

__Known issues:__  
* Possible gtk performance problems on windows.  
* Performance problems with big images.  

__Instalation:__  
You can copy the fanim.py into you gimp plugin directory.  
If you are in a unix based system, you need to give execution permission to the file,  
the command `chmod +x fanim.py` will do it.

The path is shown below.  

*gimp-2.9 and below*  
Linux: ~/.gimp-[version]/plug-ins/  
Windows: %HOMEPATH%\.gimp-[version]\plug-ins\  

*gimp-2.10*  
Linux: ~/.config/GIMP/2.10/plug-ins/  
Windows: %HOMEPATH%\AppData\Roaming\GIMP\2.10\plug-ins\  

with the files in the correct place you can open GIMP, if everything is alright you
will see in the menubar the "FAnim" menu.  

__Download__  
You can download the zip file ["here"](https://github.com/douglasvini/gimp-fanim/archive/master.zip).
