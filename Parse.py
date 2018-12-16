from bs4 import BeautifulSoup


def parse_class(document):
    soup = BeautifulSoup(document, features="html.parser")
    h1: str = soup.find("h1").contents[0].strip()
    h2 = filter_nonprintable(soup.find("h2").contents[0]).split()
    caption = soup.find("caption").contents[0].split()
    table_row = soup.find_all("tr")
    table_row.pop(0)

    class_name = h1
    lecturer_name = h2[0] + " " + h2[1]
    quarter = h2[-1]
    surveyed = caption[-4]
    enrolled = caption[-2]
    statistics = {}

    for tr in table_row:
        # BeautifulSoup(tr, features="html.parser")
        contents = tr.contents
        lst = []
        for content in contents:
            lst.append(content.text)

        statistics[lst.pop(0)] = lst

    class_result = {"class": class_name,
                    "lecturer": lecturer_name,
                    "quarter": quarter,
                    "surveyed": surveyed,
                    "enrolled": enrolled,
                    "statistics": statistics}
    print(class_result)
    return class_result


def parse_toc(text):
    TOC_STUB = "https://www.washington.edu/cec/"

    soup = BeautifulSoup(text, features="html.parser")
    result = []
    hrefs = soup.find_all('a', href=True)

    for href in hrefs:
        result.append(TOC_STUB + href['href'])

    # Useless links on each end
    FRONT = 9
    REAR = -3

    return result[FRONT:REAR]


def filter_nonprintable(text):
    import string
    # Get the difference of all ASCII characters from the set of printable characters
    nonprintable = set([chr(i) for i in range(128)]).difference(string.printable)
    # Use translate to remove all non-printable characters
    return text.translate({ord(character): None for character in nonprintable})
