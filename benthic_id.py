import glob
import os
import wx
import wx.lib.mixins.listctrl as listmix
from wx.lib.pubsub import Publisher
import wx.grid as gridlib
from photo_tagging import *

########################################################################
class SimpleListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition, size=(200,-1), style=wx.LC_REPORT|wx.SUNKEN_BORDER):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        self.Show(True)
        Publisher().subscribe(self.loadImage, ("load list"))
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnDoubleClick)
        choices = ['Barrens','Turf','Kelp','Mixed Weed','Sand','Other']
        self.InsertColumn(0,"Substrate")
        row = 0
        for k in choices:
            pos = self.InsertStringItem(row,k)
            #self.SetItemData(pos, k)
            row += 1
        self.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.Refresh()
        
    def loadImage(self,msg):
        img_path = msg.data
        self.imf = image_file(img_path)
        
    def OnItemSelected(self, event):
        self.currentItem = event.m_itemIndex
        event.Skip()
        
    def OnDoubleClick(self,event):
        chosen_substrate = self.GetItemText(self.currentItem)
        print "OnDoubleClick item %s" % self.GetItemText(self.currentItem)
        self.imf.set_xmp_substrate(chosen_substrate)
        Publisher().sendMessage("load grid", self.imf.file_path)
        event.Skip()

class SimpleGrid(gridlib.Grid): ##, mixins.GridAutoEditMixin):
    def __init__(self, parent ):
        #self.imf = image_file(img_file_path)
        gridlib.Grid.__init__(self, parent, -1)
        
        self.picPaths = []
        self.currentPicture = 0
        self.totalPictures = 0
        
        self.moveTo = None
    
        self.CreateGrid(10, 2)#, gridlib.Grid.SelectRows)
        ##self.EnableEditing(False)
    
        # simple cell formatting
        self.SetColSize(3, 200)
        self.SetRowSize(4, 45)
    
        self.SetColLabelValue(0, "Key")
        self.SetColLabelValue(1, "Value")
    
        self.SetColLabelAlignment(wx.ALIGN_LEFT, wx.ALIGN_BOTTOM)
        Publisher().subscribe(self.loadImage, ("load grid"))
    
    def loadImage(self,msg):
        img_path = msg.data
        print "Load this: %s" % img_path
        imf = image_file(img_path)
        img_dict = {    'Depth': float(imf.exif_depth),
                        'Temp' : imf.xmp_temperature,
                        'Position': imf.position,
                        'Substrate': imf.xmp_substrate,
                        }
        row = 0
        for k,v in img_dict.iteritems():
            self.SetCellValue(row, 0, k)
            self.SetCellValue(row, 1, str(v) )
            row += 1
        self.Refresh()

