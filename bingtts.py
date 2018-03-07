#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import hashlib
import os
import sys
import argparse
import shutil

# Define a few maps for reference
namemap = {
            "ar-EG" : ["Hoda"],
            "ar-SA" : ["Naayf"],
            "bg-BG" : ["Hoda"],
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
            "it-IT" : ["Cosimo, Apollo"],
            "ja-JP" : ["Ayumi, Apollo", "Ichiro, Apollo", "HarukaRUS", "LuciaRUS", "EkaterinaRUS"],
            "ko-KR" : ["HeamiRUS"],
            "ms-MY" : ["Rizwan"],
            "nb-NO" : ["HuldaRUS"],
            "nl-NL" : ["HannaRUS"],
            "pl-PL" : ["PaulinaRUS"],
            "pt-BR" : ["HeloisaRUS", "Daniel, Apollo"],
            "pt-PT" : ["HeliaRUS"],
            "ro-RO" : ["Andrei"],
            "ru-RU" : ["Irina, Apollo", "Pavel, Apollo"],
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
    
formatmap = {
    "raw-8khz-8bit-mono-mulaw" : None,
    "raw-16khz-16bit-mono-pcm" : None,
    "riff-8khz-8bit-mono-mulaw" : None,
    "riff-16khz-16bit-mono-pcm" : None
}

# Get config from CLI args
i = 0
argsDict = {}
for item in sys.argv:
    if i == 0:
        i = i + 1
        pass
    else:
        i = i + 1
        paramname, paramval = item.partition("=")[::2]
        argsDict[paramname] = paramval

try:
    helpReq = argsDict['--help']
    print ("")
    print ("Usage: {} --cache=/path/to/cache --dest=/path/to/destination --lang=en-US --voice=\"ZiraUS\" --fileformat=riff-8khz-8bit-mono-mulaw --apikey=YOUR-API-KEY --text=\"Hello World\"".format(sys.argv[0]))
    print ("")
    print ("--cache         : Location of file cache. Useful if you repeatedly request")
    print ("                      the same text to speech and wish to conserve bandwidth")
    print ("                      and reduce Azure costs. Must be writeable.")
    print ("--dest          : Location for the output file. Must be writeable.")
    print ("--lang          : Language to be spoken. Case sensitive.")
    print ("--voice         : Voice to be used. Case sensitive.")
    print ("--fileformat    : Format of the output file.")
    print ("--apikey        : API key generated by Azure.")
    print ("--text          : Text to convert to speech. MUST be enclosed in double quotes.")
    print ("")
    print ("Available language combinations (--lang --voice):")
    for item, value in namemap.items():
        for voiceval in value:
            print ("Language: {}   Voice: {}".format(item,voiceval))
    print ("")
    print ("Available file formats:")
    for item, value in formatmap.items():
        print (item)
    sys.exit(1)
except:
    pass
    
    

try:
    destLoc = argsDict['--dest']
except:
    print ("")
    print ("Error: destination location not specified.")
    print ("")
    print ("Usage: {} --cache=/path/to/cache --dest=/path/to/destination --lang=en-US --voice=\"ZiraUS\" --fileformat=riff-8khz-8bit-mono-mulaw --apikey=YOUR-API-KEY --text=\"Hello World\"".format(sys.argv[0]))
    print ("")
    sys.exit(1)

try:
    ttsLang = argsDict['--lang']
except:
    print ("")
    print ("Error: language not specified.")
    print ("")
    print ("Usage: {} --cache=/path/to/cache --dest=/path/to/destination --lang=en-US --voice=\"ZiraUS\" --fileformat=riff-8khz-8bit-mono-mulaw --apikey=YOUR-API-KEY --text=\"Hello World\"".format(sys.argv[0]))
    print ("")
    sys.exit(1)
    
try:
    ttsVoice = argsDict['--voice']
except:
    print ("")
    print ("Error: voice not specified.")
    print ("")
    print ("Usage: {} --cache=/path/to/cache --dest=/path/to/destination --lang=en-US --voice=\"ZiraUS\" --fileformat=riff-8khz-8bit-mono-mulaw --apikey=YOUR-API-KEY --text=\"Hello World\"".format(sys.argv[0]))
    print ("")
    sys.exit(1)

try:
    ttsFormat = argsDict['--fileformat']
except:
    print ("")
    print ("Error: file format not specified.")
    print ("")
    print ("Usage: {} --cache=/path/to/cache --dest=/path/to/destination --lang=en-US --voice=\"ZiraUS\" --fileformat=riff-8khz-8bit-mono-mulaw --apikey=YOUR-API-KEY --text=\"Hello World\"".format(sys.argv[0]))
    print ("")
    sys.exit(1)
    
try:
    ttsText = argsDict['--text']
except:
    print ("")
    print ("Error: text not specified.")
    print ("")
    print ("Usage: {} --cache=/path/to/cache --dest=/path/to/destination --lang=en-US --voice=\"ZiraUS\" --fileformat=riff-8khz-8bit-mono-mulaw --apikey=YOUR-API-KEY --text=\"Hello World\"".format(sys.argv[0]))
    print ("")
    sys.exit(1)

try:
    ttsApiKey = argsDict['--apikey']
except:
    print ("")
    print ("Error: API key not specified.")
    print ("")
    print ("Usage: {} --cache=/path/to/cache --dest=/path/to/destination --lang=en-US --voice=\"ZiraUS\" --fileformat=riff-8khz-8bit-mono-mulaw --apikey=YOUR-API-KEY --text=\"Hello World\"".format(sys.argv[0]))
    print ("")
    sys.exit(1)    

try:
    ttsCache = argsDict['--cache']
except:
    ttsCache = None

if ttsVoice not in namemap[ttsLang]:
    print ("")
    print ("Error: invalid language or Voice specified, or invalid combination: The following language/Voice combinations are available:")
    print ("")
    for item, value in namemap.items():
        for voiceval in value:
            print ("Language: {}".format(item))
            print ("Language: {}   Voice: {}".format(item, voiceval))
    sys.exit(1)
    
try:
    formatname = formatmap[ttsFormat]
except:
    print ("")
    print ("Error: invalid format specified: The following formats are available:")
    print ("")
    for item, value in formatmap.items():
        print (item)
    sys.exit(1)
    
if ttsCache:
    cacheaccess = os.access(ttsCache, os.W_OK)
    if not cacheaccess:
        print ("Cannot write to cache location, ignoring --cache setting...")
        ttsCache = None

m = hashlib.md5()
# Hash lang+Voice+text
m.update(("{}-{}-{}".format(ttsLang, ttsVoice, ttsText)).encode('utf-8'))
# create filename base on MD5 hash
filename = "{}.wav".format(m.hexdigest())
if ttsCache:
    # If our file already exists, just return it so we don't have to do an API call...
    if os.path.isfile(os.path.join(ttsCache, filename)):
        try:
            shutil.copy2(os.path.join(ttsCache, filename), destLoc)
            sys.exit(0)
        except (Exception) as e:
            print ("Could not copy cached file: {}".format(e))
            print ("Exiting...")
            sys.exit(1)

# Wait to import this until after we check cache to keep things as speedy as possible...
from bingtts import Translator
translator = Translator(ttsApiKey)
try:
    data = translator.speak(ttsText, ttsLang, ttsVoice, ttsFormat)
except (Exception) as e:
    print ("Error retrieving speech file: {}".format(e))
    sys.exit(1)

if ttsCache:
    try:
        with open(destLoc, 'w') as f:
            f.write(data)
    except (Exception) as e:
        print ("Couldn't write to file {}: {}".format(destLoc, e))
        sys.exit(1)
    try:
        with open(os.path.join(ttsCache, filename), 'w') as f:
            f.write(data)
    except (Exception) as e:
        cacheFileLoc = os.path.join(ttsCache, filename)
        print ("Couldn't write to file {}: {}".format(cacheFileLoc, e))
        sys.exit(1)
else:
    try:
        with open(destLoc, 'w') as f:
            f.write(data)
    except (Exception) as e:
        print ("Couldn't write to file {}: {}".format(destLoc, e))
        sys.exit(1)
        
sys.exit(0)
