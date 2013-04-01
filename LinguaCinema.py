#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import re
import time
import gettext
import wx
import wx.combo as combo
import MplayerCtrl as mpc
import wx.lib.buttons as buttons
import urllib
import urllib2
import cookielib
import json
import LinguaSubDownloader
from pysrt import SubRipFile


if getattr(sys, 'frozen', None):
    linguaBaseDir = sys._MEIPASS
    mpc.DEBUG = False
else:
    linguaBaseDir = os.path.dirname(os.path.abspath(__file__))
    mpc.DEBUG = False

linguaBitmapDir = os.path.join(linguaBaseDir, 'bitmaps')
_ = wx.GetTranslation


class LinguaFrame(wx.Frame):
    #----------------------------------------------------------------------
    def __init__(self, parent, id, title, mplayerPath):
        """

        @param parent:
        @param id:
        @param title:
        @param mplayerPath:
        """
        wx.Frame.__init__(self, parent=parent, id=id, title=title, size=wx.Size(800, 600))
        self.panel = wx.Panel(self)

        sp = wx.StandardPaths.Get()
        self.SetIcon(wx.Icon("favicon.ico", wx.BITMAP_TYPE_ICO))
        self.currentFolder = linguaBaseDir if not getattr(sys, 'frozen', None) else sp.GetDocumentsDir()
        self.currentVolume = 50
        self.mediaFile = None
        self.srtFile = None
        self.srtParsed = None
        self.isTranslateDialogShowed = False
        self.srtIndex = 0
        self.buttons = {}
        self.id_audio_detect = re.compile(r'ID_AUDIO_ID=(\d+)')

        self.create_menu()

        # create sizers
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        controlSizer = wx.BoxSizer(wx.HORIZONTAL)
        sliderSizer = wx.BoxSizer(wx.HORIZONTAL)
        subtitleSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.build_controls(controlSizer)

        self.mplayer = mpc.MplayerCtrl(self.panel, -1, mplayerPath,
                                       mplayer_args=[
                                           u'--consolecontrols', u'--no-autosub',
                                           u'--nosub', u'--identify', u'--no-fontconfig'
                                       ])

        # create volume control
        self.volumeCtrl = wx.Slider(self.panel)
        self.volumeCtrl.SetRange(0, 100)
        self.volumeCtrl.SetValue(self.currentVolume)
        self.volumeCtrl.Bind(wx.EVT_SLIDER, self.on_set_volume)
        controlSizer.Add(self.volumeCtrl, 0, wx.ALL, 5)

        #audio stream control
        self.audioStreamCtrl = wx.Choice(self.panel, choices=[_('Audio stream')], size=wx.Size(200, -1))
        self.audioStreamCtrl.Bind(wx.EVT_CHOICE, self.on_audio_stream)
        controlSizer.Add(self.audioStreamCtrl, 0, wx.ALL, 5)

        # create track slider and track counter
        self.timelineCtrl = wx.Slider(self.panel, size=wx.DefaultSize)
        self.timelineCtrl.Bind(wx.EVT_SLIDER, self.on_set_timepos)
        self.trackCounter = wx.StaticText(self.panel, label="00:00")

        sliderSizer.Add(self.timelineCtrl, 1, wx.ALL | wx.EXPAND, 5)
        sliderSizer.Add(self.trackCounter, 0, wx.ALL | wx.CENTER, 5)

        # set up playback timer
        self.playbackTimer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_update_playback)

        #create subtitle control
        self.subtitle = wx.TextCtrl(self.panel, -1, name=_('subtitles'),
                                    style=wx.TE_READONLY | wx.TE_CENTER | wx.TE_WORDWRAP | wx.TE_MULTILINE)
        self.subtitle.SetBackgroundColour(wx.Color(0, 0, 0))
        self.subtitle.SetForegroundColour(wx.Color(255, 255, 255))
        self.subtitle.SetValue('')
        self.subtitle.SetMinSize(wx.Size(-1, 100))
        self.subtitle.SetFont(wx.Font(14, 74, 90, 90, False, "Consolas"))

        subtitleSizer.Add(self.subtitle, wx.ALL | wx.EXPAND)

        mainSizer.Add(self.mplayer, 1, wx.ALL | wx.EXPAND, 5)
        mainSizer.Add(subtitleSizer, 0, wx.ALL | wx.EXPAND, 5)
        mainSizer.Add(sliderSizer, 0, wx.ALL | wx.EXPAND, 5)
        mainSizer.Add(controlSizer, 0, wx.ALL | wx.EXPAND, 5)
        self.panel.SetSizer(mainSizer)

        self.panel.Bind(mpc.EVT_MEDIA_STARTED, self.on_media_started)
        self.panel.Bind(mpc.EVT_MEDIA_FINISHED, self.on_media_finished)
        self.panel.Bind(mpc.EVT_PROCESS_STARTED, self.on_process_started)
        self.panel.Bind(mpc.EVT_PROCESS_STOPPED, self.on_process_stopped)
        self.panel.Bind(mpc.EVT_STDERR, self.on_stderr)
        self.panel.Bind(mpc.EVT_STDOUT, self.on_stdout)

        self.Bind(wx.EVT_MOUSEWHEEL, self.on_mouse_wheel)
        self.Bind(wx.EVT_CLOSE, self.on_close_window)

        self.Bind(wx.EVT_KEY_DOWN, self.on_key_down)
        self.panel.Bind(wx.EVT_KEY_DOWN, self.on_key_down)
        self.subtitle.Bind(wx.EVT_KEY_DOWN, self.on_key_down)

        self.subtitle.Bind(wx.EVT_LEFT_UP, self.on_subtitle_click)

        self.SetMinSize(wx.Size(800, 600))
        self.Center()
        self.Show()
        self.panel.Layout()
        self.panel.SetFocus()

    #----------------------------------------------------------------------
    def build_btn(self, png, handler, name, title, builder, sizer, png_toggle=None):
        img = wx.Bitmap(os.path.join(linguaBitmapDir, png))
        btn = builder(self.panel, bitmap=img, name=name)
        #btn = buttons.GenBitmapToggleButton(self.panel, bitmap=img, name=btnDict['name'])
        btn.SetInitialSize()
        btn.SetToolTipString(title)
        if not png_toggle is None and builder == buttons.GenBitmapToggleButton:
            img_toggle = wx.Bitmap(os.path.join(linguaBitmapDir, png_toggle))
            btn.SetBitmapSelected(img_toggle)

        btn.Bind(wx.EVT_BUTTON, handler)
        sizer.Add(btn, 0, wx.LEFT, 3)
        return btn

    #----------------------------------------------------------------------
    def build_controls(self, controlSizer):
        """
        Builds the playback controls
        """
        self.buttons['prev'] = self.build_btn(
            png='player_prev.png',
            handler=self.on_prev,
            title=_("Previous phrase"),
            name='prev',
            builder=buttons.GenBitmapButton,
            sizer=controlSizer)

        self.buttons['pause'] = self.build_btn(
            png='player_pause.png',
            png_toggle='player_play.png',
            handler=self.on_pause,
            title=_("Pause"),
            name='pause',
            builder=buttons.GenBitmapToggleButton,
            sizer=controlSizer)

        self.buttons['replay'] = self.build_btn(
            png='player_replay.png',
            handler=self.on_replay,
            title=_("Replay phrase"),
            name='stop',
            builder=buttons.GenBitmapButton,
            sizer=controlSizer)

        self.buttons['stop'] = self.build_btn(
            png='player_stop.png',
            handler=self.on_stop,
            title=_("Stop"),
            name='stop',
            builder=buttons.GenBitmapButton,
            sizer=controlSizer)

        self.buttons['next'] = self.build_btn(
            png='player_next.png',
            handler=self.on_next,
            title=_("Next phrase"),
            name='next',
            builder=buttons.GenBitmapButton,
            sizer=controlSizer)

        return controlSizer

    #----------------------------------------------------------------------
    def create_menu(self):
        """
        Creates a menu
        """
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        add_file_menu_item = fileMenu.Append(wx.NewId(), _("&Open media file\tCtrl+O"), _("Open media file"))
        add_subtitle_menu_item = fileMenu.Append(wx.NewId(), _("&Open subtitles file\tCtrl+S"), _("Open subtitles"))
        menubar.Append(fileMenu, _('&File'))

        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.on_add_file, add_file_menu_item)
        self.Bind(wx.EVT_MENU, self.on_add_subtitle, add_subtitle_menu_item)

    #----------------------------------------------------------------------
    def open_subtitle(self, path):
        print "open subtitle %s" % path
        self.srtFile = path
        try:
            self.srtParsed = SubRipFile.open(self.srtFile)
        except UnicodeDecodeError:
            self.srtParsed = SubRipFile.open(self.srtFile, encoding='windows-1251')

        self.srtIndex = 0

        if self.playbackTimer.IsRunning() or not self.mediaFile is None:
            offset = self.timelineCtrl.GetValue()
            while self.srtIndex < len(self.srtParsed):
                start = self.srtParsed[self.srtIndex].start
                end = self.srtParsed[self.srtIndex].end.ordinal
                if start <= offset * 1000 <= end:
                    self.subtitle.SetValue(re.compile(r'<[^>]+>').sub('', self.srtParsed[self.srtIndex].text))
                    return
                self.srtIndex += 1

        self.srtIndex = 0

    #----------------------------------------------------------------------
    def on_add_subtitle(self, event):
        """
        Add a *.srt file
        """
        wildcard = _("Subtitles Files (*.srt)|*.srt")
        dlg = wx.FileDialog(
            self, message=_("Choose a file"),
            defaultDir=self.currentFolder,
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.CHANGE_DIR
        )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            dlg.Destroy()
            self.currentFolder = os.path.dirname(path[0])
            self.open_subtitle(path)
            self.panel.SetFocus()

    #----------------------------------------------------------------------
    def on_add_file(self, event):
        """
        Add a Movie and start playing it
        @param event:
        """
        wildcard = _("Video files (avi,mkv,mp4,mov)|*.avi;*.mkv;*.mp4;*.mov")
        dlg = wx.FileDialog(
            self, message=_("Choose a file"),
            defaultDir=self.currentFolder,
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.CHANGE_DIR
        )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            dlg.Destroy()
            self.currentFolder = os.path.dirname(path[0])
            self.mediaFile = '"%s"' % path.replace("\\", "/")
            srtFile = (os.path.splitext(self.mediaFile)[0] + '.srt').replace("/", '\\').strip('"')
            if not os.path.isfile(srtFile):
                dlg = wx.MessageDialog(self, _('Subtitle file not found download it from http://opensubtitles.org?'),
                                       _('%s not exists') % srtFile, wx.YES_NO | wx.ICON_QUESTION)
                if dlg.ShowModal() == wx.ID_YES:
                    print self.mediaFile.replace("/", '\\').strip('"')
                    LinguaSubDownloader.DownloadSubtitleForMovie(self.mediaFile.replace("/", '\\').strip('"'), 'eng')
                dlg.Destroy()

            self.timelineCtrl.SetValue(0)
            self.mplayer.Loadfile(self.mediaFile)

            if os.path.isfile(srtFile):
                self.open_subtitle(srtFile)


        self.panel.SetFocus()

    #----------------------------------------------------------------------
    def on_media_started(self, event):
        #print _('Media started!')
        t_len = self.mplayer.GetTimeLength()
        self.timelineCtrl.SetRange(0, t_len)
        self.playbackTimer.Start(100)
        self.buttons['pause'].SetToggle(False)
        self.mplayer.SetProperty("volume", self.currentVolume)
        self.audioStreamCtrl.SetSelection(0)
        self.panel.SetFocus()

    #----------------------------------------------------------------------
    def on_media_finished(self, event):
        #print _('Media finished!')
        self.playbackTimer.Stop()
        self.panel.SetFocus()
        self.srtIndex = 0

    #----------------------------------------------------------------------
    def on_stop(self, event):
        #print _("stopping...")
        self.mplayer.Stop()
        self.playbackTimer.Stop()
        self.mediaFile = None
        self.srtIndex = 0
        self.srtFile = None
        self.srtParsed = None
        self.timelineCtrl.SetValue(0)
        self.subtitle.SetValue("")

    #----------------------------------------------------------------------
    def change_phrase(self):
        if (not self.srtFile is None) and (not self.srtParsed is None):
            offset = self.srtParsed[self.srtIndex].start.ordinal / 1000
            self.timelineCtrl.SetValue(offset)
            secsPlayed = time.strftime('%M:%S', time.gmtime(offset))
            self.trackCounter.SetLabel(secsPlayed)
            self.mplayer.SetProperty('time_pos', offset)
            self.subtitle.SetValue(re.compile(r'<[^>]+>').sub('', self.srtParsed[self.srtIndex].text))
            self.panel.SetFocus()

    #----------------------------------------------------------------------
    def on_next(self, event):
        if self.playbackTimer.IsRunning() and not self.srtFile is None and self.srtIndex < len(self.srtParsed):
            self.srtIndex += 1
            self.change_phrase()

    #----------------------------------------------------------------------
    def on_prev(self, event):
        if self.playbackTimer.IsRunning() and not self.srtFile is None and self.srtIndex > 0:
            self.srtIndex -= 1
            self.change_phrase()

    def on_replay(self, event):
        if self.playbackTimer.IsRunning() and not self.srtFile is None and self.srtIndex > 0:
            self.change_phrase()

    #----------------------------------------------------------------------
    def on_pause(self, event):
        if self.playbackTimer.IsRunning():
            #print _("pausing...")
            self.mplayer.Pause()
            self.playbackTimer.Stop()
            self.buttons['pause'].SetToggle(True)
        elif not self.mediaFile is None and self.mplayer.process_alive:
            #print _("resuming...")
            self.mplayer.Pause()
            self.playbackTimer.Start()
            self.buttons['pause'].SetToggle(False)
        self.buttons['pause'].SetFocus()

    def on_stdout(self, event):
        m = self.id_audio_detect.match(event.data)
        if not m is None:
            max_audio_id = int(m.group(1))
            self.audioStreamCtrl.Clear()
            for i in range(0, max_audio_id + 1):
                self.audioStreamCtrl.Append(_('Audio stream #%d') % i)

    def on_stderr(self, event):
        print event.data

    #----------------------------------------------------------------------
    def on_process_started(self, event):
        #print _('Process started!')
        pass

    #----------------------------------------------------------------------
    def on_process_stopped(self, event):
        #print _('Process stopped!')
        pass

    #----------------------------------------------------------------------
    def on_set_volume(self, event):
        """
        Sets the volume of the music player
        """
        self.currentVolume = self.volumeCtrl.GetValue()
        if self.playbackTimer.IsRunning():
            self.mplayer.SetProperty("volume", self.currentVolume)
            self.SetFocus()

    #----------------------------------------------------------------------
    def on_audio_stream(self, event):
        if self.playbackTimer.IsRunning():
            self.mplayer.SwitchAudio(self.audioStreamCtrl.GetCurrentSelection())

    def on_subtitle_down(self, event):
        event.Skip()
    #----------------------------------------------------------------------
    def on_subtitle_click(self, event):

        need_play = False
        if self.playbackTimer.IsRunning():
            self.on_pause(event)
            need_play = True

        if self.isTranslateDialogShowed:
            return
        word = ''
        value = self.subtitle.GetValue()
        if value:
            selection = self.subtitle.GetStringSelection()

            if not selection is None and len(selection) > 0:
                word = selection.replace(u"\n", " ")
            else:
                position = event.GetPosition()
                (res, hitpos) = self.subtitle.HitTestPos(position)
                (col, line) = self.subtitle.PositionToXY(hitpos)
                text_line = self.subtitle.GetLineText(line)

                if not text_line is None and len(text_line) > 0:
                    r_space = text_line.find(' ', col)
                    r_space = r_space if r_space != -1 else len(text_line)
                    word = text_line[0:r_space]
                    l_space = word.rfind(' ')
                    word = word[l_space:] if l_space != -1 else word

            if word.strip(" \n\r\t") != "":
                dlg = LinguaTranslateDialog(self, word)
                self.isTranslateDialogShowed = True
                dlg.Raise()
                dlg.ShowModal()
                dlg.Destroy()
                self.isTranslateDialogShowed = False

        if need_play:
            self.on_pause(event)

        self.subtitle.SetFocus()
        event.Skip()

    #----------------------------------------------------------------------
    def on_set_timepos(self, event):
        offset = self.timelineCtrl.GetValue()
        if self.playbackTimer.IsRunning():
            secsPlayed = time.strftime('%M:%S', time.gmtime(offset))
            self.trackCounter.SetLabel(secsPlayed)
            self.mplayer.SetProperty('time_pos', offset)

            self.SetFocus()

            if (not self.srtFile is None) and (not self.srtParsed is None):
                i = 0
                while i < len(self.srtParsed):
                    if self.srtParsed[i].start.ordinal <= offset * 1000 <= self.srtParsed[i].end.ordinal:
                        self.srtIndex = i
                        self.subtitle.SetValue(re.compile(r'<[^>]+>').sub('', self.srtParsed[self.srtIndex].text))
                        break
                    i += 1
                if self.srtIndex != i:
                    self.strIndex = 0
                    self.subtitle.SetValue("")

    #----------------------------------------------------------------------
    def on_update_playback(self, event):
        """
        Updates playback slider and track counter
        @param event:
        """

        if not self.playbackTimer.IsRunning():
            return

        try:
            offset = self.mplayer.GetTimePos()
        except:
            return

        if offset is None:
            return

        mod_off = str(offset)[-1]
        if mod_off == '0':
            offset = int(offset)
            self.timelineCtrl.SetValue(offset)

            secsPlayed = time.strftime('%M:%S', time.gmtime(offset))
            self.trackCounter.SetLabel(secsPlayed)
            if (not self.srtFile is None) and (not self.srtParsed is None):
                i = self.srtIndex
                while i < len(self.srtParsed):
                    if self.srtParsed[i].start.ordinal <= offset * 1000 <= self.srtParsed[i].end.ordinal:
                        if (i == 0 or i != self.srtIndex):
                            self.srtIndex = i
                            self.subtitle.SetValue(re.compile(r'<[^>]+>').sub('', self.srtParsed[self.srtIndex].text))
                        break
                    i += 1

    #----------------------------------------------------------------------
    def on_mouse_wheel(self, event):
        z = event.GetWheelRotation()
        if z is None or z == 0:
            return

        z = 5 if z > 0 else -5

        self.currentVolume += z
        self.volumeCtrl.SetValue(self.currentVolume)

        if self.playbackTimer.IsRunning():
            self.mplayer.SetProperty("volume", self.currentVolume)

    #----------------------------------------------------------------------
    def on_key_down(self, event):
        key = event.GetKeyCode()
        if key == wx.WXK_ESCAPE:
            self.Close()

        if key == wx.WXK_SPACE:
            self.on_pause(event)

        if key == wx.WXK_PAGEDOWN:
            self.on_next(event)

        if key == wx.WXK_PAGEUP:
            self.on_prev(event)

        event.Skip()


    #----------------------------------------------------------------------
    def on_close_window(self, event):
        self.mplayer.Destroy()
        self.Destroy()

    #----------------------------------------------------------------------
    def on_resize(self, event):
        self.panel.Layout()
        self.panel.SetFocus()


