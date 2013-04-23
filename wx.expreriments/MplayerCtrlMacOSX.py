#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MplayerCtrl as mpc
import wx
import sys

class Frame(wx.Frame):
    def __init__(self, parent, id, files):
        wx.Frame.__init__(self, parent, id, size=(-1, -1))
        self.panel = wx.Panel(self)

        mplayer_args=[
           u'--no-autosub',
           u'--nosub', u'--identify', u'--slave', u'--idle'
        ]
        if sys.platform == 'darwin':
            self.mpc = mpc.MplayerCtrl(self.panel, -1, '/opt/local/bin/mplayer',mplayer_args=mplayer_args)
        else:
            self.mpc = mpc.MplayerCtrl(self.panel, -1, '../bin/win32/mplayer2.exe',mplayer_args=mplayer_args)


        self.panel.Bind(mpc.EVT_MEDIA_STARTED, self.media_started)
        self.panel.Bind(mpc.EVT_MEDIA_FINISHED, self.media_finished)
        self.panel.Bind(mpc.EVT_PROCESS_STARTED, self.process_started)
        self.panel.Bind(mpc.EVT_PROCESS_STOPPED, self.process_stopped)
        self.panel.Bind(mpc.EVT_STDERR, self.stderr)
        self.Bind(wx.EVT_INIT_DIALOG, self.init_dialog)

        self.files = files

        self.panel.Layout()
        self.Center()
        self.Show()

    def init_dialog(self, evt):
        for f in self.files:
            self.mpc.Loadfile(f, 1) # add to mplayers playlist

    def media_started(self, evt):
        print '----------> Media started'
        print 'Now playing:', self.mpc.GetMetaTitle()
        wx.FutureCall(3000, self.mpc.PtStep, '+') # after 3 seconds switch to the
                                                  # next file in the playlist
    def media_finished(self, evt):
        print '----------> Media finished'
    def process_started(self, evt):
        print '----------> Process started'
    def process_stopped(self, evt):
        print '----------> Process stopped'
    def stderr(self, evt):
        print 'Stderr >>>', evt.data


if __name__ == '__main__':
    mpc.DEBUG = True
    app = wx.PySimpleApp()
    if sys.platform == 'darwin':
        f = Frame(None, -1, ['ffmpeg:///Volumes/Untitled 1/Shared/Video/Да Винчи/Demoni.Da.Vinchi.S01E01.L1.HDTVRip.Kerob.avi'])
    else:
        f = Frame(None, -1, ['ffmpeg:///D:/Shared/Video/Да Винчи/Demoni.Da.Vinchi.S01E01.L1.HDTVRip.Kerob.avi'])
    app.MainLoop()