# Python-Bing-TTS
Microsoft Bing Text to Speech library for Python

# Installation
To install using pip, run the following command:

    pip install git+https://github.com/westparkcom/Python-Bing-TTS.git

# Usage
The following is the usage of the library

    translator.speak(text, language, voice, fileformat)

Variable | Description | Note
--- | --- | ---
text | The text that you wish to convert to speech | 
language | The language/country you wish to hear the speech in | Case sensitive. See [Bing TTS API Reference](https://docs.microsoft.com/en-us/azure/cognitive-services/speech/api-reference-rest/bingvoiceoutput#SupLocales) for list
voice | The name of the voice to use | Case sensitive
fileformat | File format to encode the speech to | See [Bing TTS API Reference](https://docs.microsoft.com/en-us/azure/cognitive-services/speech/api-reference-rest/bingvoiceoutput#Http) for list of formats

# Example
    from bingtts import Translator
    translator = Translator('YOUR-API-KEY-HERE')
    output = translator.speak("This is a text to speech translation", "en-US", "JessaRUS", "riff-16khz-16bit-mono-pcm")
    with open("file.wav", "w") as f:
        f.write(output)
