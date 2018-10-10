# -*- coding: utf-8 -*-
"""
    __init__

    A library to get text to speech from micrsoft translation engine.

    See: https://www.microsoft.com/cognitive-services/en-us/speech-api/documentation/api-reference-rest/bingvoiceoutput

"""

try:
    import simplejson as json
except ImportError:
    import json
import logging

try:
    import httplib
except ImportError:
    import http.client as httplib


class BadRequestException(Exception):
    def __init__(self, message):
        self.message = "{} {}".format(
            message.status,
            message.reason
            )
        super(
            BadRequestException,
            self
            ).__init__(
                self.message
                )
        
class AuthException(Exception):
    def __init__(self, message):
        self.message = "{} {}".format(
            message.status,
            message.reason
            )
        super(
            AuthException,
            self
            ).__init__(
                self.message
                )
        
class LanguageException(Exception):
    def __init__(self, message):
        self.message = "{}".format(
            message
            )
        super(
            LanguageException,
            self
            ).__init__(
                self.message
                )


class Translator(object):
    """
    Implements API for the Microsoft Translator service
    """
    auth_host = 'api.cognitive.microsoft.com'
    auth_path = '/sts/v1.0/issueToken'
    base_host = 'speech.platform.bing.com'
    base_path = ''
    def __init__(self, client_secret, debug=False):
        """
        :param clien_secret: The API key provided by Azure
        :param debug: If true, the logging level will be set to debug
        """
        self.client_secret = client_secret
        self.debug = debug
        self.logger = logging.getLogger(
            "bingtts"
            )
        self.access_token = None
        if self.debug:
            self.logger.setLevel(
                level=logging.DEBUG
                )
        
    def get_access_token(self):
        """
        Retrieve access token from Azure.
        
        :return: Text of the access token to be used with requests
        """
        headers={
            'Ocp-Apim-Subscription-Key' : self.client_secret
            }
        conn = httplib.HTTPSConnection(
            self.auth_host
            )
        conn.request(
            method="POST",
            url=self.auth_path,
            headers=headers,
            body=""
            )
        response = conn.getresponse()    
        if int(response.status) != 200:
            raise AuthException(
                response
                )
        return response.read()
        
    def call(self, headerfields, path, body):
        """
        Calls Bing API and retrieved audio
        
        :param headerfields: Dictionary of all headers to be sent
        :param path: URL path to be appended to requests
        :param body: Content body to be posted
        """
        
        # If we don't have an access token, get one
        if not self.access_token:
            self.access_token = self.get_access_token()
        
        # Set authorization header to token we just retrieved
        headerfields["Authorization"] = "Bearer {}".format(
            self.access_token.decode(
                'utf-8'
                )
            )
        # Post to Bing API
        urlpath = "/".join(
            [
                self.base_path,
                path
            ]
            )
        conn = httplib.HTTPSConnection(
            self.base_host
            )
        conn.request(
            method="POST",
            url=urlpath,
            headers=headerfields,
            body=body.encode('utf-8')
            )
        resp = conn.getresponse()
        # If token was expired, get a new one and try again
        if int(resp.status) == 401:
            self.access_token = None
            return self.call(
                headerfields,
                path,
                body
                )
        
        # Bad data or problem, raise exception    
        if int(resp.status) != 200:
            raise BadRequestException(
                resp
                )
            
        return resp.read()
        
    def speak(self, text, lang, voice, fileformat):
        """
        Gather parameters and call.
        
        :param text: Text to be sent to Bing TTS API to be
                     converted to speech
        :param lang: Language to be spoken
        :param voice: Voice of the speaker
        :param fileformat: File format (see link below)
        
        Name maps and file format specifications can be found here:
        https://docs.microsoft.com/en-us/azure/cognitive-services/speech/api-reference-rest/bingvoiceoutput
        """
        
        namemap = {
            "ar-EG" : ["Hoda"],
            "ar-SA" : ["Naayf"],
            "bg-BG" : ["Ivan"],
            "ca-ES" : ["HerenaRUS"],
            "cs-CZ" : ["Jakub"],
            "da-DK" : ["HelleRUS"],
            "de-AT" : ["Michael"],
            "de-CH" : ["Karsten"],
            "de-DE" : ["Hedda", "HeddaRUS", "Stefan, Apollo"],
            "el-GR" : ["Stefanos"],
            "en-AU" : ["Catherine", "HayleyRUS"],
            "en-CA" : ["Linda", "HeatherRUS"],
            "en-GB" : ["Susan, Apollo", "HazelRUS", "George, Apollo"],
            "en-IE" : ["Sean"],
            "en-IN" : ["Heera, Apollo", "PriyaRUS", "Ravi, Apollo"],
            "en-US" : ["ZiraRUS", "JessaRUS", "BenjaminRUS"],
            "es-ES" : ["Laura, Apollo", "HelenaRUS", "Pablo, Apollo"],
            "es-MX" : ["HildaRUS", "Raul, Apollo"],
            "fi-FI" : ["HeidiRUS"],
            "fr-CA" : ["Caroline", "HarmonieRUS"],
            "fr-CH" : ["Guillaume"],
            "fr-FR" : ["Julie, Apollo", "HortenseRUS", "Paul, Apollo"],
            "he-IL" : ["Asaf"],
            "hi-IN" : ["Kalpana, Apollo", "Kalpana", "Hemant"],
            "hr-HR" : ["Matej"],
            "hu-HU" : ["Szabolcs"],
            "id-ID" : ["Andika"],
            "it-IT" : ["Cosimo, Apollo","LuciaRUS"],
            "ja-JP" : ["Ayumi, Apollo", "Ichiro, Apollo", "HarukaRUS"],
            "ko-KR" : ["HeamiRUS"],
            "ms-MY" : ["Rizwan"],
            "nb-NO" : ["HuldaRUS"],
            "nl-NL" : ["HannaRUS"],
            "pl-PL" : ["PaulinaRUS"],
            "pt-BR" : ["HeloisaRUS", "Daniel, Apollo"],
            "pt-PT" : ["HeliaRUS"],
            "ro-RO" : ["Andrei"],
            "ru-RU" : ["Irina, Apollo", "Pavel, Apollo","EkaterinaRUS"],
            "sk-SK" : ["Filip"],
            "sl-SI" : ["Lado"],
            "sv-SE" : ["HedvigRUS"],
            "ta-IN" : ["Valluvar"],
            "th-TH" : ["Pattara"],
            "tr-TR" : ["SedaRUS"],
            "vi-VN" : ["An"],
            "zh-CN" : ["HuihuiRUS", "Yaoyao, Apollo", "Kangkang, Apollo"],
            "zh-HK" : ["Tracy, Apollo", "TracyRUS", "Danny, Apollo"],
            "zh-TW" : ["Yating, Apollo", "HanHanRUS", "Zhiwei, Apollo"]
            }
        if not text:
            raise LanguageException(
                "Text to convert is not defined!"
                )
        if not voice and not lang:
            # Default to English voice if nothing is defined
            voice = 'ZiraRUS'
            lang = 'en-US'
        if voice and not lang:
            raise LanguageException(
                "Voice defined witout defining language!"
                )
        if lang not in namemap:
            raise LanguageException(
                "Requested language {} not available!".format(
                    lang
                    )
                )
        if lang and not voice:
            # Default to first voice in array
            voice = namemap[lang][0]
        if voice not in namemap[lang]:
            raise LanguageException(
                "Requested language {} does not have voice {}!".format(
                    lang,
                    voice
                    )
                )
        if not fileformat:
            fileformat = 'riff-8khz-8bit-mono-mulaw'
        # Set the service name sent to Bing TTS
        servicename = "Microsoft Server Speech Text to Speech Voice ({}, {})".format(
            lang,
            voice
            )
            
        headers = {
            "Content-type" : "application/ssml+xml",
            "X-Microsoft-OutputFormat" : fileformat,
            "X-Search-AppId" : "07D3234E49CE426DAA29772419F436CA", 
            "X-Search-ClientID" : "1ECFAE91408841A480F00935DC390960", 
            "User-Agent" : "TTSForPython"
            }
            
        body = "<speak version='1.0' xml:lang='{}'><voice xml:lang='{}' xml:gender='{}' name='{}'>{}</voice></speak>".format(
            lang,
            lang,
            voice,
            servicename,
            text
            )
        
        return self.call(headers, "synthesize", body)
