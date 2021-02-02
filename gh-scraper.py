import requests
from bs4 import BeautifulSoup


def set_url(url, langue=None, page=None, serach=None, repo_type=None):
    new_url = url
    privios = False
    and_char = "&"

    if langue is not None:
        new_url += str("l=" + langue)
        privios = True

    if page is not None:
        if (privios):
            new_url += and_char

        new_url += str("p=" + str(page))
        privios = True

    if page is None:
        if (privios):
            new_url += and_char
        new_url += ("p=" + str(1))
        privios = True

    if serach is not None:
        if (privios):
            new_url += and_char
        new_url += str("q=" + serach)
        privios = True

    if repo_type is not None:
        if (privios):
            new_url += and_char
        new_url += str("type=" + repo_type)

    return new_url


## build and create the needed url
# url = 'https://github.com/search?'
# m_lan = "Java"
# m_page = 10
# m_qution = "arknoid"
# m_type = "Repositories"

# url = find_url(url, m_lan,m_page,m_qution,m_type)

# geting the url of all repos as deep as needed in github
def trade_spider(max_pages, repo_links):
    page = 1
    while page <= max_pages:
        # url = 'https://github.com/search?l=Java&p=' + str(page) + '&q=arknoid&type=Repositories'  ## 21 repos
        # url = 'https://github.com/search?l=C&p=' + str(page) + '&q=arknoid&type=Repositories'  ## 1 repo
        url = 'https://github.com/search?l=C%2B%2B&p=' + str(page) + '&q=arknoid&type=Repositories'  ## 4 repo

        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "lxml")
        tmp = soup.findAll("div", {'class': 'f4 text-normal'})

        for link in tmp:
            repo_full_url = str(link).split("url")[1].split("}")[0].split("\"")[2]
            repo_links.append(repo_full_url)

        if not repo_links:
            print("done scroling - now go out")
            break
        page += 1


# going over the links in item_url and finds all the directory's links
# def get_directory_list_link(item_url):
#     directory_list = []
#     source_code = requests.get(item_url)
#     plain_text = source_code.text
#     soup = BeautifulSoup(plain_text, "lxml")
#     directory_regex = soup.findAll("svg", {"aria-label": "directory"})
#
#     for url in directory_regex:
#         full_url = "https://github.com"+url
#         directory_list.append(full_url)
#
#     return directory_list


# going over the links in item_url and finds all the files's links
def get_links_in_single_repo(item_url):
    files_list = []
    source_code = requests.get(item_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "lxml")
    file_regex = soup.findAll("td", {"class": "content"})

    for i in file_regex:
        if len(str(i).split("\"")) > 6:
            file = "https://github.com/" + str(i).split("\"")[7]
            files_list.append(file)

    return files_list


def leaf(item_url):
    source_code = requests.get(item_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "lxml")
    file_regex = soup.findAll("td", {"class": "blob-num js-line-number"})
    readme_regex = soup.findAll("div", {"id": "readme"})
    if len(file_regex) != 0:
        return True
    elif len(readme_regex) != 0:
        return True
    else:
        return False


def find_leaf(single_repo_links):
    go_again = []
    for repo_page in single_repo_links:
        if not leaf(repo_page):
            go_again.append(repo_page)
        else:
            print("url = ", repo_page, " is leaf- ", leaf(repo_page))
    if len(go_again) > 0:
        return go_again


def reprt(go_again):
    if go_again != None:
        for next_link in go_again:
            single_repo_links = get_links_in_single_repo(next_link)
            go_again2 = find_leaf(single_repo_links)
            return go_again2

def main():
    repo_links = []
    deep = 3

    trade_spider(deep, repo_links)

    index = 1
    for repo_name in repo_links:
        print("index: " + str(index) + " url: " + repo_name)
        index += 1

    for repo in repo_links:
        # repo = "https://github.com/ProofOfGravity/ChiliArknoid"
        single_repo_links = get_links_in_single_repo(repo)
        go_again = find_leaf(single_repo_links)
        print("need to go over this now - ", reprt(go_again))

if __name__ == '__main__':
    main()