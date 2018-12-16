from bs4 import BeautifulSoup
import requests
import Parse


def pretty_print_post(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in
    this function because it is programmed to be pretty
    printed and may differ from the actual request.
    """
    print('{}\n{}\n{}\n\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))
    print('-----------END-----------')


def get_hidden_fields(text):
    soup = BeautifulSoup(text, features="html.parser")
    tags = soup.find_all("input", type="hidden")

    hidden = {}
    for tag in tags:
        hidden[tag.attrs["name"]] = tag.attrs["value"]

    return hidden


class Page:

    username: str
    password: str

    pubcookie_g: str
    pubcookie_g_req: {str: str}
    pubcookie_l = {"pubcookie_l": ""}
    first_kiss = {str: str}

    WEBLOGIN = "https://weblogin.washington.edu/"

    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.pubcookie_g_req = {}
        self.pubcookie_g = ""
        self.first_kiss = {}

    def __str__(self):
        return \
            "username: " + self.username + "\n" + \
            "password: " + self.password + "\n" + \
            "pubcookie_g: " + self.pubcookie_g + "\n" + \
            "pubcookie_g_req:" + self.pubcookie_g_req.__str__() + "\n" \
            "pubcookie_l: " + self.pubcookie_l.__str__() + "\n" + \
            "self.first_kiss: " + self.first_kiss.__str__()

    """
    Authentication
    """
    def request_first_kiss(self):
        r = requests.get(self.WEBLOGIN)
        first_kiss = get_hidden_fields(r.text)
        first_kiss["user"] = self.username
        first_kiss["pass"] = self.password

        self.first_kiss = first_kiss

    def request_pubcookie_l(self):
        r = requests.post(self.WEBLOGIN, self.first_kiss)
        self.pubcookie_l["pubcookie_l"] = r.headers['Set-Cookie'].split(";")[0].split("=")[1]

    def request_pubcookie_g_req(self, url):
        r = requests.get(url)
        self.pubcookie_g_req = get_hidden_fields(r.text)

    def request_pubcookie_g(self, url):
        # Phase 1
        headers = {"Connection": "close",
                   "Origin": "https://www.washington.edu",
                   "Referer": url}

        r = requests.post(self.WEBLOGIN, cookies=self.pubcookie_l, data=self.pubcookie_g_req, headers=headers)
        first_kiss = get_hidden_fields(r.text)
        first_kiss["user"] = self.username
        first_kiss["pass"] = self.password

        # Phase 2
        headers = {"Connection": "close",
                   "Origin": self.WEBLOGIN,
                   "Referer": self.WEBLOGIN}
        r = requests.post(self.WEBLOGIN, headers=headers, data=first_kiss)
        pubcookie_g = get_hidden_fields(r.text)

        # Get pubcookie_g
        self.pubcookie_g = "pubcookie_g=" + pubcookie_g["pubcookie_g"]
        # Get pubcookie_l
        self.pubcookie_l["pubcookie_l"] = r.headers['Set-Cookie'].split(";")[0].split("=")[1]

    def login(self, target):
        self.request_first_kiss()
        self.request_pubcookie_l()
        self.request_pubcookie_g_req(target)
        self.request_pubcookie_g(target)

    """
    Retrieval
    """
    def get_page(self, url):
        headers = {"Cookie": self.pubcookie_g,
                   "Referer": "https://weblogin.washington.edu/"}
        r = requests.get(url, headers=headers)

        return r.text

    def get_toc_letter(self):
        toc_url = "https://www.washington.edu/cec/toc.html"
        self.login(toc_url)
        return Parse.parse_toc(self.get_page(toc_url))

    def get_toc_links(self, url):
        self.login(url)
        return Parse.parse_toc(self.get_page(url))

    def get_toc_all_and_write(self, path):
        # all_links = []

        with open(path, 'w+') as f:
            letters = self.get_toc_letter()
            for letter in letters:
                links = self.get_toc_links(letter)
                for link in links:
                    print(link)
                    f.write(link+"\n")

        print("all done")