class LinguaTranslateDialog(wx.Dialog):
    langNames = [_('English'), _('Russian'), _('Spanish'), _('Portugese'), _('Brazilian'), _('French'), _('Deutch'),
                 _('Italian')]
    langISO = ['en', 'ru', 'es', 'pt-pt', 'pt-br', 'fr', 'de', 'it']
    translateValue = ''

    def __init__(self, parent, selectedText):
        wx.Dialog.__init__(self,
                           parent,
                           id=wx.ID_ANY, title=_(u"Translation of selected text"),
                           pos=wx.DefaultPosition, size=wx.Size(500, 400), style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        translateSizer = wx.BoxSizer(wx.VERTICAL)
        translateSizer.SetMinSize(wx.Size(-1, 240))

        langSizer = wx.BoxSizer(wx.HORIZONTAL)
        langSizer.SetMinSize(wx.Size(-1, 30))

        toolSizer = wx.BoxSizer(wx.VERTICAL)
        toolSizer.SetMinSize(wx.Size(-1, 80))

        self.sourceText = wx.StaticText(self,
                                        wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(-1, 40), wx.ALIGN_CENTRE)
        self.sourceText.Wrap(-1)
        self.sourceText.SetFont(wx.Font(14, 74, 90, 90, False, "Consolas"))
        self.sourceText.SetForegroundColour(wx.Colour(255, 255, 255))
        self.sourceText.SetBackgroundColour(wx.Colour(0, 0, 0))
        self.sourceText.SetMinSize(wx.Size(-1, 40))
        self.sourceText.SetLabel(selectedText)

        translateSizer.Add(self.sourceText, 0, wx.ALL | wx.EXPAND, 5)

        self.translateText = wx.StaticText(self,
                                           wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(-1, 200),
                                           wx.ALIGN_LEFT)
        self.translateText.Wrap(-1)
        self.translateText.SetFont(wx.Font(14, 74, 90, 90, False, "Consolas"))
        self.translateText.SetMinSize(wx.Size(-1, 200))

        translateSizer.Add(self.translateText, 0, wx.ALL | wx.EXPAND, 5)

        self.sourceLangLabel = wx.StaticText(self, wx.ID_ANY, _(u"Source"), wx.DefaultPosition, wx.Size(-1, 20), 0)
        self.sourceLangLabel.Wrap(-1)
        langSizer.Add(self.sourceLangLabel, 0, wx.ALL, 5)

        self.sourceLang = combo.BitmapComboBox(self,
                                               wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(-1, 20), "",
                                               wx.CB_READONLY)
        self.build_flag_combobox(self.sourceLang, )
        self.build_flag_combobox(self.sourceLang, selectedLang=_("en"))
        langSizer.Add(self.sourceLang, 0, wx.ALL, 5)

        self.targetLangLabel = wx.StaticText(self, wx.ID_ANY, _(u"Translate"), wx.DefaultPosition, wx.Size(-1, 20), 0)
        self.targetLangLabel.Wrap(-1)
        langSizer.Add(self.targetLangLabel, 0, wx.ALL, 5)

        self.targetLang = combo.BitmapComboBox(self,
                                               wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, "",
                                               wx.CB_READONLY)
        self.targetLang.SetMinSize(wx.Size(-1, 20))
        self.build_flag_combobox(self.targetLang, selectedLang=_("ru"))
        langSizer.Add(self.targetLang, 0, wx.ALL, 5)

        self.okButton = wx.Button(self, wx.ID_OK, _(u"Continue"), wx.DefaultPosition, wx.Size(-1, -1), 0)
        toolSizer.Add(self.okButton, 0, wx.ALL | wx.EXPAND, 2)

        self.addButton = wx.Button(self, wx.ID_ANY, _(u"Add to Lingualeo Dictionary"), wx.DefaultPosition,
                                   wx.Size(-1, -1), 0)
        toolSizer.Add(self.addButton, 0, wx.ALL | wx.EXPAND, 2)

        mainSizer.Add(translateSizer, 0, wx.EXPAND, 5)
        mainSizer.Add(langSizer, 0, wx.ALL | wx.EXPAND, 5)
        mainSizer.Add(toolSizer, 0, wx.ALL | wx.EXPAND, 5)

        self.sourceLang.Bind(wx.EVT_COMBOBOX, self.on_change_lang)
        self.targetLang.Bind(wx.EVT_COMBOBOX, self.on_change_lang)
        self.addButton.Bind(wx.EVT_BUTTON, self.on_add_context)
        self.Bind(wx.EVT_INIT_DIALOG, self.on_init_dialog)

        self.SetSizer(mainSizer)
        self.Layout()
        self.CentreOnParent(wx.BOTH)
        self.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))
        self.SetFocus()

    #----------------------------------------------------------------------
    def build_flag_combobox(self, combobox, selectedLang=None):
        """

        @param combobox:
        @param selectedLang:
        @return:
        """
        if not isinstance(combobox, combo.BitmapComboBox):
            return

        combobox.Clear()

        i = 0
        while i < len(LinguaTranslateDialog.langISO):
            langId = LinguaTranslateDialog.langISO[i]
            langName = LinguaTranslateDialog.langNames[i]
            img = wx.Bitmap(os.path.join(linguaBitmapDir, 'flags', langId + '.png'))
            combobox.Append(langName, bitmap=img)
            i += 1

        if not selectedLang is None:
            i = 0
            while i < len(LinguaTranslateDialog.langISO):
                if LinguaTranslateDialog.langISO[i] == selectedLang:
                    combobox.SetSelection(i)
                    break
                i += 1

    #----------------------------------------------------------------------
    def translate_list(self, translated_value, data):
        """print parameters from list"""
        for val in data:
            if isinstance(val, basestring):
                translated_value += "\t " + val + "\n"
        return translated_value

    # noinspection PyBroadException
    def translate(self):
        url = "http://translate.google.com/translate_a/t?%s"
        list_of_params = {'client': 't',
                          'hl': linguaLocale.GetCanonicalName()[0:2],
                          'multires': '1', }

        list_of_params.update({'text': re.sub(r'[^\w\s"\']+', '', self.sourceText.GetLabelText()),
                               'sl': LinguaTranslateDialog.langISO[self.sourceLang.GetSelection()],
                               'tl': LinguaTranslateDialog.langISO[self.targetLang.GetSelection()]})

        request = urllib2.Request(url % urllib.urlencode(list_of_params),
                                  headers={'User-Agent': 'Mozilla/5.0', 'Accept-Charset': 'utf-8'})
        res = urllib2.urlopen(request).read()

        fixed_json = re.sub(r',{2,}', ',', res).replace(',]', ']')
        data = json.loads(fixed_json)

        #simple translation
        translated_value = data[0][0][0] + "\n"
        self.translateValue = data[0][0][0]

        #abbreviation
        if not isinstance(data[1], basestring):
            translated_value += data[1][0][0] + "\n"
            translated_value = self.translate_list(translated_value, data[1][0][1])

        #interjection
        try:
            if not isinstance(data[1][1], basestring):
                translated_value += data[1][1][0] + "\n"
                translated_value = self.translate_list(translated_value, data[1][1][1])
        except Exception:
            translated_value += _("no interjection") + "\n"

        self.translateText.SetLabel(translated_value)
        self.translateText.Wrap(self.translateText.GetSize().width)

    #----------------------------------------------------------------------
    def on_init_dialog(self, event):
        self.translate()
        self.SetFocus()

    #----------------------------------------------------------------------
    def on_change_lang(self, event):
        self.translate()
        event.Skip()

    #----------------------------------------------------------------------
    def on_add_context(self, event):
        dlg = LinguaLeoDialog(self)
        dlg.ShowModal()
        dlg.Destroy()
        event.Skip()


