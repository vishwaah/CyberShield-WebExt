import re
from html.parser import HTMLParser
import requests
import json

SOCIAL_MEDIA_PATTERN = re.compile(
    r"(facebook\.com|twitter\.com|linkedin\.com|instagram\.com|youtube\.com|tiktok\.com)",
    re.IGNORECASE
)

class SocialMediaLinkFinder(HTMLParser):
    def __init__(self):
        super().__init__()
        self.social_links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr_name, attr_value in attrs:
                if attr_name == "href" and SOCIAL_MEDIA_PATTERN.search(attr_value):
                    self.social_links.append(attr_value)

def check_social_media_presence(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        parser = SocialMediaLinkFinder()
        parser.feed(response.text)

        if parser.social_links:
            return json.dumps({"score": 1.0, "details": {"links": parser.social_links}})
        else:
            return json.dumps({"score": 0.0, "details": {"message": "No social media links found"}})
    except Exception as e:
        return json.dumps({"score": 0.0, "details": {"error": str(e)}})

if __name__ == "__main__":
    import sys
    url = sys.argv[1]
    print(check_social_media_presence(url))
