import requests

text = ''

data = {"apikey":"fe224304a5e5ff8ed263551e6138a1eeb0ec8b4d",
        "outputMode":"json",
        "url":"http://localhost/feedback.txt",
        "showSourceText":1
        }
r = requests.post("https://gateway-a.watsonplatform.net/calls/url/URLGetTextSentiment",data=data)

print str(r.status_code) + " " + r.reason
print r.text
