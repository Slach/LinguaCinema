#===================================================================================================
# Original code here https://github.com/nicoddemus/ss
#===================================================================================================
from __future__ import with_statement
import xmlrpclib
import difflib
import os
import sys
import struct
import gzip
import urllib
import tempfile
import shutil


#===================================================================================================
# QueryOpenSubtitles
# @todo added LinguaCinema Registered User Agent
#===================================================================================================
def QueryOpenSubtitles(movie_filenames, language):
    uri = 'http://api.opensubtitles.org/xml-rpc'
    server = xmlrpclib.Server(uri, verbose=0, allow_none=True, use_datetime=True)
    login_info = server.LogIn('', '', 'en', 'OS Test User Agent')
    token = login_info['token']

    try:
        result = {}

        for movie_filename in movie_filenames:
            search_queries = [
                dict(
                    moviehash=CalculateHashForFile(movie_filename),
                    moviebytesize=str(os.path.getsize(movie_filename)),
                    sublanguageid=language,
                ),
                dict(
                    query=os.path.basename(os.path.splitext(movie_filename)[0]),
                    sublanguageid=language,
                )
            ]

            response = server.SearchSubtitles(token, search_queries)
            search_results = response['data']

            if search_results:
                result[movie_filename] = search_results

        return result
    finally:
        server.LogOut(token)


#===================================================================================================
# FindBestSubtitleMatches
#===================================================================================================
def FindBestSubtitleMatches(movie_filenames, language):
    all_search_results = QueryOpenSubtitles(movie_filenames, language)

    for movie_filename in movie_filenames:

        search_results = all_search_results.get(movie_filename, [])
        possibilities = [search_result['SubFileName'] for search_result in search_results]
        basename = os.path.splitext(os.path.basename(movie_filename))[0]
        closest_matches = difflib.get_close_matches(basename, possibilities)
        if closest_matches:
            filtered = [x for x in search_results if x['SubFileName'] in closest_matches]
            filtered.sort(key=lambda x: (closest_matches.index(x['SubFileName']), -x['SubDownloadsCnt']))
            search_result = filtered[0]
            yield movie_filename, search_result['SubDownloadLink'], '.' + search_result['SubFormat']
        else:
            yield movie_filename, None, None


#===================================================================================================
# ObtainSubtitleFilename
#===================================================================================================
def ObtainSubtitleFilename(movie_filename, language, subtitle_ext):
    dirname = os.path.dirname(movie_filename)
    basename = os.path.splitext(os.path.basename(movie_filename))[0]

    # possibilities where we don't override
    filenames = [
        #  -> movie.srt
        os.path.join(dirname, basename + subtitle_ext),
        #  -> movie.eng.srt
        os.path.join(dirname, '%s.%s%s' % (basename, language, subtitle_ext)),
    ]
    for filename in filenames:
        if not os.path.isfile(filename):
            return filename

    # use also ss on the extension and always overwrite
    #  -> movie.eng.ss.srt
    return os.path.join(dirname, '%s.%s.%s%s' % (basename, language, 'ss', subtitle_ext))


#===================================================================================================
# DownloadSub
#===================================================================================================
def DownloadSub(subtitle_url, subtitle_filename):
    # first download it and save to a temp dir
    urlfile = urllib.urlopen(subtitle_url)
    try:
        gzip_subtitle_contents = urlfile.read()
    finally:
        urlfile.close()

    tempdir = tempfile.mkdtemp()
    try:
        basename = subtitle_url.split('/')[-1]
        tempfilename = os.path.join(tempdir, basename)
        with file(tempfilename, 'wb') as f:
            f.write(gzip_subtitle_contents)

        f = gzip.GzipFile(tempfilename, 'r')
        try:
            subtitle_contents = f.read()
        finally:
            f.close()

        # copy it over the new filename
        with file(subtitle_filename, 'w') as f:
            f.write(subtitle_contents)
    finally:
        shutil.rmtree(tempdir)


