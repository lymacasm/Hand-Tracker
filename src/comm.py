import urllib2

def sendToHost(comm):
    try:
        ip = "192.168.0.105:8080"

        url = "http://" + ip + "/" + comm

        #print url
        urllib2.urlopen(url)

    except urllib2.URLError:
        print "Failed to send data to host"
