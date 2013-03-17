# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct  8 2012)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

import gettext

_ = gettext.gettext

###########################################################################
## Class LinguaFrame
###########################################################################

class LinguaFrame(wx.Frame):
    def __init__( self, parent ):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(800, 600), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.Size(800, 600), wx.DefaultSize)

        fgSizer2 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer2.SetFlexibleDirection(wx.BOTH)
        fgSizer2.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_listCtrl1 = wx.ListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_HRULES | wx.LC_ICON)
        fgSizer2.Add(self.m_listCtrl1, 0, wx.ALL, 5)

        self.m_staticText3 = wx.StaticText(self, wx.ID_ANY, _(u"MyLabel"), wx.DefaultPosition, wx.DefaultSize,
                                           wx.ALIGN_CENTRE)
        self.m_staticText3.Wrap(-1)
        self.m_staticText3.SetFont(wx.Font(14, 74, 90, 90, False, "Consolas"))
        self.m_staticText3.SetForegroundColour(wx.Colour(255, 255, 255))
        self.m_staticText3.SetBackgroundColour(wx.Colour(0, 0, 0))

        fgSizer2.Add(self.m_staticText3, 0, wx.ALL, 5)

        m_choice1Choices = []
        self.m_choice1 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice1Choices, 0)
        self.m_choice1.SetSelection(0)
        fgSizer2.Add(self.m_choice1, 0, wx.ALL, 5)

        self.SetSizer(fgSizer2)
        self.Layout()

        self.Centre(wx.BOTH)

    def __del__( self ):
        pass
