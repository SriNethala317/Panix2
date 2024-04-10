class Song:
    def __init__(self, name, artist='', img_url='test' ) -> None:
        self.song_info = {'name': name, 'artist': artist, 'img_url': img_url, "played": False, "length": 0}
    
    def __str__(self) -> str:
        return str(self.song_info)
    
    def __repr__(self) -> str:
        return str(self.song_info)
    
    def get_song_info(self):
        return self.song_info
    
    def get_name(self):
        return self.song_info['name']
    
    def get_artist(self):
        return self.song_info['artist']
    
    def get_length(self):
        return self.song_info['length']
    
    def get_image(self):
        print(self.song_info['image_url'])
        # return self.song_info['image_url']
    
    def get_filename(self):
        return self.song_info['filename']
    
    def set_length(self, length):
        self.song_info['length'] = length
    
    def set_filename(self, filename):
        self.song_info['filename'] = filename
