import wikipedia

def get_random_wikipedia_page_with_image():

    wikipedia.set_lang("en")
    random_title = wikipedia.random()
    page = wikipedia.page(random_title)

    while len(page.images) == 0:
        random_title = wikipedia.random()
        print("Random title:", random_title)
        page = wikipedia.page(random_title)

    return page


page = get_random_wikipedia_page_with_image()

title = page.title
summary = page.summary
content = page.content.strip()
image = page.images[0]
