import json
import sys

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class Author:
    def __init__(self, name, birth_date, birth_location, description):
        self.name = name
        self.birth_date = birth_date
        self.birth_location = birth_location
        self.description = description
        self.quotes = []

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=False, indent=4)


class Quote:
    def __init__(self, text, tags):
        self.text = text
        self.tags = tags

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=False, indent=4)


def scrape_quote_text_and_tags(driver_quote_element):
    found_quote_text = driver_quote_element.find_element(
        By.CLASS_NAME, 'text').text.strip()\
        .encode("ascii", "ignore").decode('utf-8')
    found_quote_tags = [element_tag.text.strip()
                        for element_tag in
                        driver_quote_element.find_elements(
                            By.CLASS_NAME, 'tag')]
    return Quote(found_quote_text, found_quote_tags)


def scrape_about_page_to_author(driver):
    name = driver.find_element(
        By.CLASS_NAME, 'author-title').text.strip()
    birth_date = driver.find_element(
        By.CLASS_NAME, 'author-born-date').text.strip()
    birth_location = driver.find_element(
        By.CLASS_NAME, 'author-born-location').text.strip()
    description = driver.find_element(
        By.CLASS_NAME, 'author-description').text.strip()\
        .encode("ascii", "ignore").decode('utf-8')
    return Author(name, birth_date, birth_location, description)


def scrape(author_to_search):
    driver = webdriver.Firefox()
    author = None

    # Com 2 loops é possível evitar que sempre haja uma verificação
    # do about mesmo que já tenha sido obtido

    # Primeiro loop: pegar as informações por autor
    driver.get("http://quotes.toscrape.com/")

    # pra que o próximo loop já saiba por qual página começar a busca
    number_page_found = 0
    found = False

    while 'No quotes found!' not in driver.page_source:
        number_page_found += 1
        try:
            found_quotes = driver.find_elements(
                By.CLASS_NAME, 'quote')
            for found_quote in found_quotes:
                found_author = found_quote.find_elements(
                    By.TAG_NAME, 'span')[1]
                found_author_name = found_author.find_element(
                    By.CLASS_NAME, 'author').text
                if found_author_name == author_to_search:
                    about_element = found_author.find_element(
                        By.TAG_NAME, 'a')
                    about_element.click()

                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located(
                            (By.CLASS_NAME, "author-title"))
                    )
                    author = scrape_about_page_to_author(driver)
                    found = True
                    break

        except Exception as e:
            print(e)

        try:
            driver.find_element(
                By.XPATH, '//nav/ul/li[@class="next"]/a').click()
        except NoSuchElementException:
            # Acabou o scrape
            break

    if found:  # Achou pelo menos uma frase

        # Vai pra primeira página de frases que contenha uma frase do
        # autor pesquisado
        driver.get(f"http://quotes.toscrape.com/page/"
                   f"{number_page_found}/")

        # Segundo loop: scrape das quotes de acordo com o nome do
        # autor passado por parâmetro

        while 'No quotes found!' not in driver.page_source:
            try:
                found_quotes = driver.find_elements(
                    By.CLASS_NAME, 'quote')
                for found_quote in found_quotes:
                    found_author = found_quote.find_elements(
                        By.TAG_NAME, 'span')[1]
                    found_author_name = found_author.find_element(
                        By.CLASS_NAME, 'author').text
                    if found_author_name == author_to_search:
                        author.quotes.append(
                            scrape_quote_text_and_tags(found_quote))

                driver.find_element(
                    By.XPATH, '//nav/ul/li[@class="next"]/a').click()
            except Exception as e:
                print(e)
            try:
                driver.find_element(
                    By.XPATH, '//nav/ul/li[@class="next"]/a').click()
            except NoSuchElementException:
                # Acabou o scrape
                break

    driver.close()
    return author


if __name__ == '__main__':
    author_to_scrape = sys.argv[1:][0]
    scraped_result = scrape(author_to_scrape)
    scraped_result_json = "{}"
    if scraped_result is not None:
        scraped_result_json = scraped_result.toJSON()
    with open("output.json", "w") as file:
        file.write(scraped_result_json)
    print(scraped_result_json)
