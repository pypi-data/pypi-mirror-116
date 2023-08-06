def start():
    from bs4 import BeautifulSoup

    import requests

    # %%
    url = "https://www.poetryfoundation.org/"


    # %%
    page = requests.get(url)


    # %%
    soup = BeautifulSoup(page.content, 'lxml')


    # %%
    temp_list = soup.find_all('div', 'c-feature-hd')


    # %%
    main_dict = {}


    # %%
    main_dict['mainEssay'] = {'title':temp_list[0].h2.a.text,     'URL':temp_list[0].h2.a['href']} 


    # %%
    main_dict['poemOfTheDay'] = {'title' : temp_list[1].h2.a.text,     'URL' : temp_list[1].h2.a['href']}


    # %%
    main_dict['essay'] = {'title': temp_list[2].h2.a.text,     'URL':temp_list[2].h2.a['href']}


    # %%
    switcher_dict = {
        1 : 'mainEssay',
        2 : 'poemOfTheDay',
        3 : 'essay'
    }


    # %%
    def fetchPOTD(title, URL):
        print("Fetching {} from {} ....".format(title, URL))
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'lxml')
        content_lines = soup.find_all('div', 'c-feature-bd')[0].div.find_all('div')
        author = soup.find('span', 'c-txt c-txt_attribution').a.text
        print("\n\n\n", title, sep='')
        print("By", author)
        print()
        for i in content_lines:
            print(i.text)


    # %%
    def fetchMainEssay(title, URL):
        print("Fetching {} from {} ....".format(title, URL))
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'lxml')
        tag_set = soup.find_all('div', 'c-userContent')
        author = soup.find('span', 'c-txt c-txt_attribution').a.text
        content_lines = tag_set[0].find_all('p')
        print("\n\n\n", title, sep='')
        print("By", author)
        print()
        for i in content_lines:
            print(i.text)


    # %%
    def fetchEssay(title, URL):
        print("Fetching {} from {} ....".format(title, URL))
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'lxml')
        tag_set = soup.find_all('div', 'c-userContent')
        content_lines = tag_set[0].find_all('p')
        author = soup.find('span', 'c-txt c-txt_attribution').a.text
        print("\n\n\n", title, sep='')
        print("By", author)
        print()
        for i in content_lines:
            print(i.text)


    # %%
    #choice
    print("\nChoices:\n\n1. Main Essay\n2. Poem Of The Day\n3. Secondary Essay\n\nEnter your choice (1-3) : ", end='')
    choice = int(input())
    target_title = main_dict[switcher_dict[choice]]['title']
    target_URL = main_dict[switcher_dict[choice]]['URL']
    if choice == 1:
        fetchMainEssay(target_title, target_URL)
    elif choice == 2:
        fetchPOTD(target_title, target_URL)
    elif choice == 3:
        fetchEssay(target_title, target_URL)
    else:
        print("Have a valid choice, please! :(\n")