class LinguaLeoDialog(wx.Dialog):
    rememberCookie = False
    def __init__( self, parent ):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY,
                           title=_(u"Add to LinguaLeo Personal Dictionary"),
                           pos=wx.DefaultPosition,
                           size=wx.Size(400, 200),
                           style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.loginLabel = wx.StaticText(self, wx.ID_ANY, _(u"LinguaLeo account email"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.loginLabel.Wrap(-1)
        mainSizer.Add(self.loginLabel, 0, wx.ALL, 5)

        self.login = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(380, -1), 0)
        mainSizer.Add(self.login, 0, wx.ALL, 5)

        self.passwordLabel = wx.StaticText(self, wx.ID_ANY, _(u"Password"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.passwordLabel.Wrap(-1)
        mainSizer.Add(self.passwordLabel, 0, wx.ALL, 5)

        self.password = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(380, -1), 0)
        mainSizer.Add(self.password, 0, wx.ALL, 5)

        self.addButton = wx.Button(self, wx.ID_OK, _(u"Add"), wx.DefaultPosition, wx.Size(380, -1), 0)
        mainSizer.Add(self.addButton, 0, wx.ALL, 5)

        self.cancelButton = wx.Button(self, wx.ID_CANCEL, _(u"Cancel"), wx.DefaultPosition, wx.Size(380, -1), 0)
        mainSizer.Add(self.cancelButton, 0, wx.ALL, 5)

        self.addButton.Bind(wx.EVT_BUTTON, self.on_add_context)

        self.SetSizer(mainSizer)
        self.Layout()

        self.Centre(wx.BOTH)

    #----------------------------------------------------------------------
    def on_add_context(self, event):
        parentDlg = self.GetParent()
        mainWindow = parentDlg.GetParent()

        cookies = cookielib.LWPCookieJar()
        handlers = [
            urllib2.HTTPHandler(),
            urllib2.HTTPSHandler(),
            urllib2.HTTPCookieProcessor(cookies)
        ]
        opener = urllib2.build_opener(*handlers)
        if LinguaLeoDialog.rememberCookie == False:
            params = {'email': self.login.GetValue(),
                      'password': self.password.GetValue()}
            params = dict([k.encode('utf-8'),v.encode('utf-8')] for k,v in params.items())
            request = urllib2.Request("http://lingualeo.com/api/user/login",
                                      data=urllib.urlencode(params),
                                      headers={'User-Agent': 'LinguaCinema', 'Accept-Charset': 'utf-8'})
            response = opener.open(request)
            for cookie in cookies:
                if cookie.name == 'remember':
                    LinguaLeoDialog.rememberCookie = cookie.value
            response = response.read()
            user = json.loads(response)


        params = {'word': parentDlg.sourceText.GetLabelText(),
                  'tword': parentDlg.translateValue,
                  'context': mainWindow.subtitle.GetValue() }
        params = dict([k.encode('utf-8'),v.encode('utf-8')] for k,v in params.items())
        request = urllib2.Request("http://lingualeo.com/api/login",
                                  data=urllib.urlencode(params),
                                  headers={'User-Agent': 'LinguaCinema',
                                           'Accept-Charset': 'utf-8',
                                           'Cookie:': u'remember=%s' % LinguaLeoDialog.rememberCookie})

        response = opener.open(request)
        addWord = json.loads(response.read())
        print addWord

if __name__ == "__main__":
    import os, sys

    paths = [
        r'mplayer2.exe',
        r'mplayer2',
        r'mplayer.exe',
        r'mplayer'
        r'C:\Program Files (x86)\Mplayer2\mplayer2.exe',
        r'C:\Program Files\Mplayer2\mplayer2.exe',
        r'C:\Program Files (x86)\Mplayer\mplayer.exe',
        r'C:\Program Files\Mplayer\mplayer.exe',
    ]

    if getattr(sys, 'frozen', None):
        paths.extend([
            os.path.join(sys._MEIPASS, 'mplayer2.exe'),
            os.path.join(sys._MEIPASS, 'mplayer2')
        ])

    mplayerPath = None
    for path in paths:
        if os.path.exists(path):
            mplayerPath = path
            break

    if not mplayerPath:
        print "mplayer not found!"
        sys.exit()

    gettext.install('LignuaCinema', './locale', unicode=True)
    app = wx.App(redirect=False)

    localedir = os.path.join(linguaBaseDir, "locale")
    langid = wx.LANGUAGE_DEFAULT
    domain = "LinguaCinema"

    linguaLocale = wx.Locale(langid)
    linguaLocale.AddCatalogLookupPathPrefix(localedir)
    linguaLocale.AddCatalog(domain)

    frame = LinguaFrame(None, -1, _('LinguaCinema watch movie and learn language'), mplayerPath)
    app.MainLoop()