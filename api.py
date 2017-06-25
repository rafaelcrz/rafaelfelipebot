import urllib.request
import json
from unittest.test.test_result import __init__


# Get repositories from Github
class Repositorie:
    def getRepositories(self):
        with urllib.request.urlopen(
                "https://api.github.com/search/repositories?q=user:rafaelcrz&sort:stars") as item:
            data = json.load(item)
            repository = data['items']
        return repository  # name - html_url
