import json


def unit2time():
    with open(f'assets/song/notes.json','r') as f:
        chartContent = json.load(f)

    chartList = [{}, {}, {}, {}]


    for track in range(4):
        for chartIdx in chartContent['chartFrameIds'][track]:
            chartList[track][chartIdx['unitId']/200] = chartIdx['tailLengthUnitId']

        chartList[track] = resortDict(chartList[track])


    return chartList
def resortDict(dict):
    output = {}
    sortKeys = sorted(dict,reverse=False)
    for i in sortKeys:
        output[i] = dict[i]
    return output


# print(unit2time('raining'))

def getChartAttr(name):
    with open(f'assets/song/notes.json','r') as f:
        chartContent = json.load(f)

    return chartContent

