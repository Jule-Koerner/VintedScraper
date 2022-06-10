
def sizeFilter(url):
    driver.get(url)
    html = driver.page_source

    piece = BeautifulSoup(html, "html.parser")
    #print("piece", piece)
    size = piece.find_all("div", {'class': "details-list__item-value"})
    print("SIZE", size)
    return size


print(links[10])

sizeFilter(links[10])