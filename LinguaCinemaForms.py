# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Oct  8 2012)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.combo

import gettext
_ = gettext.gettext

###########################################################################
## Class LinguaTranslateDialog
###########################################################################

class LinguaTranslateDialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Translation of selected text"), pos = wx.DefaultPosition, size = wx.Size( 500,350 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		mainSizer = wx.BoxSizer( wx.VERTICAL )
		
		translateSizer = wx.BoxSizer( wx.VERTICAL )
		
		translateSizer.SetMinSize( wx.Size( -1,290 ) ) 
		self.sourceText = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,40 ), wx.ALIGN_CENTRE )
		self.sourceText.Wrap( -1 )
		self.sourceText.SetFont( wx.Font( 14, 74, 90, 90, False, "Consolas" ) )
		self.sourceText.SetForegroundColour( wx.Colour( 255, 255, 255 ) )
		self.sourceText.SetBackgroundColour( wx.Colour( 0, 0, 0 ) )
		self.sourceText.SetMinSize( wx.Size( -1,40 ) )
		
		translateSizer.Add( self.sourceText, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.translateText = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,230 ), wx.ALIGN_LEFT )
		self.translateText.Wrap( -1 )
		self.translateText.SetFont( wx.Font( 14, 74, 90, 90, False, "Consolas" ) )
		self.translateText.SetMinSize( wx.Size( -1,230 ) )
		
		translateSizer.Add( self.translateText, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		mainSizer.Add( translateSizer, 1, wx.EXPAND, 5 )
		
		langSizer = wx.BoxSizer( wx.HORIZONTAL )
		
		langSizer.SetMinSize( wx.Size( -1,30 ) ) 
		self.sourceLangLabel = wx.StaticText( self, wx.ID_ANY, _(u"Source"), wx.DefaultPosition, wx.Size( -1,20 ), 0 )
		self.sourceLangLabel.Wrap( -1 )
		langSizer.Add( self.sourceLangLabel, 0, wx.ALL, 5 )
		
		self.sourceLang = wx.combo.BitmapComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,20 ), "", wx.CB_READONLY ) 
		langSizer.Add( self.sourceLang, 0, wx.ALL, 5 )
		
		self.targetLangLabel = wx.StaticText( self, wx.ID_ANY, _(u"Translate"), wx.DefaultPosition, wx.Size( -1,20 ), 0 )
		self.targetLangLabel.Wrap( -1 )
		langSizer.Add( self.targetLangLabel, 0, wx.ALL, 5 )
		
		self.targetLang = wx.combo.BitmapComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, "", wx.CB_READONLY ) 
		self.targetLang.SetMinSize( wx.Size( -1,20 ) )
		
		langSizer.Add( self.targetLang, 0, wx.ALL, 5 )
		
		
		mainSizer.Add( langSizer, 1, wx.ALL|wx.FIXED_MINSIZE, 5 )
		
		self.okButton = wx.Button( self, wx.ID_ANY, _(u"Continue"), wx.DefaultPosition, wx.DefaultSize, 0 )
		mainSizer.Add( self.okButton, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		self.SetSizer( mainSizer )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.okButton.Bind( wx.EVT_BUTTON, self.on_continue_click )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def on_continue_click( self, event ):
		event.Skip()
	

