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

import json
import requests
import copy


class BadRequest(Exception):
    ''' Bad request as sent to server. '''
    pass

class UnknownStyle(Exception):
    ''' Unknown style. '''
    pass

class FieldNotSet(Exception):
    ''' Required parameter not set. '''
    pass

class LengthOutOfRange(Exception):
    ''' Length of the field is beyond limit. '''
    pass


class Picovico():
    """ Picovico object."""
    def __init__(self, access_token):
        self._host           = 'https://api.picovico.com'
        self._access_token   = access_token
        self._styles         = None
        self.getStyles()

    class Video():
        ''' Picovico Video object '''
        def __init__(self, picovico, style, music, callback_url):
            if not style:
                FieldNotSet('Style is required.')

            if not music:
                FieldNotSet('music is required.')

            if not callback_url:
                FieldNotSet('callback_url is required.')

            self._picovico      = picovico
            self._style         = style
            self._music         = music
            self._callback_url  = callback_url
            self._frames        = []
            self._extra_fields  = {}
        
        def setExtraField(self, key, value):
            ''' Sets the extra fields for the video.

            Keyword arguments:
            key          -- The param name.
            value        -- And its value.
            '''
            self._extra_fields[key] = value

        def addImage(self, image_url, caption=None):
            # Image url is required field
            if not image_url:
                FieldNotSet('image_url is required in a image.')
            # if not empty check for length
            if caption and len(caption) > 140:
                LengthOutOfRange("Image Caption should not exceed 140 chars. [%s]" % caption)

            # Update the list
            data = {'url': image_url, 'text': caption }
            self._frames.append({'frame': 'image_frame', 'data': data})
            
        def addText(self, title=None, text=None):
            # Both field cannot be empty
            if not (title or text):
                FieldNotSet('Both title and text cannot be empty in Text Frame')

            # if not empty check for length
            if title and len(title) > 64:
                LengthOutOfRange("Title should not exceed 64 chars. '%s'" % caption)
            if text and len(text) > 140:
                LengthOutOfRange("Text should not exceed 140 chars. '%s'" % caption)

            # Update the list
            data = {'title': title, 'text': text }
            self._frames.append({'frame': 'text_frame', 'data': data})

        def create(self):
            # Check the style
            style = self._picovico._getStyle(self._style)
            if not style:
                raise UnknownStyle(self._style)

            # Check extra params
            for ef in style['extra_field']:
                if not ef['machine_name'] in self._extra_fields.keys():
                    # The field must be set, at least to None or '' -- Just a check to make sure that user won't leave this field empty unknowingly
                    raise FieldNotSet(ef['machine_name'])

                # check for length
                value = self._extra_fields[ef['machine_name']]
                if value and 'max_length' in ef and ef['max_length'] != 0 and len(value) > ef['max_length']:            # 0 refers to unlimited length
                    LengthOutOfRange("%s should not exceed %s chars. '%s'" % (ef['machine_name'], ef['max_length'], value) )

            # Everything is fine. Send the request.
            data = copy.deepcopy(self._extra_fields)
            data['callback_url'] = self._callback_url
            data['music_url'] = self._music
            data['frames'] = self._frames
            data['theme'] = self._style
            
            data = json.dumps(data)
            url = '%s/%s?access_token=%s' % (self._picovico._host, 'create', self._picovico._access_token)
            response=requests.post(url,data={"vdd": data})

            self._picovico._raiseIfError(response)
            response=json.loads(response.content)
            return response['token']
        
    def _getStyle(self, style_name):
        ''' Returns the complete style object from its name.

        Keyword arguments:
        style_name  -- The style machine name.
        '''

        for style in self._styles['themes']:
            if style['machine_name'] == style_name:
                return style
    
    def _getFrame(self, frame_name):
        ''' Returns the Frame details from the frame_name.

        Keyword arguments:
        frame_name  -- The frame machine name.
        '''

        for frame in self._styles['frames']:
            if frame['machine_name'] == frame_name:
                return frame


    def _raiseIfError(self, response):
        ''' Throws an exception if the response is error. '''
        
        if response.status_code==200:
            return

        raise BadRequest(response.status_code, response.content)
        
    def getStyles(self):
        ''' Returns the list of styles available '''
        if self._styles:
            return self._styles

        url = '%s/%s?access_token=%s' % (self._host, 'themes', self._access_token)
        response    = requests.get(url)
        self._raiseIfError(response)        
        self._styles = json.loads(response.content)

    def video(self, style, music, callback_url):
        ''' Creates an empty video object and returns it.

        Keyword arguments:
        style        -- The machine_name of the style to be used for the video.
        music        -- The public-url of the music to be used for video.
        callback_url -- The url to be called when the video rendering is completed.
        '''

        return Picovico.Video(self, style, music, callback_url)
        
       
