import time
import requests
import logging
import pytz
import datetime

from m3u8_parser import M3U8Playlist

streamlogger = logging.getLogger('stream-writer')
streamlogger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.ERROR)


"""Playlist URI"""
m3u8uri = ''
"""Playlist object"""
playlist = M3U8Playlist(base_uri='')

moscow_timezone = pytz.timezone('Europe/Moscow')

try:
    while True:
        m3u8_raw = requests.get(m3u8uri).content.decode('utf8')
        timeprefix = datetime.dat
        etime.now(moscow_timezone).strftime('%d-%m-%Y_%H%M%S')

        with open('./files/{}.stream.mp4'.format(timeprefix), 'wb+') as mp4_file_descriptor:
            for pie in playlist.parse(m3u8_raw):
                if playlist.parse_extinf(pie) is not None:
                    extinf = playlist.parse_extinf(pie)
                    streamlogger.info("Download: {}".format(extinf))

                    try:
                        uri = extinf.get('uri')
                        pie_content = requests.get(uri)
                        streamlogger.info('Success {}!'.format(uri))
                        wroted_pie = mp4_file_descriptor.write(pie_content.content)
                        streamlogger.info('Success wrote pie {} [{}kb]'.format(uri, wroted_pie/1024))
                    except Exception as error:
                        streamlogger.error("Error! Can't download pie {}. (error info: {}) ".format(uri, error))

        time.sleep(10)
except KeyboardInterrupt:
    mp4_file_descriptor.close()
    streamlogger.info("CTRL+C! Bye...")



