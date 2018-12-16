import Page
import Creds
import Parse
import json
import pathlib

if __name__ == '__main__':
    link_path = "/tmp/all_links.txt"
    json_path = "/tmp/all_json.json"

    user = Page.Page(Creds.username, Creds.password)
    # user.get_toc_all_and_write(link_path)

    results = []

    p = pathlib.Path(link_path)
    urls = p.read_text().splitlines()

    counter = 0
    for url in urls:
        counter += 1
        user.login(url)
        page = user.get_page(url)
        results.append(Parse.parse_class(page))
        if counter > 3:
            break

    with open(json_path, "w+") as outfile:
        json.dump(results, outfile)
