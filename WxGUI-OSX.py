import wx, threading, Queue, sys, time
import os

ID_BEGIN=100

class MainPane(wx.Panel):
    def __init__(self, parent, id=wx.ID_ANY, title="Health Desk",
                 pos = wx.DefaultPosition, size=(900,750)):

        wx.Panel.__init__(self, parent=parent)
        #self.SetIcon(GetMondrianIcon())
        #self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.frame = parent
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

    def OnEraseBackground(self, evt):
        dc = evt.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        bmp = wx.Bitmap("HD.Settings.Screen.png")
        dc.DrawBitmap(bmp, 0, 0)


class MainFrame(wx.Frame):

    def __init__(self):
        self.counter1 = 0
        self.counter2 = 0
        """Constructor"""
        wx.Frame.__init__(self, None, -1, 'Health Desk', size=(550, 500))
        panel = MainPane(self)
        mainSz = wx.BoxSizer(wx.VERTICAL)

        horSz1 = wx.BoxSizer(wx.HORIZONTAL)
        insizer = wx.BoxSizer(wx.HORIZONTAL)
        insizer.Add(horSz1, 0, wx.TOP, 45)
        mainSz.Add(insizer, 0, wx.BOTTOM | wx.LEFT, 20)

        statTxt3 = TransparentText(panel, -1, "Popup Interval")
        horSz1.Add(statTxt3, 3)
        txtCtrl4 = wx.TextCtrl(panel, -1, '300')
        helpstr = "The minimum interval between notifications."
        txtCtrl4.SetToolTip(wx.ToolTip(helpstr))
        horSz1.Add(txtCtrl4, 1)
        posBtn = wx.Button(panel, id=wx.ID_ANY, label="Disabled")
        eyeBtn = wx.Button(panel, id=wx.ID_ANY, label="Disabled")

        def onButton(event):
            replace_line('healthdeskrc', 0, str(txtCtrl4.GetValue()))

        def onButton1(event):
            replace_line('healthdeskrc', 1, 'PEnabled')
            self.counter1+=1
            if self.counter1 % 2 == 0:
                posBtn.SetLabel('Disabled')
                replace_line('healthdeskrc', 1, 'PDisabled')
            else:
                posBtn.SetLabel('Enabled')

        def onButton2(event):
            replace_line('healthdeskrc', 2, 'EEnabled')
            self.counter2+=1
            if self.counter2 % 2 == 0:
                eyeBtn.SetLabel('Disabled')
                replace_line('healthdeskrc', 2, 'EDisabled')
            else:
                eyeBtn.SetLabel('Enabled')


        posBtn.Bind(wx.EVT_BUTTON, onButton1)
        eyeBtn.Bind(wx.EVT_BUTTON, onButton2)

        horSzp = wx.BoxSizer(wx.HORIZONTAL)
        statTxt3 = TransparentText(panel, 0, "Check for posture")
        horSzp.Add(statTxt3, 3)
        insizer3 = wx.BoxSizer(wx.HORIZONTAL)
        insizer3.Add(posBtn, 1)
        horSzp.Add(insizer3, 1, wx.LEFT, 16)
        mainSz.Add(horSzp, 0.5, wx.ALL, 20)

        horSz3 = wx.BoxSizer(wx.HORIZONTAL)
        statTxt3 = TransparentText(panel, 0, "Check for eye position")
        horSz3.Add(statTxt3, 3)
        insizer4 = wx.BoxSizer(wx.HORIZONTAL)
        insizer4.Add(eyeBtn, 1)
        horSz3.Add(insizer4, 1, wx.LEFT, 16)
        mainSz.Add(horSz3, 0.5, wx.ALL, 20)

        saveBtn = wx.Button(panel, id=wx.ID_ANY, label="Save")
        saveBtn.Bind(wx.EVT_BUTTON, onButton)

        horSz4 = wx.BoxSizer(wx.HORIZONTAL)
        horSz4.Add(saveBtn, 1)
        insizer2 = wx.BoxSizer(wx.HORIZONTAL)
        insizer2.Add(horSz4, 1, wx.LEFT, 350)
        mainSz.Add(insizer2, 1, wx.TOP, 20)
        menubar = wx.MenuBar()
        file = wx.Menu()
        help = wx.Menu()
        file.AppendSeparator()
        quit = wx.MenuItem(file, 105, '&Quit\tCtrl+Q', 'Quit the Application')
        about = wx.MenuItem(help, 205, '&About\tCtrl+A', 'Display information about this product')
        file.AppendItem(quit)
        help.AppendItem(about)
        menubar.Append(file, '&File')
        menubar.Append(help, '&Help')
        self.SetMenuBar(menubar)
        self.Centre()
        self.Bind(wx.EVT_MENU, self.OnQuit, id=105)
        self.Bind(wx.EVT_MENU, self.DisplayHelp, id=205)
        self.SetAutoLayout(True)
        self.SetSizer(mainSz)
        panel.SetSizer(mainSz)
        mainSz.Fit(panel)
        panel.Layout()
        self.Center()

    def OnQuit(self, event):
        self.Close()

    def DisplayHelp(self, event):
        dlg = wx.MessageDialog(self, "This is Health Desk, an app to remind users about healthy habits during extended computer use.", "About", wx.OK)
        dlg.ShowModal() # Show it
        dlg.Destroy()

    def replace_line(file_name, line_num, text):
        lines = open(file_name, 'r').readlines()
        lines[line_num] = text
        out = open(file_name, 'w')
        out.writelines(lines)
        out.close()


