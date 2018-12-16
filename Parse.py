from bs4 import BeautifulSoup


def parse_class(document):
    soup = BeautifulSoup(document, features="html.parser")
    h1: str = soup.find("h1").contents[0]
    h2 = filter_nonprintable(soup.find("h2").contents[0]).split()
    caption = soup.find("caption").contents[0].split()
    table_row = soup.find_all("tr")
    table_row.pop(0)

    class_name = h1
    lecturer_name = h2[0] + " " + h2[1]
    quarter = h2[-1]
    surveyed = int(float(caption[-4].replace('"', '')))
    enrolled = int(float(caption[-2].replace('"', '')))
    statistics = {}

    for tr in table_row:
        contents = tr.contents
        lst = []
        for content in contents:
            lst.append(content.text.strip().replace(':', ''))

        statistics[lst.pop(0)] = lst

    class_result = {"class": class_name.strip(),
                    "lecturer": lecturer_name.strip(),
                    "quarter": quarter.strip(),
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
