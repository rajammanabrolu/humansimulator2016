import wx, threading, Queue, sys, time
import os

ID_BEGIN=100

class MainFrame(wx.Frame):
    def __init__(self, parent, id=wx.ID_ANY, title="Health Desk",
                 pos = wx.DefaultPosition, size=(400,550)):

        wx.Frame.__init__(self, parent, id, title, pos, size)
        #self.SetIcon(GetMondrianIcon())
        pn = wx.Panel(self, -1)
        mainSz = wx.BoxSizer(wx.VERTICAL)

        horSz1 = wx.BoxSizer(wx.HORIZONTAL)
        mainSz.Add(horSz1, 1, wx.EXPAND | wx.ALL, 5)

        statTxt3 = wx.StaticText(pn, -1, "Popup Linger")
        horSz1.Add(statTxt3, 3)
        txtCtrl4 = wx.TextCtrl(pn, -1, "4000")
        helpstr = "How Long The Popup Will Stay\nAround After It Is Launched"
        txtCtrl4.SetToolTip(wx.ToolTip(helpstr))
        horSz1.Add(txtCtrl4, 1)

        #Uncomment the below and hardcode the directory and filename
        #filehandle=open(os.path.join(self.dirname, self.filename),'w')
        #filehandle.write(txtCtrl4)
        #filehandle.close()

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
        pn.SetAutoLayout(True)
        pn.SetSizer(mainSz)
        pn.Fit()


    def OnQuit(self, event):
        self.Close()

    def DisplayHelp(self, event):
        dlg = wx.MessageDialog(self, "*Insert helpful info here*", "About", wx.OK)
        dlg.ShowModal() # Show it
        dlg.Destroy()

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MainFrame(None, -1, 'Help Desk')
        self.frame.Show(True)
        self.frame.Center()
        return True

#entry point
if __name__ == '__main__':
    app = MyApp(0)
    app.MainLoop()
