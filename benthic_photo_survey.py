import wx

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title )
        self.init_ui()
        self.Show(True)
        
    def init_ui(self):
        panel = MyPanel(self)
    
class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent,wx.ID_ANY)
        self.init_ui()
        
    def init_ui(self):
        # Right Column box
        rbox = wx.BoxSizer(wx.VERTICAL)
        
        # Exif Data box
        exifsbox = wx.StaticBox(self, label="Exif Data")
        exifsizer = wx.StaticBoxSizer(exifsbox,wx.VERTICAL)
        exifgrid = wx.FlexGridSizer(4,2)
        
        pos_label = wx.StaticText(self, label="Position")
        dep_label = wx.StaticText(self, label="Depth")
        tem_label = wx.StaticText(self, label="Temperature")
        sub_label = wx.StaticText(self, label="Substrate")
        
        position = wx.StaticText(self, label="-36 45.2345\n123 23.5668")
        depth = wx.StaticText(self, label="12.5 m")
        temp = wx.StaticText(self, label="10 C")
        substrate = wx.StaticText(self, label="Barrens")
        
        exifgrid.AddMany([(pos_label),(position,1,wx.EXPAND),
                            (dep_label),(depth)
                            ])
        
        # Select Substrate box
        sb = wx.StaticBox(self, label="Substrate Selector")
        ssbox = wx.StaticBoxSizer(sb, wx.VERTICAL)
        self.substSelect = SubstrateSelector(self, -1 )
        ssbox.Add(self.substSelect, flag=wx.CENTER)
        
        # Put stuff in the right column
        rbox.Add(exifsbox)
        rbox.Add(ssbox)
        
        self.SetSizer(rbox)
        
class SubstrateSelector(wx.ListBox):
    def __init__(self, *args, **kwargs):
        subst = ['Sand','Barrens','Turf','Mixed Weed','Kelp Forest','Other']
        super(SubstrateSelector, self).__init__(*args, size=(120,150), choices=subst, style=wx.LB_SINGLE, **kwargs)
        
        
app = wx.App(redirect=True,filename='error.txt')
frame = MyFrame(None, title='Benthic Photo Survey')
app.MainLoop()