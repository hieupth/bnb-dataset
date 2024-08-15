"""
This is scrapping a list of places from Wikipedia.
You should adapt this script according to the page you want to scrap
"""
from pathlib import Path
import tap
from selenium import webdriver
from selenium.webdriver.common.by import By
import numpy as np


class Arguments(tap.Tap):
    url: str = "https://en.wikipedia.org/wiki/List_of_the_most_common_U.S._place_names"
    output: Path = "data/cities.txt"
    xpath: str = '//table[@class="wikitable sortable jquery-tablesorter"]/tbody/tr/td/a'
    # xpath: str = '//*[@id="mw-content-text"]/div[1]/table[2]/tbody/tr/td/a'


if __name__ == "__main__":
    args = Arguments().parse_args()
    print(args)

    driver = webdriver.Firefox()
    driver.get(args.url)

    # cities = [
    #     a.text
    #     # for a in driver.find_elements_by_xpath(args.xpath)
    #     for a in driver.find_element(By.XPATH, args.xpath)
    # ]
    cities = driver.find_elements(By.CSS_SELECTOR, "td > a")
    cities = np.unique([x.accessible_name for x in cities]).tolist()
    driver.close()

    args.output.parent.mkdir(exist_ok=True, parents=True)

    with open(args.output, "w") as fid:
        fid.write("\n".join(cities))
