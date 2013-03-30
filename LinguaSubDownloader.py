from __future__ import with_statement
import xmlrpclib
import difflib
import os
import calculate_hash
import gzip
import urllib
import tempfile
import shutil
import time
import optparse

#===================================================================================================
# QueryOpenSubtitles
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
                    moviehash=calculate_hash.CalculateHashForFile(movie_filename),
                    moviebytesize=os.path.getsize(movie_filename),
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
    extensions = set(['.avi', '.mp4', '.mpg', '.mkv'])
    returned = set()

    for input_name in input_names:

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
    formats = ['.sub', '.srt', '.ssa', '.smi', '.mpl']
    basename = os.path.splitext(filename)[0]
    for format in formats:
        if os.path.isfile(basename + format):
            return True

    return False
