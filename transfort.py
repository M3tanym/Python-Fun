# might need to install these, probably ...$ pip install xmltodict requests
import xmltodict
import requests

def getETA(stop, route):
    '''return a nice string with info about buses arriving at this stop'''
    # found this URL with a little poking around http://ridetransfort.com/bustracker
    url = 'http://clever-web.fcgov.com/bustime/map/getStopPredictions.jsp?stop={}&route={}'.format(stop, route)
    r = requests.get(url)
    xml = xmltodict.parse(r.content)
    ret = ''
    name = xml['stop']['nm']

    if name == None:
        ret = "Stop {} doesn't exist.".format(stop)
    elif 'pre' not in xml['stop']:
        ret = 'Route {} not arriving at stop {} ({}) anytime soon.'.format(route, stop, name)
    else:
        time = xml['stop']['pre']['pt'].split(' ')[0]
        bus = xml['stop']['pre']['v']
        ret = 'Route {} (bus {}) arriving at stop {} ({}) in {} minutes.'.format(route, bus, stop, name, time)

    return ret

# Next, it would be cool to get geolocation info too
# http://clever-web.fcgov.com/bustime/map/getBusesForRoute.jsp?route=2 is a good starting place

if __name__ == '__main__':
    # examples
    print(getETA(237, 2))
    print(getETA(237, 3))
