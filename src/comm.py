import urllib2

def sendToHost(comm):
    ip = "192.168.0.106:8080"

    url = "http://" + ip + "/" + comm

    #print url
    urllib2.urlopen(url)