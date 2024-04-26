#
import json

with open('./sets.json','r') as f:
    setDatas = json.load(f)

keys = setDatas['keys']
autoPlay = setDatas['autoplay']

with open('./projectSettings.json','r') as f:
    currentSong = json.load(f)['currentSong']


debugMode = False