class ViewerPanel(wx.Panel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)
        
        width, height = wx.DisplaySize()
        self.picPaths = []
        self.currentPicture = 0
        self.totalPictures = 0
        self.photoMaxSize = height - 200
        Publisher().subscribe(self.updateImages, ("update images"))

        self.slideTimer = wx.Timer(None)
        self.slideTimer.Bind(wx.EVT_TIMER, self.update)
        
        self.myGrid = SimpleGrid(self)
        an_id = wx.NewId()
        self.myListCtrl = SimpleListCtrl(self, an_id)
        
        self.layout()
        
    #----------------------------------------------------------------------
    def layout(self):
        """
        Layout the widgets on the panel
        """
        
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.infoSizer = wx.BoxSizer(wx.VERTICAL)
        self.imgGridSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        img = wx.EmptyImage(self.photoMaxSize,self.photoMaxSize)
        self.imageCtrl = wx.StaticBitmap(self, wx.ID_ANY, 
                                         wx.BitmapFromImage(img))
        self.imgGridSizer.Add(self.imageCtrl, 0, wx.ALL|wx.CENTER, 5)
        self.imageLabel = wx.StaticText(self, label="")
        
        self.infoSizer.Add(self.myListCtrl, 0, wx.ALL|wx.CENTER, 5)
        self.infoSizer.Add(self.myGrid, 0, wx.ALL|wx.CENTER, 5)
        
        self.imgGridSizer.Add(self.infoSizer, 0, wx.ALL|wx.CENTER, 5)
        
        self.mainSizer.Add(self.imgGridSizer, 0, wx.ALL|wx.RIGHT, 5)
        
        self.mainSizer.Add(self.imageLabel, 0, wx.ALL|wx.CENTER, 5)
        
        btnData = [("Previous", btnSizer, self.onPrevious),
                   ("Slide Show", btnSizer, self.onSlideShow),
                   ("Next", btnSizer, self.onNext)]
        for data in btnData:
            label, sizer, handler = data
            self.btnBuilder(label, sizer, handler)
            
        self.mainSizer.Add(btnSizer, 0, wx.CENTER)
        self.SetSizer(self.mainSizer)
            
    #----------------------------------------------------------------------
    def btnBuilder(self, label, sizer, handler):
        """
        Builds a button, binds it to an event handler and adds it to a sizer
        """
        btn = wx.Button(self, label=label)
        btn.Bind(wx.EVT_BUTTON, handler)
        sizer.Add(btn, 0, wx.ALL|wx.CENTER, 5)
        
    #----------------------------------------------------------------------
    def loadImage(self, image):
        """"""
        image_name = os.path.basename(image)
        img = wx.Image(image, wx.BITMAP_TYPE_ANY)
        # scale the image, preserving the aspect ratio
        W = img.GetWidth()
        H = img.GetHeight()
        if W > H:
            NewW = self.photoMaxSize
            NewH = self.photoMaxSize * H / W
        else:
            NewH = self.photoMaxSize
            NewW = self.photoMaxSize * W / H
        img = img.Scale(NewW,NewH)

        self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
        self.imageLabel.SetLabel(image_name)
        self.Refresh()
        Publisher().sendMessage("load grid", image)
        Publisher().sendMessage("load list", image)
        Publisher().sendMessage("resize", "")
        
    #----------------------------------------------------------------------
    def nextPicture(self):
        """
        Loads the next picture in the directory
        """
        if self.currentPicture == self.totalPictures-1:
            self.currentPicture = 0
        else:
            self.currentPicture += 1
        self.loadImage(self.picPaths[self.currentPicture])
        
    #----------------------------------------------------------------------
    def previousPicture(self):
        """
        Displays the previous picture in the directory
        """
        if self.currentPicture == 0:
            self.currentPicture = self.totalPictures - 1
        else:
            self.currentPicture -= 1
        self.loadImage(self.picPaths[self.currentPicture])
        
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
        self.picPaths = msg.data
        self.totalPictures = len(self.picPaths)
        self.loadImage(self.picPaths[0])
        
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
    def onSlideShow(self, event):
        """
        Starts and stops the slideshow
        """
        btn = event.GetEventObject()
        label = btn.GetLabel()
        if label == "Slide Show":
            self.slideTimer.Start(3000)
            btn.SetLabel("Stop")
        else:
            self.slideTimer.Stop()
            btn.SetLabel("Slide Show")
        
        
########################################################################
class ViewerFrame(wx.Frame):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="Image Viewer")
        panel = ViewerPanel(self)
        self.folderPath = ""
        Publisher().subscribe(self.resizeFrame, ("resize"))
        
        self.initToolbar()
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        
        self.Show()
        self.sizer.Fit(self)
        self.Center()
        
        
    #----------------------------------------------------------------------
    def initToolbar(self):
        """
        Initialize the toolbar
        """
        self.toolbar = self.CreateToolBar()
        self.toolbar.SetToolBitmapSize((16,16))
        
        open_ico = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, (16,16))
        openTool = self.toolbar.AddSimpleTool(wx.ID_ANY, open_ico, "Open", "Open an Image Directory")
        self.Bind(wx.EVT_MENU, self.onOpenDirectory, openTool)
        
        self.toolbar.Realize()
        
    #----------------------------------------------------------------------
    def onOpenDirectory(self, event):
        """
        Opens a DirDialog to allow the user to open a folder with pictures
        """
        dlg = wx.DirDialog(self, "Choose a directory",
                           style=wx.DD_DEFAULT_STYLE)
        
        if dlg.ShowModal() == wx.ID_OK:
            self.folderPath = dlg.GetPath()
            # print self.folderPath
            picPaths = glob.glob(self.folderPath + os.path.sep + "*.JPG")
            picPaths = picPaths + glob.glob(self.folderPath + os.path.sep + "*.jpg") 
            # print picPaths
        Publisher().sendMessage("update images", picPaths)
        
    #----------------------------------------------------------------------
    def resizeFrame(self, msg):
        """"""
        self.sizer.Fit(self)
        

        
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = ViewerFrame()
    app.MainLoop()
    
