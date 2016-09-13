#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
  Copyright (C) 2016, Douglas Knowman
  douglasknowman@gmail.com

  Distributed under the terms of GNU GPL v3 (or lesser GPL) license.

FAnim
Timeline

"""
from gimpfu import gimp
import pygtk
pygtk.require('2.0')
import gtk

WINDOW_TITLE = "GIMP FAnim Timeline [%s]"

class Timeline(gtk.Window):
    def __init__(self,title):
        gtk.Window.__init__(self,gtk.WINDOW_TOPLEVEL)

        self.set_title(title)
        # variables
        self.is_playing = False
        self.is_replay = False
        # modifiable widgets
        self.play_button_images = []
        
        self._setup_widgets()

    def destroy(self,widget):
        gtk.main_quit()

    def start(self):
        gtk.main()

    def _setup_widgets(self):
        """
        create all the window staticaly placed widgets.
        """
        # basic window definitions
        self.connect("destroy",self.destroy)
        self.set_default_size(400,140)
        self.set_keep_above(True)

        # start creating basic layout
        base = gtk.VBox()

        # commands bar widgets
        cbar = gtk.HBox()
        cbar.pack_start(self._setup_playbackbar(),False,False,0)
        #cbar.pack_start(self._setup_timebar(cbar))
        #cbar.pack_start(self._setup_generalbar(cbar))

        # frames bar widgets
        fbar = gtk.HBox()
        #fbar.pack_start(self._setup_framebar)

        # mount the widgets together
        base.pack_start(cbar,False,False,0)
        base.pack_start(fbar)
        self.add(base)
        
        # finalize showing all widgets
        self.show_all()

    def _setup_playbackbar(self):
        pbar = gtk.HBox()
        button_size = 30
        stock_size = gtk.ICON_SIZE_BUTTON

        # play button
        ## image
        image_play = gtk.Image()
        image_play.set_from_stock(gtk.STOCK_MEDIA_PLAY,stock_size)
        image_pause = gtk.Image()
        image_pause.set_from_stock(gtk.STOCK_MEDIA_PAUSE,stock_size)
        ## append the images to a list to be used later on
        self.play_button_images.append(image_play)
        self.play_button_images.append(image_pause)
        ## button
        playb = gtk.Button()
        playb.set_image(image_play)
        playb.set_size_request(button_size,button_size)

        # to start frame button
        image_tostart = gtk.Image()
        image_tostart.set_from_stock(gtk.STOCK_MEDIA_PREVIOUS,stock_size)
        tsb = gtk.Button()
        tsb.set_image(image_tostart)
        tsb.set_size_request(button_size,button_size)

        # to start frame button
        image_toend = gtk.Image()
        image_toend.set_from_stock(gtk.STOCK_MEDIA_NEXT,stock_size)
        teb = gtk.Button()
        teb.set_image(image_toend)
        teb.set_size_request(button_size,button_size)

        # next/prev frame buttons
        image_prev = gtk.Image()
        image_prev.set_from_stock(gtk.STOCK_MEDIA_REWIND,stock_size)
        image_next = gtk.Image()
        image_next.set_from_stock(gtk.STOCK_MEDIA_FORWARD,stock_size)

        nb = gtk.Button()
        nb.set_image(image_next)
        nb.set_size_request(button_size,button_size)

        pb = gtk.Button()
        pb.set_image(image_prev)
        pb.set_size_request(button_size,button_size)

        # repeat button
        image_prev = gtk.Image()
        image_prev.set_from_stock(gtk.STOCK_REFRESH,stock_size)
        rb = gtk.ToggleButton()
        rb.set_image(image_prev)
        rb.set_size_request(button_size,button_size)

        # connecting the button with callback
        playb.connect('clicked',self.on_toggle_play,pbar)
        rb.connect('toggled',self.on_replay)

        # set the tooltips
        playb.set_tooltip_text("Animation play/pause")
        rb.set_tooltip_text("Animation replay active/deactive")
        pb.set_tooltip_text("To the previous frame")
        nb.set_tooltip_text("To the next frame")
        tsb.set_tooltip_text("To the start frame")
        teb.set_tooltip_text("To the end frame")

        
        # packing all widgets
        pbar.pack_start(tsb,False,False,0) # to start button
        pbar.pack_start(pb,False,False,0) # previous frame
        pbar.pack_start(playb,False,False,0) # play stop
        pbar.pack_start(nb,False,False,0) # next frame
        pbar.pack_start(teb,False,False,0) # to end button
        pbar.pack_start(rb,False,False,0) # repeat button

        return pbar

    def _setup_timebar(self):
        return None
    def _setup_generalbar(self):
        return None

#----------------------Callback Functions----------------#

    def on_toggle_play(self,widget,pbar):
        """
        This method will change the animation play state,
        change the button image and will disable/enable the other buttons
        interation.
        for that they need 2 image which is stored in self.play_button_images
        variable.
        """
        self.is_playing = not self.is_playing
        if self.is_playing:
            widget.set_image(self.play_button_images[1])
        else :
            widget.set_image(self.play_button_images[0])

        # loop through all playback bar children to disable interation.
        for child in pbar.children():
            if child == widget: continue # avoid disable the play button itself.
            child.set_sensitive(not self.is_playing)

    def on_replay(self,widget):
        self.is_replay = widget.get_active()
        print (self.is_replay)

def timeline_main(image,drawable):
    global WINDOW_TITLE
    WINDOW_TITLE = WINDOW_TITLE % (image.name)
    win = Timeline(WINDOW_TITLE)
    win.start()
