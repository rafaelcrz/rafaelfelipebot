import urllib.request
import json
#from urllib.request import urlopen


# Get repositories from Github
class Repositorie:

    def getRepositories(self):
        response = urllib.request.urlopen(
            "https://api.github.com/search/repositories?q=user:rafaelcrz&sort:stars").read().decode('utf8')
        obj = json.loads(response)
        repository = obj['items']
        return repository
