#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import shutil
from subprocess import Popen

import wx


Editor = "gedit"
DataPath = "/etc/hostswitcher"
DefaultHosts = "/etc/hostswitcher/default"
CurrentHosts = "/etc/hostswitcher/CURRENT"


def get_all_hosts():
    r = []
    for fname in os.listdir(DataPath):
        if fname != "CURRENT" and os.path.isfile(os.path.join(DataPath, fname)):
            r.append(fname)
    return r


def call_editor(fpath):
    result = False
    cmd = r'%s %s'
    try:
        p = Popen(cmd % (Editor, fpath), shell = True)
        p.wait()
        result = True
    except Exception, e:
        print e
    return result


class MainFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        wx.Frame.__init__(self, *args, **kwds)
        self.icon = wx.Icon("/usr/share/icons/hicolor/128x128/apps/switch-icon.png", wx.BITMAP_TYPE_PNG)
        self.SetIcon(self.icon)
        with open(CurrentHosts, "rb") as fp:
            self.current = fp.read()
        self.all_hosts = get_all_hosts()

        self.combo_box_1 = wx.ComboBox(self, wx.ID_ANY, choices = self.all_hosts, style = wx.CB_DROPDOWN)
        index = 0
        try:
            index = self.all_hosts.index(self.current)
        except Exception:
            pass
        self.combo_box_1.Select(index)
        self.button_add = wx.Button(self, wx.ID_ANY, "Add")
        self.button_delete = wx.Button(self, wx.ID_ANY, "Delete")
        self.button_edit = wx.Button(self, wx.ID_ANY, "Edit")
        self.button_set = wx.Button(self, wx.ID_ANY, "Set")
        self.Bind(wx.EVT_BUTTON, self.OnAdd, self.button_add)
        self.Bind(wx.EVT_BUTTON, self.OnDelete, self.button_delete)
        self.Bind(wx.EVT_BUTTON, self.OnEdit, self.button_edit)
        self.Bind(wx.EVT_BUTTON, self.OnSet, self.button_set)
        self.statusbar = self.CreateStatusBar(1)

        self.__set_properties()
        self.__do_layout()

    def __set_properties(self):
        self.SetTitle("hostswitcher")
        self.statusbar.SetStatusWidths([-1])
        self.statusbar.SetStatusText("Current: %s" % self.current)

    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_1 = wx.GridSizer(1, 4, 0, 0)
        sizer_1.Add(self.combo_box_1, 0, wx.ALL | wx.EXPAND, 0)
        grid_sizer_1.Add(self.button_add, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        grid_sizer_1.Add(self.button_delete, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        grid_sizer_1.Add(self.button_edit, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        grid_sizer_1.Add(self.button_set, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_1.Add(grid_sizer_1, 1, 0, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()

    def OnAdd(self, evt):
        dialog = wx.TextEntryDialog(self,
                                    "Enter name:",
                                    "Add", style = wx.OK | wx.CANCEL)
        dialog.Centre(wx.BOTH)
        if dialog.ShowModal() == wx.ID_OK:
            name = dialog.GetValue()
            if name not in ("CURRENT", ) and name not in self.all_hosts:
                fpath = os.path.join(DataPath, name)
                shutil.copy(os.path.join(DataPath, "default"), fpath)
                call_editor(fpath)
                self.all_hosts.append(name)
                self.combo_box_1.AppendItems([name])
            else:
                msg_dialog = wx.MessageDialog(self,
                                              "Failed to create \"%s\".\nFile already exists." % name,
                                              'Failed to create "%s"' % name, wx.OK | wx.ICON_ERROR)
                msg_dialog.Centre(wx.BOTH)
                msg_dialog.ShowModal()
                msg_dialog.Destroy()
        dialog.Destroy()

    def OnDelete(self, evt):
        name = self.combo_box_1.GetValue()
        fpath = os.path.join(DataPath, name)
        if name != "default":
            msg_dialog = wx.MessageDialog(self,
                                          "Are you sure that you want to delete file \"%s\"" % name,
                                          "Delete \"%s\"" % name, wx.YES_NO | wx.ICON_EXCLAMATION)
            msg_dialog.Centre(wx.BOTH)
            r = msg_dialog.ShowModal()
            if r == wx.ID_YES:
                if os.path.exists(fpath) and os.path.isfile(fpath):
                    os.remove(fpath)
                    index = self.combo_box_1.GetSelection()
                    self.combo_box_1.Delete(index)
                    self.combo_box_1.Select(0)
            msg_dialog.Destroy()
        else:
            msg_dialog = wx.MessageDialog(self,
                                          "\"%s\" can't be deleted.\nYou can edit it only." % name,
                                          "\"%s\" can't be deleted." % name, wx.OK | wx.ICON_ERROR)
            msg_dialog.Centre(wx.BOTH)
            msg_dialog.ShowModal()
            msg_dialog.Destroy()


    def OnEdit(self, evt):
        name = self.combo_box_1.GetValue()
        fpath = os.path.join(DataPath, name)
        r = call_editor(fpath)

    def OnSet(self, evt):
        name = self.combo_box_1.GetValue()
        fpath = os.path.join(DataPath, name)
        msg_dialog = wx.MessageDialog(self,
                                      "Are you sure that you want to set file \"%s\" as current hosts" % name,
                                      "Set \"%s\"" % name, wx.YES_NO | wx.ICON_EXCLAMATION)
        msg_dialog.Centre(wx.BOTH)
        r = msg_dialog.ShowModal()
        if r == wx.ID_YES:
            with open(fpath, "rb") as fp_src:
                with open("/etc/hosts", "wb") as fp_des:
                    fp_des.write(fp_src.read())
                    self.current = name
                    with open(CurrentHosts, "wb") as fp:
                        fp.write(name)
                    self.statusbar.SetStatusText("Current: %s" % self.current)
        msg_dialog.Destroy()


class MainApp(wx.App):
    def OnInit(self):
        w = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_X)
        h = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_Y)
        frame = MainFrame(None, -1, "", (w / 2 - 200, h / 2 - 50), style = wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
        self.SetTopWindow(frame)
        frame.Show()
        return True

def main():
    try:
        if not os.path.exists(DataPath):
            os.makedirs(DataPath)
        if not os.path.exists(DefaultHosts):
            with open(DefaultHosts, "wb") as fp_def:
                with open("/etc/hosts", "rb") as fp_hosts:
                    fp_def.write(fp_hosts.read())
            with open(CurrentHosts, "wb") as fp_cur:
                fp_cur.write("default")
        app = MainApp()
        app.MainLoop()
    except Exception, e:
        print e

if __name__ == "__main__":
    main()