#===================================================================================================
# FindMovieFiles
#===================================================================================================
def FindMovieFiles(input_names, recursive=False):
    extensions = {'.avi', '.mp4', '.mpg', '.mkv'}
    returned = set()

    for input_name in input_names:
        print input_name
        if os.path.isfile(input_name) and input_name not in returned:
            yield input_name
            returned.add(input_name)
        else:
            names = os.listdir(input_name)
            for name in names:
                result = os.path.join(input_name, name)
                if name[-4:] in extensions:
                    if result not in returned:
                        yield result
                        returned.add(result)

                elif os.path.isdir(result) and recursive:
                    for x in FindMovieFiles([result], recursive):
                        yield x


#===================================================================================================
# HasSubtitle
#===================================================================================================
def HasSubtitle(filename):
    # list of subtitle formats obtained from opensubtitles' advanced search page.
    # formats = ['.sub', '.srt', '.ssa', '.smi', '.mpl']
    formats = ['.srt']
    basename = os.path.splitext(filename)[0]
    for ext in formats:
        if os.path.isfile(basename + ext):
            return True

    return False


#===================================================================================================
# CalculateHashForFile
#===================================================================================================
def CalculateHashForFile(name):
    """
    Calculates the hash for the given filename.

    Algorithm from: http://trac.opensubtitles.org/projects/opensubtitles/wiki/HashSourceCodes

    @param name: str
        Path to the file

    @return: str
        The calculated hash code, as an hex string.
    """
    longlongformat = 'q'  # long long
    bytesize = struct.calcsize(longlongformat)

    f = open(name, "rb")

    filesize = os.path.getsize(name)
    movie_hash = filesize

    if filesize < 65536 * 2:
        return "SizeError"

    for x in range(65536 / bytesize):
        movie_buffer = f.read(bytesize)
        (l_value,) = struct.unpack(longlongformat, movie_buffer)
        movie_hash += l_value
        movie_hash = movie_hash & 0xFFFFFFFFFFFFFFFF #to remain as 64bit number

    f.seek(max(0, filesize - 65536), 0)
    for x in range(65536 / bytesize):
        movie_buffer = f.read(bytesize)
        (l_value,) = struct.unpack(longlongformat, movie_buffer)
        movie_hash += l_value
        movie_hash = movie_hash & 0xFFFFFFFFFFFFFFFF

    f.close()
    returnedhash = "%016x" % movie_hash
    return returnedhash


#===================================================================================================
# DownloadSubtitleForMovie
#===================================================================================================
def DownloadSubtitleForMovie(filename, language):
    input_filenames = list(FindMovieFiles([filename], recursive=False))
    if not input_filenames:
        sys.stdout.write('No files to search subtitles for. Aborting.\n')
        return False

    skipped_filenames = []
    new_input_filenames = []
    for input_filename in input_filenames:
        if HasSubtitle(input_filename):
            skipped_filenames.append(input_filename)
        else:
            new_input_filenames.append(input_filename)
    input_filenames = new_input_filenames

    def PrintStatus(text, status):
        spaces = 70 - len(text)
        if spaces < 2:
            spaces = 2
        sys.stdout.write('%s%s%s\n' % (text, ' ' * spaces, status))


    sys.stdout.write('Language: %s\n' % language)
    if skipped_filenames:
        print 'Skipping %d files that already have subtitles.' % len(skipped_filenames)

    if not input_filenames:
        return False

    sys.stdout.write('Querying OpenSubtitles.org for %d file(s)...\n' % len(input_filenames))
    sys.stdout.write('\n')

    matches = []
    for (movie_filename, subtitle_url, subtitle_ext) in sorted(
            FindBestSubtitleMatches(input_filenames, language=language)):
        if subtitle_url:
            status = 'OK'
        else:
            status = 'No matches found.'

        PrintStatus('- %s' % os.path.basename(movie_filename), status)

        if subtitle_url:
            subtitle_filename = ObtainSubtitleFilename(movie_filename, language, subtitle_ext)
            matches.append((movie_filename, subtitle_url, subtitle_ext, subtitle_filename))

    if not matches:
        return False

    sys.stdout.write('\n')
    sys.stdout.write('Downloading...\n')
    for (movie_filename, subtitle_url, subtitle_ext, subtitle_filename) in matches:
        DownloadSub(subtitle_url, subtitle_filename)
        PrintStatus(' - %s' % os.path.basename(subtitle_filename), 'DONE')
    return True