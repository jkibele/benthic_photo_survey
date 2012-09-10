import glob
import os
import wx
from wx.lib.pubsub import Publisher
from photo_tagging import *

class bpsPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        width, height = wx.DisplaySize()
        self.picPaths = []
        self.currentPicture = 0
        self.totalPictures = 0
        self.photoMaxSize = height - 200
        
    

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.myPanel = bpsPanel(self)
        self.exif_data_staticbox = wx.StaticBox(self.myPanel, -1, "Exif Data")
        self.select_substrate_staticbox = wx.StaticBox(self.myPanel, -1, "Select Substrate")
        self.photo_info_staticbox = wx.StaticBox(self.myPanel, -1, "Photo Info")
        
        Publisher().subscribe(self.updateImages, ("update images"))
        Publisher().subscribe(self.resizeFrame, ("resize"))
        
        # Menu Bar
        self.bps_menubar = wx.MenuBar()
        self.file_menu = wx.Menu()
        self.load_photos = wx.MenuItem(self.file_menu, wx.NewId(), "Load Photos", "", wx.ITEM_NORMAL)
        self.file_menu.AppendItem(self.load_photos)
        self.load_gps = wx.MenuItem(self.file_menu, wx.NewId(), "Load GPS Log", "", wx.ITEM_NORMAL)
        self.file_menu.AppendItem(self.load_gps)
        self.load_depth = wx.MenuItem(self.file_menu, wx.NewId(), "Load Depth Log", "", wx.ITEM_NORMAL)
        self.file_menu.AppendItem(self.load_depth)
        self.file_menu.AppendSeparator()
        self.quit_menu = wx.MenuItem(self.file_menu, wx.ID_EXIT, "Quit", "", wx.ITEM_NORMAL)
        self.file_menu.AppendItem(self.quit_menu)
        self.bps_menubar.Append(self.file_menu, "File")
        self.SetMenuBar(self.bps_menubar)
        # Menu Bar end
        self.btn_geotag = wx.Button(self.myPanel, -1, "Geotag")
        self.btn_depth_tag = wx.Button(self.myPanel, -1, "Depth Temp Tag")
        #self.the_image = wx.StaticBitmap(self.myPanel, -1, wx.Bitmap("/home/jkibele/Pictures/us_in_little_boat.jpg", wx.BITMAP_TYPE_ANY))
        img = wx.EmptyImage(self.myPanel.photoMaxSize,self.myPanel.photoMaxSize)
        self.the_image = wx.StaticBitmap(self.myPanel, wx.ID_ANY, wx.BitmapFromImage(img))
        #print self.the_image.__class__.__name__
        self.btn_prev = wx.Button(self.myPanel, -1, "< Prev")
        self.btn_next = wx.Button(self.myPanel, -1, "Next >")
        self.dir_label = wx.StaticText(self.myPanel, -1, "Directory:")
        self.directory = wx.StaticText(self.myPanel, -1, " ")
        self.filename_label = wx.StaticText(self.myPanel, -1, "Filename:")
        self.filename = wx.StaticText(self.myPanel, -1, " ")
        self.img_num = wx.StaticText(self.myPanel, -1, "0 of 0 in directory")
        self.pos_label = wx.StaticText(self.myPanel, -1, "Position:")
        self.position = wx.StaticText(self.myPanel, -1, " \n ")
        self.depth_label = wx.StaticText(self.myPanel, -1, "Depth:")
        self.depth = wx.StaticText(self.myPanel, -1, " ")
        self.temp_label = wx.StaticText(self.myPanel, -1, "Temperature:")
        self.temperature = wx.StaticText(self.myPanel, -1, " ")
        self.subst_label = wx.StaticText(self.myPanel, -1, "Substrate:")
        self.substrate = wx.StaticText(self.myPanel, -1, " ")
        self.substSelector = wx.ListBox(self.myPanel, -1, choices=["Sand", "Turf", "Barrens", "Mixed Weed", "Kelp Forest", "Other"])
        self.substSelectLabel = wx.StaticText(self.myPanel, -1, "Double click to set substrate value.")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_MENU, self.loadPhotos, self.load_photos)
        self.Bind(wx.EVT_MENU, self.loadGPS, self.load_gps)
        self.Bind(wx.EVT_MENU, self.loadDepth, self.load_depth)
        self.Bind(wx.EVT_MENU, self.appQuit, self.quit_menu)
        self.Bind(wx.EVT_BUTTON, self.geotag, self.btn_geotag)
        self.Bind(wx.EVT_BUTTON, self.depth_tag, self.btn_depth_tag)
        self.Bind(wx.EVT_BUTTON, self.onPrevious, self.btn_prev)
        self.Bind(wx.EVT_BUTTON, self.onNext, self.btn_next)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.setSubstrate, self.substSelector)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("Benthic Photo Survey")
        self.substSelector.SetMinSize((120, 150))
        self.substSelector.SetSelection(0)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        self.ubberSizer = wx.BoxSizer(wx.VERTICAL)
        mainGrid = wx.FlexGridSizer(1, 2, 0, 0)
        rightColumn = wx.FlexGridSizer(3, 1, 0, 0)
        select_substrate = wx.StaticBoxSizer(self.select_substrate_staticbox, wx.VERTICAL)
        exif_data = wx.StaticBoxSizer(self.exif_data_staticbox, wx.HORIZONTAL)
        exif_grid = wx.FlexGridSizer(4, 2, 0, 0)
        photo_info = wx.StaticBoxSizer(self.photo_info_staticbox, wx.VERTICAL)
        self.left_column = wx.BoxSizer(wx.VERTICAL)
        button_holder = wx.BoxSizer(wx.HORIZONTAL)
        upper_button_holder = wx.GridSizer(1, 3, 0, 0)
        upper_button_holder.Add(self.btn_geotag, 0, wx.ALL, 5)
        upper_button_holder.Add(self.btn_depth_tag, 0, wx.ALL, 5)
        self.left_column.Add(upper_button_holder, 1, wx.ALL, 5)
        self.left_column.Add(self.the_image, 0, wx.ALL|wx.CENTER, 5)
        button_holder.Add(self.btn_prev, 0, wx.ALL, 10)
        button_holder.Add((300, 20), 0, wx.ALIGN_CENTER_VERTICAL, 0)
        button_holder.Add(self.btn_next, 0, wx.ALL, 10)
        self.left_column.Add(button_holder, 1, wx.ALIGN_CENTER_HORIZONTAL, 0)
        mainGrid.Add(self.left_column, 1, wx.EXPAND, 0)
        photo_info.Add(self.dir_label, 0, 0, 0)
        photo_info.Add(self.directory, 0, wx.ALIGN_RIGHT, 0)
        photo_info.Add(self.filename_label, 0, wx.TOP, 5)
        photo_info.Add(self.filename, 0, wx.ALIGN_RIGHT, 0)
        photo_info.Add(self.img_num, 0, wx.TOP, 5)
        rightColumn.Add(photo_info, 1, wx.ALL|wx.EXPAND, 5)
        exif_grid.Add(self.pos_label, 0, wx.RIGHT|wx.ALIGN_RIGHT, 5)
        exif_grid.Add(self.position, 0, 0, 0)
        exif_grid.Add(self.depth_label, 0, wx.RIGHT|wx.ALIGN_RIGHT, 5)
        exif_grid.Add(self.depth, 0, 0, 0)
        exif_grid.Add(self.temp_label, 0, wx.RIGHT|wx.ALIGN_RIGHT, 5)
        exif_grid.Add(self.temperature, 0, 0, 0)
        exif_grid.Add(self.subst_label, 0, wx.RIGHT|wx.ALIGN_RIGHT, 5)
        exif_grid.Add(self.substrate, 0, 0, 0)
        exif_data.Add(exif_grid, 1, wx.ALL|wx.EXPAND, 5)
        rightColumn.Add(exif_data, 1, wx.ALL|wx.EXPAND, 5)
        select_substrate.Add(self.substSelector, 0, wx.ALL|wx.EXPAND, 5)
        select_substrate.Add(self.substSelectLabel, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        rightColumn.Add(select_substrate, 1, wx.ALL|wx.EXPAND, 5)
        mainGrid.Add(rightColumn, 1, wx.TOP|wx.EXPAND, 20)
        self.myPanel.SetSizer(mainGrid)
        mainGrid.AddGrowableCol(0)
        self.ubberSizer.Add(self.myPanel, 1, wx.EXPAND, 0)
        self.SetSizer(self.ubberSizer)
        self.ubberSizer.Fit(self)
        self.Layout()
        # end wxGlade

    #----------------------------------------------------------------------
    def loadPhotos(self, event): # wxGlade: MyFrame.<event_handler>
        """
        Opens a DirDialog to allow the user to open a folder with pictures
        """
        dlg = wx.DirDialog(self, "Choose a directory",
                           style=wx.DD_DEFAULT_STYLE)
        
        if dlg.ShowModal() == wx.ID_OK:
            self.folderPath = dlg.GetPath()
            #print self.folderPath
            picPaths = glob.glob(self.folderPath + os.path.sep + "*.JPG")
            picPaths = picPaths + glob.glob(self.folderPath + os.path.sep + "*.jpg") 
            #print picPaths
        Publisher().sendMessage("update images", picPaths)
        event.Skip()

    #----------------------------------------------------------------------
    def loadImage(self, image):
        """"""
        direc, image_name = os.path.split(image)
        self.imf = image_file(image)
        img = wx.Image(image, wx.BITMAP_TYPE_ANY)
        # scale the image, preserving the aspect ratio
        W = img.GetWidth()
        H = img.GetHeight()
        if W > H:
            NewW = self.myPanel.photoMaxSize
            NewH = self.myPanel.photoMaxSize * H / W
        else:
            NewH = self.myPanel.photoMaxSize
            NewW = self.myPanel.photoMaxSize * W / H
        img = img.Scale(NewW,NewH)
        # the image
        self.the_image.SetBitmap(wx.BitmapFromImage(img))
        # photo info
        self.filename.SetLabel(image_name)
        self.directory.SetLabel(direc)
        num_str = "%i of %i" % (self.myPanel.currentPicture + 1,self.myPanel.totalPictures)
        self.img_num.SetLabel(num_str)
        # exif data
        self.loadExif()
        
        self.Refresh()
        Publisher().sendMessage("load grid", image)
        Publisher().sendMessage("load list", image)
        Publisher().sendMessage("resize", "")
        
    #----------------------------------------------------------------------
    def loadExif(self):
        self.position.SetLabel( self.imf.position.__str__().replace(',','\n') )
        if self.imf.exif_depth:
            dstr = str(self.imf.exif_depth) + " m"
        else:
            dstr = 'None'
        self.depth.SetLabel( dstr )
        if self.imf.xmp_temperature:
            tstr = str(self.imf.xmp_temperature) + ' ' + self.imf.xmp_temp_units
        else:
            tstr = 'None'
        self.temperature.SetLabel( tstr )
        self.substrate.SetLabel( self.imf.xmp_substrate )
        
        self.substrate.Refresh()
        
    #----------------------------------------------------------------------
    def nextPicture(self):
        """
        Loads the next picture in the directory
        """
        if self.myPanel.currentPicture == self.myPanel.totalPictures-1:
            self.myPanel.currentPicture = 0
        else:
            self.myPanel.currentPicture += 1
        self.loadImage(self.myPanel.picPaths[self.myPanel.currentPicture])
        
    #----------------------------------------------------------------------
    def previousPicture(self):
        """
        Displays the previous picture in the directory
        """
        if self.myPanel.currentPicture == 0:
            self.myPanel.currentPicture = self.myPanel.totalPictures - 1
        else:
            self.myPanel.currentPicture -= 1
        self.loadImage(self.myPanel.picPaths[self.myPanel.currentPicture])
        
    #----------------------------------------------------------------------
    def update(self, event):
        """
        Called when the slideTimer's timer event fires. Loads the next
        picture from the folder by calling th nextPicture method
        """
        self.nextPicture()
        
    #----------------------------------------------------------------------
    def updateImages(self, msg):
        """
        Updates the picPaths list to contain the current folder's images
        """
        self.myPanel.picPaths = msg.data
        self.myPanel.totalPictures = len(self.myPanel.picPaths)
        self.loadImage(self.myPanel.picPaths[0])
        
    #----------------------------------------------------------------------
    def onNext(self, event):
        """
        Calls the nextPicture method
        """
        self.nextPicture()
    
    #----------------------------------------------------------------------
    def onPrevious(self, event):
        """
        Calls the previousPicture method
        """
        self.previousPicture()
        
    #----------------------------------------------------------------------
    def resizeFrame(self, msg):
        """"""
        self.ubberSizer.Fit(self)

    def loadGPS(self, event): # wxGlade: MyFrame.<event_handler>
        print "Event handler `loadGPS' not implemented!"
        event.Skip()

    def loadDepth(self, event): # wxGlade: MyFrame.<event_handler>
        print "Event handler `loadDepth' not implemented!"
        event.Skip()

    def appQuit(self, event): # wxGlade: MyFrame.<event_handler>
        print "Event handler `appQuit' not implemented!"
        event.Skip()

    def geotag(self, event): # wxGlade: MyFrame.<event_handler>
        print "Event handler `geotag' not implemented!"
        event.Skip()

    def depth_tag(self, event): # wxGlade: MyFrame.<event_handler>
        print "Event handler `depth_tag' not implemented!"
        event.Skip()

    def setSubstrate(self, event): # wxGlade: MyFrame.<event_handler>
        index = event.GetSelection()
        chosen_substrate = self.substSelector.GetString(index)
        self.imf.set_xmp_substrate(chosen_substrate)
        self.loadExif()
        event.Skip()

# end of class MyFrame


if __name__ == "__main__":
    benthicPS = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    benthic_photo_survey = MyFrame(None, -1, "")
    benthicPS.SetTopWindow(benthic_photo_survey)
    benthic_photo_survey.Show()
    benthicPS.MainLoop()
