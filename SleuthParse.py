import sys
import urllib
import urllib2
import hashlib
import hmac
import json
import time


def signMessage(SECRET_KEY, MESSAGE):

    hashedMessage = hmac.new(SECRET_KEY, MESSAGE, hashlib.sha512).hexdigest()

    return hashedMessage


#looper eventually
def genLoop(obj, buyKey, sellKey):
    if buyKey in obj:
        yield obj[buyKey]
    if sellKey in obj:
        yield obj[sellKey]
    for sub in obj:
        if isinstance(obj[sub], list):
            for i in obj[sub]:
                for j in genLoop(i, buyKey, sellKey):
                    yield j


if __name__ == '__main__':

    sleuthConf = json.load(open('SleuthParse.conf'))
    args = json.loads(sys.argv[1])
    EXCHANGE = str(args['exchange'])
    PUBLIC_KEY = str(args['publicKey'])
    SECRET_KEY = str(args['secretKey'])
    COMMAND = str(args['command'])
    PARAMS = args['params']

    authReq = True if len(PUBLIC_KEY) else False
    apiConf = sleuthConf[EXCHANGE]

    if authReq:

        cParam = {}
        encode = {}
        headers = {}
        url = apiConf['privateURL']

        cParam['command'] = apiConf['keys'][COMMAND]
        cParam['nonce'] = str(int(time.time()))
        cParam['pubKey'] = PUBLIC_KEY
            
        for param in apiConf['urlParams']:
            encode[apiConf['keys'][param]] = cParam[param]
        if PARAMS:
            for param in PARAMS:
                encode[apiConf['keys'][param]] = PARAMS[param]
 
        encodedStr = urllib.urlencode(encode)

        cParam['signedMessage'] = signMessage(SECRET_KEY, encodedStr)

        for header in apiConf['headers']:
            headers[apiConf['keys'][header]] = cParam[header]  

        req = urllib2.Request(url, encodedStr, headers)

    else:
        encode = {}
        cParam = {}
        url = apiConf['publicURL']

        cParam['command'] = apiConf['keys'][COMMAND]

        for param in apiConf['pubURLParams']:
            encode[apiConf['keys'][param]] = cParam[param]
        if PARAMS:
            for param in PARAMS:
                encode[apiConf['keys'][param]] = PARAMS[param]

        encodedStr = urllib.urlencode(encode)
        url += "?"+encodedStr

        req = urllib2.Request(url)

    response = urllib2.urlopen(req)
    x = response.read()
    print(x)
    