class TransparentText(wx.StaticText):
  def __init__(self, parent, id=wx.ID_ANY, label='',
               pos=wx.DefaultPosition, size=wx.DefaultSize,
               style=wx.TRANSPARENT_WINDOW, name='transparenttext'):
    wx.StaticText.__init__(self, parent, id, label, pos, size, style, name)

    self.Bind(wx.EVT_PAINT, self.on_paint)
    self.Bind(wx.EVT_ERASE_BACKGROUND, lambda event: None)
    self.Bind(wx.EVT_SIZE, self.on_size)

  def on_paint(self, event):
    bdc = wx.PaintDC(self)
    dc = wx.GCDC(bdc)

    font_face = self.GetFont()
    font_color = self.GetForegroundColour()

    dc.SetFont(font_face)
    dc.SetTextForeground(font_color)
    dc.DrawText(self.GetLabel(), 0, 0)

  def on_size(self, event):
    self.Refresh()
    event.Skip()

class TransparentCheckBox(wx.CheckBox):
  def __init__(self, parent, id=-1, label='EmptyString', pos=wx.DefaultPosition, size=wx.DefaultSize, style=0, validator=wx.DefaultValidator, name='MyLife'):
    wx.CheckBox.__init__(self, parent, id, label, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0, validator=wx.DefaultValidator, name='MyLife')

    self.Bind(wx.EVT_PAINT, self.on_paint)
    self.Bind(wx.EVT_ERASE_BACKGROUND, lambda event: None)
    self.Bind(wx.EVT_SIZE, self.on_size)

  def on_paint(self, event):
    bdc = wx.PaintDC(self)
    dc = wx.GCDC(bdc)

    font_face = self.GetFont()
    font_color = self.GetForegroundColour()

    dc.SetFont(font_face)
    dc.SetTextForeground(font_color)
    dc.DrawText(self.GetLabel(), 0, 0)

  def on_size(self, event):
    self.Refresh()
    event.Skip()

class Main(wx.App):

    def __init__(self, redirect=False, filename=None):

        wx.App.__init__(self, redirect, filename)
        dlg = MainFrame()
        dlg.Centre()
        dlg.Show()

if __name__ == "__main__":
    app = Main()
    app.MainLoop()
