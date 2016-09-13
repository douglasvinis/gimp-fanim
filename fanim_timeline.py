#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
  Copyright (C) 2016, Douglas Knowman
  douglasknowman@gmail.com

  Distributed under the terms of GNU GPL v3 (or lesser GPL) license.

FAnim
Timeline

"""
from gimpfu import gimp,pdb
import pygtk
pygtk.require('2.0')
import gtk
import numpy

WINDOW_TITLE = "GIMP FAnim Timeline [%s]"

class Utils:
    @staticmethod
    def button_stock(stock,size):
        """
        Return a button with a image from stock items 
        """
        b = gtk.Button()
        img = gtk.Image()
        img.set_from_stock(stock,size)
        b.set_image(img)
        return b

    @staticmethod
    def toggle_button_stock(stock,size):
        """
        Return a button with a image from stock items 
        """
        b = gtk.ToggleButton()
        img = gtk.Image()
        img.set_from_stock(stock,size)
        b.set_image(img)
        return b

class AnimFrame(gtk.EventBox):
    def __init__(self,layer,width=100,height=120):
        gtk.EventBox.__init__(self)
        self.set_size_request(width,height)
        #variables
        self.thumbnail = None
        self.label = None
        self.layer = layer

        self._setup()

    def _setup(self):
        self.thumbnail = gtk.Image()
        self.label = gtk.Label(self.layer.name)

        frame = gtk.Frame()
        layout = gtk.VBox()
        # add frame to this widget
        self.add(frame)

        # add layout manager to the frame
        frame.add(layout)

        layout.pack_start(self.label)
        layout.pack_start(self.thumbnail)
        self._get_thumb_image()

    def _get_thumb_image(self):
        width = 100
        height = 100
        image_data = pdb.gimp_drawable_thumbnail(self.layer,width,height)
        w,h,c = image_data[0],image_data[1],image_data[2]
        # create a 2d array to store the organized data.
        p2d = [[[0 for z in range(c)] for x in range(w)] for y in range(h)]

        # looping through all pixels of the thumbnail and organize it.
        x = y = z = 0
        for i in range(image_data[3]):
            p2d[y][x][z] = image_data[4][i]
            z += 1
            if z >= c:
                z = 0
                x += 1
                if x >= w:
                    x = 0
                    y += 1
        ##
        image_array = numpy.array(p2d,dtype=numpy.uint8)
        pixbuf = gtk.gdk.pixbuf_new_from_array(image_array,gtk.gdk.COLORSPACE_RGB,8)
        self.thumbnail.set_from_pixbuf(pixbuf)

    def update_layer_info(self):
        self._get_thumb_image()


class Timeline(gtk.Window):
    def __init__(self,title,image):
        gtk.Window.__init__(self,gtk.WINDOW_TOPLEVEL)

        self.set_title(title)
        self.image = image
        self.frame_bar = None
        # variables
        self.is_playing = False
        self.is_replay = False
        # modifiable widgets
        self.play_button_images = []
        self.widgets_to_disable = []
        
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
        cbar.pack_start(self._setup_playbackbar(),False,False,10)
        cbar.pack_start(self._setup_editbar(),False,False,10)
        cbar.pack_start(self._setup_timebar(),False,False,10)
        cbar.pack_start(self._setup_onionskin(),False,False,10)
        cbar.pack_start(self._setup_generalbar(),False,False,10)

        # frames bar widgets
        self.frame_bar = gtk.HBox()
        scroll_window = gtk.ScrolledWindow()
        scroll_window.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
        scroll_window.add_with_viewport(self.frame_bar)
        scroll_window.set_size_request(-1,140)

        # mount the widgets together
        base.pack_start(cbar,False,False,0)
        base.pack_start(scroll_window,True,True,0)
        self.add(base)
        
        # catch all layers
        self._scan_image_layers()

        # finalize showing all widgets
        self.show_all()

    def _scan_image_layers(self):
        layers = self.image.layers
        layers.reverse()
        for layer in layers:
            f = AnimFrame(layer)
            self.frame_bar.pack_start(f,False,True,2)

    def _setup_playbackbar(self):
        playback_bar = gtk.HBox()
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
        b_play = gtk.Button()
        b_play.set_image(image_play)
        b_play.set_size_request(button_size,button_size)

        b_tostart = Utils.button_stock(gtk.STOCK_MEDIA_PREVIOUS,stock_size)
        b_toend = Utils.button_stock(gtk.STOCK_MEDIA_NEXT,stock_size)
        b_prev = Utils.button_stock(gtk.STOCK_MEDIA_REWIND,stock_size)
        b_next = Utils.button_stock(gtk.STOCK_MEDIA_FORWARD,stock_size)

        b_repeat = Utils.toggle_button_stock(gtk.STOCK_REFRESH,stock_size)

        # connecting the button with callback
        b_play.connect('clicked',self.on_toggle_play)
        b_repeat.connect('toggled',self.on_replay)

        # add to the disable on play list
        w = [b_repeat,b_prev,b_next,b_tostart,b_toend]
        map(lambda x: self.widgets_to_disable.append(x),w)

        # set the tooltips
        b_play.set_tooltip_text("Animation play/pause")
        b_repeat.set_tooltip_text("Animation replay active/deactive")
        b_prev.set_tooltip_text("To the previous frame")
        b_next.set_tooltip_text("To the next frame")
        b_tostart.set_tooltip_text("To the start frame")
        b_toend.set_tooltip_text("To the end frame")
        
        # packing everything in gbar
        playback_bar.pack_start(b_tostart,False,False,0)
        playback_bar.pack_start(b_prev,False,False,0)
        playback_bar.pack_start(b_play,False,False,0)
        playback_bar.pack_start(b_next,False,False,0)
        playback_bar.pack_start(b_toend,False,False,0)
        playback_bar.pack_start(b_repeat,False,False,0)

        return playback_bar

    def _setup_editbar(self):
        stock_size = gtk.ICON_SIZE_BUTTON
        edit_bar = gtk.HBox()
        
        b_back = Utils.button_stock(gtk.STOCK_GO_BACK,stock_size)
        b_forward = Utils.button_stock(gtk.STOCK_GO_FORWARD,stock_size)
        b_rem = Utils.button_stock(gtk.STOCK_REMOVE,stock_size)
        b_add = Utils.button_stock(gtk.STOCK_ADD,stock_size)

        # add to the disable on play list
        w = [b_back,b_forward,b_rem,b_add]
        map(lambda x: self.widgets_to_disable.append(x),w)

        # packing everything in gbar
        map(lambda x: edit_bar.pack_start(x,False,False,0),w)

        return edit_bar

    def _setup_timebar(self):
        stock_size = gtk.ICON_SIZE_BUTTON
        time_bar = gtk.HBox()

        b_time = Utils.button_stock(gtk.STOCK_PROPERTIES,stock_size)

        self.widgets_to_disable.append(b_time)

        time_bar.pack_start(b_time,False,False,0)
        return time_bar

    def _setup_onionskin(self):
        stock_size = gtk.ICON_SIZE_BUTTON
        button_size = 30
        onionskin_bar = gtk.HBox()

        # active onionskin
        b_active = Utils.toggle_button_stock(gtk.STOCK_DND_MULTIPLE,stock_size)

        # onionskin config
        b_conf = Utils.button_stock(gtk.STOCK_PROPERTIES,stock_size)

        # add to the disable on play list
        w = [b_active,b_conf]
        map(lambda x: self.widgets_to_disable.append(x),w)

        # packing everything in gbar
        map(lambda x: onionskin_bar.pack_start(x,False,False,0),w)

        return onionskin_bar

    def _setup_generalbar(self):
        stock_size = gtk.ICON_SIZE_BUTTON
        general_bar = gtk.HBox()

        b_about = Utils.button_stock(gtk.STOCK_ABOUT,stock_size)
        b_export = Utils.button_stock(gtk.STOCK_CONVERT,stock_size)
        b_quit = Utils.button_stock(gtk.STOCK_QUIT,stock_size)

        # callbacks
        b_quit.connect('clicked',self.destroy)

        # add to the disable on play list
        w = [b_about, b_export, b_quit]
        map(lambda x: self.widgets_to_disable.append(x),w)

        # packing everything in gbar
        map(lambda x: general_bar.pack_start(x,False,False,0),w)

        return general_bar

#----------------------Callback Functions----------------#

    def on_toggle_play(self,widget):
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
        for w in self.widgets_to_disable:
            w.set_sensitive(not self.is_playing)

    def on_replay(self,widget):
        self.is_replay = widget.get_active()
        print (self.is_replay)

def timeline_main(image,drawable):
    global WINDOW_TITLE
    WINDOW_TITLE = WINDOW_TITLE % (image.name)
    win = Timeline(WINDOW_TITLE,image)
    win.start()
