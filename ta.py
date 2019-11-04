# https://www.tripadvisor.it/Restaurants-g187791-Rome_Lazio.html

# import BeautifulSoap library
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# import requests lib to make possibile http requests
import requests

from time import sleep

# URL base of trip advisor
URLBASE = "https://www.tripadvisor.it"

# Url of the roman restaurants
URL = "/Restaurants-g187791-Rome_Lazio.html"

# Create instance of firefox webdriver
driver = webdriver.Firefox()


# Get a restaurant property
def get_single_restaurant_prop(soap, container_dom, container_class, child_dom, child_class):
    # Find the prop wrapper
    if soap.find(container_dom, {"class": container_class}):
        container = soap.find(container_dom, {"class": container_class})
        # Find the property
        if container.find(child_dom, {"class": child_class}):
            return container.find(child_dom, {"class": child_class}).text
    return "N/A"


# Get the list of reviews
def get_single_restaurant_reviews(soap):
    reviews = soap.find_all("p", {"class": "partial_entry"})

    for review in reviews:
        print("- " + review.text + "\n")
        sleep(1)


# Get single restaurant
def get_single_restaurant(url_rest):
    # Navigate the restaurant single page
    single_restaurant_page = requests.get(URLBASE + url_rest)

    # Get the restaurant single page html
    soap = BeautifulSoup(single_restaurant_page.text, "html.parser")

    # Get restaurant properties
    name = get_single_restaurant_prop(soap, "div", "restaurantName", "h1", "h1")
    address = get_single_restaurant_prop(soap, "div", "address", "span", "detail")
    phone = get_single_restaurant_prop(soap, "div", "phone", "span", "detail")
    score = get_single_restaurant_prop(
        soap,
        "div",
        "restaurants-detail-overview-cards-RatingsOverviewCard__primaryRatingRow--VhEsu",
        "span",
        "restaurants-detail-overview-cards-RatingsOverviewCard__overallRating--nohTl")

    info = "\nNome: {}\nIndirizzo: {}\nTelefono: {}\nPunteggio: {}\n"
    print(info.format(name, address, phone, score))

    driver.get(URLBASE + url_rest)

    # Get the more button
    more = driver.find_elements_by_css_selector(".partial_entry span.taLnk")

    if len(more) != 0:
        more[0].click()
    get_single_restaurant_reviews(soap)

    pass


# Infinite loop
while True:
    # Request the roman restaurant html page
    page = requests.get(URLBASE + URL)

    # Parse the html page
    soup = BeautifulSoup(page.text, "html.parser")

    # Find all restaurants based on a class and save them in an array
    archive_restaurant_class = "restaurants-list-ListCell__cellContainer--2mpJS"
    restaurants = soup.find_all("div", {"class": archive_restaurant_class})

    # For every restaurant in the list till there is one
    for restaurant in restaurants:
        # Get the restaurant url based on a class attached to an a tag
        single_restaurant_class = "restaurants-list-ListCell__restaurantName--2aSdo"
        single_restaurant_url = restaurant.find("a", {"class": single_restaurant_class})

        # This should get information about the single restaurant
        get_single_restaurant(single_restaurant_url.attrs['href'])

    # Find the next button to have the link for next list of restaurant
    next_page = soup.find("a", {"class": "next"})

    URL = next_page.attrs['href']

    # Sleep to avoid too much requests and be banned from server
    sleep(2)
