"""
 Copyright 2012 Picovico Pvt Ltd

 Licensed under the Apache License, Version 2.0 (the "License"); you may
 not use this file except in compliance with the License. You may obtain
 a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 License for the specific language governing permissions and limitations
 under the License.
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'../src'))

from picovico import Picovico

ACCESS_TOKEN = None
# The callback_url is called once the video task is complete.
CALLBACK_URL = 'http://exmaple.com/callback'
MUSIC_URL    = 'http://example.com/music/my_music.aac'

try:
    import apiKey.ACCESS_TOKEN
    ACCESS_TOKEN = apiKey.ACCESS_TOKEN
except:
    pass


if not ACCESS_TOKEN:
    print 'Need a access_token to execute it. You can request one at: developers@picovico.com'

picovico = Picovico(ACCESS_TOKEN)

# You can get a list of styles by calling 
# styles = picovico.getStyles()
# print styles

video = picovico.video('vanilla', MUSIC_URL, CALLBACK_URL)

video.addImage('http://farm7.static.flickr.com/6034/6227544215_fe9a9ed1ea_b.jpg', 'The predator and the prey')
video.addImage('http://farm7.static.flickr.com/6169/6228061064_413bf3da13_b.jpg')
video.addImage('http://farm7.static.flickr.com/6080/6115623115_ab728913f3_b.jpg', 'The eternal rays')
video.addText('Flora')
video.addImage('http://farm7.static.flickr.com/6014/5909306527_0ba1606f8f_b.jpg')
video.addImage('http://farm5.static.flickr.com/4079/4764595958_fee8a036f5_b.jpg')
video.addText('Photos by', 'Suraj Sapkota')

video.setExtraField('video_title_16', 'Video title')
video.setExtraField('title_text', None)

token = video.create()

# The callback will contains all metadata related to video, and this token can be used as a reference to map it
print 'Video Token: %s ' % token


