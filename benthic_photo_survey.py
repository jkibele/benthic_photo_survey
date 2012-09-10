import glob
import os
import wx
from wx.lib.pubsub import Publisher
from photo_tagging import *



class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.exif_data_staticbox = wx.StaticBox(self, -1, "Exif Data")
        self.subst_selector_box_staticbox = wx.StaticBox(self, -1, "Substrate Selector")
        self.photo_info_staticbox = wx.StaticBox(self, -1, "Photo Info")
        
        # Menu Bar
        self.frame_1_menubar = wx.MenuBar()
        self.file_menu = wx.Menu()
        self.load_gps_log = wx.MenuItem(self.file_menu, wx.NewId(), "Load GPS log", "", wx.ITEM_NORMAL)
        self.file_menu.AppendItem(self.load_gps_log)
        self.load_depth_log = wx.MenuItem(self.file_menu, wx.NewId(), "Load Depth log", "", wx.ITEM_NORMAL)
        self.file_menu.AppendItem(self.load_depth_log)
        self.load_photos = wx.MenuItem(self.file_menu, wx.NewId(), "Load Photos", "", wx.ITEM_NORMAL)
        self.file_menu.AppendItem(self.load_photos)
        self.frame_1_menubar.Append(self.file_menu, "File")
        self.SetMenuBar(self.frame_1_menubar)
        # Menu Bar end
        self.bitmap_1 = wx.StaticBitmap(self, -1, wx.Bitmap("/home/jkibele/Pictures/ArchiteuthisVoyageMap_med.jpg", wx.BITMAP_TYPE_ANY))
        #img = wx.EmptyImage(self.photoMaxSize,self.photoMaxSize)
        #self.bitmap_1 = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(img))
        self.Prev = wx.Button(self, -1, "< Prev")
        self.Next = wx.Button(self, -1, "Next >")
        self.directory = wx.StaticText(self, -1, "Directory: /usr/blah/porkchop/blah/doink/doink")
        self.filename = wx.StaticText(self, -1, "filename.jpg")
        self.photo_num = wx.StaticText(self, -1, "1 of 23", style=wx.ALIGN_RIGHT)
        self.position = wx.StaticText(self, -1, "Position:", style=wx.ALIGN_RIGHT)
        self.coords = wx.StaticText(self, -1, "-36  45.456'\n145  23.456'")
        self.depth_label = wx.StaticText(self, -1, "Depth:", style=wx.ALIGN_RIGHT)
        self.dep = wx.StaticText(self, -1, "12.765 m")
        self.temp_label = wx.StaticText(self, -1, "Temperature:", style=wx.ALIGN_RIGHT)
        self.temp = wx.StaticText(self, -1, "16.23 C")
        self.subst_label = wx.StaticText(self, -1, "Substrate:")
        self.substrate = wx.StaticText(self, -1, "Turf")
        self.substSelector = wx.ListBox(self, -1, choices=["Sand", "Turf", "Barrens", "Mixed Weed", "Kelp Forest", "Other"])
        self.subst_selector_text = wx.StaticText(self, -1, "Double click to set substrate type", style=wx.ALIGN_CENTRE)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("Benthic Photo Survey")
        self.substSelector.SetMinSize((150, 150))
        self.substSelector.SetSelection(0)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        mainSizer = wx.FlexGridSizer(0,2,5,5)
        mainSizer.AddGrowableRow(0, 0)
        #rightColumn = wx.BoxSizer(wx.VERTICAL)
        rightColumn = wx.FlexGridSizer(4,0)
        rightColumn.Add((10,20),0,0,0)
        subst_selector_box = wx.StaticBoxSizer(self.subst_selector_box_staticbox, wx.VERTICAL)
        exif_data = wx.StaticBoxSizer(self.exif_data_staticbox, wx.HORIZONTAL)
        exif_grid = wx.FlexGridSizer(4, 2, 5, 5)
        photo_info = wx.StaticBoxSizer(self.photo_info_staticbox, wx.VERTICAL)
        #filename_and_count = wx.BoxSizer(wx.HORIZONTAL)
        leftColumn = wx.BoxSizer(wx.VERTICAL)
        button_holder = wx.BoxSizer(wx.HORIZONTAL)
        leftColumn.Add(self.bitmap_1, 0, wx.ALL|wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL, 20)
        leftColumn.Add((550, 20), 0, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 0)
        button_holder.Add(self.Prev, 0, wx.BOTTOM|wx.ALIGN_BOTTOM, 20)
        button_holder.Add((300, 20), 0, wx.ALIGN_BOTTOM, 0)
        button_holder.Add(self.Next, 0, wx.BOTTOM|wx.ALIGN_BOTTOM, 20)
        leftColumn.Add(button_holder, 1, wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL, 0)
        mainSizer.Add(leftColumn, 1, wx.EXPAND, 0)
        photo_info.Add(self.directory, 0, wx.ALL, 5)
        photo_info.Add(self.filename, 0, wx.ALL, 5)
        photo_info.Add(self.photo_num, 0, wx.ALL, 5)
        #filename_and_count.Add(self.filename, 0, wx.ALL, 5)
        #filename_and_count.Add(self.photo_num, 0, wx.ALL|wx.ALIGN_RIGHT, 5)
        #photo_info.Add(filename_and_count, 1, wx.EXPAND, 0)
        rightColumn.Add(photo_info, 1, wx.ALL|wx.EXPAND|wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL, 5)
        exif_grid.Add(self.position, 0, wx.ALIGN_RIGHT, 0)
        exif_grid.Add(self.coords, 0, 0, 0)
        exif_grid.Add(self.depth_label, 0, wx.ALIGN_RIGHT, 0)
        exif_grid.Add(self.dep, 0, 0, 0)
        exif_grid.Add(self.temp_label, 0, wx.ALIGN_RIGHT, 0)
        exif_grid.Add(self.temp, 0, 0, 0)
        exif_grid.Add(self.subst_label, 0, wx.ALIGN_RIGHT, 0)
        exif_grid.Add(self.substrate, 0, 0, 0)
        exif_data.Add(exif_grid, 1, wx.ALL|wx.EXPAND, 5)
        rightColumn.Add(exif_data, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5)
        subst_selector_box.Add(self.substSelector, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        subst_selector_box.Add(self.subst_selector_text, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        rightColumn.Add(subst_selector_box, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5)
        mainSizer.Add(rightColumn, 1, 0, 0)
        self.SetSizer(mainSizer)
        mainSizer.Fit(self)
        self.Layout()
        # end wxGlade

# end of class MyFrame


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = MyFrame(None, -1, "Benthic Photo Survey")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()
