import requests
import queue


class M3U8Playlist:
    base_uri = None
    playlist_elements = []
    readed_elements = []
    download_queue = None
    _m3u8_raw = ''

    def __init__(self, content=None, base_uri=''):
        self._m3u8_raw = content
        self.base_uri = base_uri
        self.download_queue = queue.Queue()
        if content:
            self.parse(content)

    def parse_pie(self, pie):
        return pie.split('\r\n')[:-1]

    def parse_raw_pies(self, raw_pies):
        return [self.parse_pie(raw_pie) for raw_pie in raw_pies]

    def parse(self, content):
        raw_pies = content.replace('\r\n\r\n', '\r\n').split('#')[1:]
        return self.parse_raw_pies(raw_pies)

    def parse_extinf(self, extinf_pie, with_base=True):
        extinf_meta_pies = extinf_pie[0].split(':')
        if not extinf_meta_pies[0] == 'EXTINF':
            return None
        extinf_meta_descr = extinf_meta_pies[1].split(',')


        if with_base:
            uri = self.base_uri + extinf_pie[1]
        else:
            uri = extinf_pie[1]

        playlist_element = {
            'attr_name': extinf_meta_pies[0],
            'duration': extinf_meta_descr[0],
            'title': extinf_meta_descr[1],
            'uri': uri
        }
        if playlist_element not in self.playlist_elements:
            self.playlist_elements.append(playlist_element)
        return playlist_element

