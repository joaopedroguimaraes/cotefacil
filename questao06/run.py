from main import scrape

if __name__ == '__main__':
    author_to_scrape = "J.K. Rowling"
    scraped_result = scrape(author_to_scrape)
    scraped_result_json = "{}"
    if scraped_result is not None:
        scraped_result_json = scraped_result.toJSON()
    with open("output.json", "w") as file:
        file.write(scraped_result_json)
    print(scraped_result_json)
