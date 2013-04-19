# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Oct  8 2012)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx "1" {import wx.aui }
import wx.combo

import gettext
_ = gettext.gettext

###########################################################################
## Class LinguaFrame
###########################################################################

class LinguaFrame ( wx.Frame wx.Frame ):
	
	def __init__( self, parent ):def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 1000,700 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 1000,700 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		"1" { self.m_mgr = wx.aui.AuiManager()
		self.m_mgr.SetManagedWindow( self )
		{ self.m_mgr.SetFlags()
		} }
		mainSizer = wx.BoxSizer( wx.HORIZONTAL )
		
		leftSizer = wx.BoxSizer( wx.VERTICAL )
		
		
		mainSizer.Add( leftSizer, 1, wx.EXPAND, 5 )
		
		rightSizer = wx.BoxSizer( wx.VERTICAL )
		
		rightSizer.SetMinSize( wx.Size( 200,-1 ) ) 
		
		mainSizer.Add( rightSizer, 1, wx.FIXED_MINSIZE|wx.RIGHT, 5 )
		
		
		self.SetSizer( mainSizer )
		self.Layout()
		
		self.Centre( wx.BOTH )  "1" {
		self.m_mgr.Update() }
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
		"1" { self.m_mgr.UnInit()
		}
	

###########################################################################
## Class LinguaTranslateDialog
###########################################################################

class LinguaTranslateDialog ( wx.Dialog wx.Dialog ):
	
	def __init__( self, parent ):def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Translation of selected text"), pos = wx.DefaultPosition, size = wx.Size( 500,350 ), style = wx.DEFAULT_DIALOG_STYLE )wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Translation of selected text"), pos = wx.DefaultPosition, size = wx.Size( 500,350 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		"1" { self.m_mgr = wx.aui.AuiManager()
		self.m_mgr.SetManagedWindow( self )
		{ self.m_mgr.SetFlags()
		} }
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
		
		self.Centre( wx.BOTH )  "1" {
		self.m_mgr.Update() }
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.okButton.Bind( wx.EVT_BUTTON, self.on_continue_click )
	
	def __del__( self ):
		pass
		"1" { self.m_mgr.UnInit()
		}
	
	
	# Virtual event handlers, overide them in your derived class
	def on_continue_click( self, event ):
		event.Skip()
	

###########################################################################
## Class LinguaLeoDialog
###########################################################################

class LinguaLeoDialog ( wx.Dialog wx.Dialog ):
	
	def __init__( self, parent ):def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Add to LinguaLeo Personal Dictionary"), pos = wx.DefaultPosition, size = wx.Size( 400,200 ), style = wx.DEFAULT_DIALOG_STYLE )wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Add to LinguaLeo Personal Dictionary"), pos = wx.DefaultPosition, size = wx.Size( 400,200 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		"1" { self.m_mgr = wx.aui.AuiManager()
		self.m_mgr.SetManagedWindow( self )
		{ self.m_mgr.SetFlags()
		} }
		mainSizer = wx.BoxSizer( wx.VERTICAL )
		
		self.loginLabel = wx.StaticText( self, wx.ID_ANY, _(u"LinguaLeo account email"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.loginLabel.Wrap( -1 )
		mainSizer.Add( self.loginLabel, 0, wx.ALL, 5 )
		
		self.login = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 380,-1 ), 0 )
		mainSizer.Add( self.login, 0, wx.ALL, 5 )
		
		self.passwordLabel = wx.StaticText( self, wx.ID_ANY, _(u"Password"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.passwordLabel.Wrap( -1 )
		mainSizer.Add( self.passwordLabel, 0, wx.ALL, 5 )
		
		self.password = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 380,-1 ), 0 )
		mainSizer.Add( self.password, 0, wx.ALL, 5 )
		
		self.okButton = wx.Button( self, wx.ID_OK, _(u"Add"), wx.DefaultPosition, wx.Size( 380,-1 ), 0 )
		mainSizer.Add( self.okButton, 0, wx.ALL, 5 )
		
		self.cancelBtn = wx.Button( self, wx.ID_CANCEL, _(u"Cancel"), wx.DefaultPosition, wx.Size( 380,-1 ), 0 )
		mainSizer.Add( self.cancelBtn, 0, wx.ALL, 5 )
		
		
		self.SetSizer( mainSizer )
		self.Layout()
		
		self.Centre( wx.BOTH )  "1" {
		self.m_mgr.Update() }
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
		"1" { self.m_mgr.UnInit()
		}
	

