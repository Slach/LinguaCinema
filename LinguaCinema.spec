# -*- mode: python -*-
a = Analysis(['LinguaCinema.py'],
             pathex=['C:\\usr\\local\\apache\\htdocs\\lingualeo.ru\\src\\Lingualeo_player'],
             hiddenimports=[],
             hookspath=None)
a.datas += [
            ('bitmaps/player_next.png', 'C:\\usr\\local\\apache\\htdocs\\lingualeo.ru\\src\\Lingualeo_player\\bitmaps\\player_next.png',  'DATA'),
            ('bitmaps/player_play.png', 'C:\\usr\\local\\apache\\htdocs\\lingualeo.ru\\src\\Lingualeo_player\\bitmaps\\player_play.png',  'DATA'),
            ('bitmaps/player_prev.png', 'C:\\usr\\local\\apache\\htdocs\\lingualeo.ru\\src\\Lingualeo_player\\bitmaps\\player_prev.png',  'DATA'),
            ('bitmaps/player_stop.png', 'C:\\usr\\local\\apache\\htdocs\\lingualeo.ru\\src\\Lingualeo_player\\bitmaps\\player_stop.png',  'DATA'),
            ('bitmaps/player_pause.png', 'C:\\usr\\local\\apache\\htdocs\\lingualeo.ru\\src\\Lingualeo_player\\bitmaps\\player_pause.png',  'DATA'),
            ('mplayer2.exe', 'C:\\usr\\local\\apache\\htdocs\\lingualeo.ru\\src\\Lingualeo_player\\mplayer2.exe',  'DATA'),
            ('mplayer/subfont.ttf', 'C:\\usr\\local\\apache\\htdocs\\lingualeo.ru\\src\\Lingualeo_player\\mplayer\\subfont.ttf',  'DATA'),
            ('bitmaps/flags/en.png', 'C:\\usr\\local\\apache\\htdocs\\lingualeo.ru\\src\\Lingualeo_player\\bitmaps\\flags\\en.png',  'DATA'),
            ('bitmaps/flags/ru.png', 'C:\\usr\\local\\apache\\htdocs\\lingualeo.ru\\src\\Lingualeo_player\\bitmaps\\flags\\ru.png',  'DATA'),
            ('bitmaps/flags/es.png', 'C:\\usr\\local\\apache\\htdocs\\lingualeo.ru\\src\\Lingualeo_player\\bitmaps\\flags\\es.png',  'DATA'),
            ('bitmaps/flags/fr.png', 'C:\\usr\\local\\apache\\htdocs\\lingualeo.ru\\src\\Lingualeo_player\\bitmaps\\flags\\fr.png',  'DATA'),
            ('bitmaps/flags/de.png', 'C:\\usr\\local\\apache\\htdocs\\lingualeo.ru\\src\\Lingualeo_player\\bitmaps\\flags\\de.png',  'DATA'),
            ('bitmaps/flags/it.png', 'C:\\usr\\local\\apache\\htdocs\\lingualeo.ru\\src\\Lingualeo_player\\bitmaps\\flags\\it.png',  'DATA'),
            ('bitmaps/flags/pt-pt.png', 'C:\\usr\\local\\apache\\htdocs\\lingualeo.ru\\src\\Lingualeo_player\\bitmaps\\flags\\pt-pt.png',  'DATA'),
            ('bitmaps/flags/pt-br.png', 'C:\\usr\\local\\apache\\htdocs\\lingualeo.ru\\src\\Lingualeo_player\\bitmaps\\flags\\pt-br.png',  'DATA'),
           ]
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join('build\\pyi.win32\\LinguaCinema', 'LinguaCinema.exe'),
          debug=False,
          strip=None,
          upx=True,
          console=True )

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name=os.path.join('dist', 'LinguaCinema'))
