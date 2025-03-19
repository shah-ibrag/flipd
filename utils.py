import logging
from time import sleep
from random import randint
from config_reader import login_credentials

logging.basicConfig(level=logging.INFO)

def login(page):
    username, password = login_credentials()

    page.goto('https://oguser.com/login')
    page.wait_for_selector('xpath=//html/body/div[4]/div/form[1]/div[2]/div[1]/div/div[2]/div/span/button')
    
    username_input = page.query_selector('input[placeholder="Username/Email"]')
    password_input = page.query_selector('input[placeholder="Password"]')
    login_button = page.query_selector('xpath=//html/body/div[4]/div/form[1]/div[2]/div[1]/div/div[2]/div/span/button')
    
    sleep(1)
    username_input.type(username)
    sleep(1)
    password_input.type(password)
    login_button.click()

def total_pages(page):
    last_page = '//a[@class="pagination_last"]'
    page.goto('https://oguser.com/Forum-OG-Instagram-Usernames')
    page.wait_for_selector('xpath=' + last_page)
    total_pages = page.query_selector('xpath=' + last_page).inner_text()
    return int(total_pages)

def extract_links(page, tbody_xpath):
    page.wait_for_selector('xpath=' + tbody_xpath)
    tr_elements = page.query_selector_all('xpath=' + tbody_xpath + '/tr')
    tr_count = len(tr_elements)
    logging.info(f"Number of <tr> elements: {tr_count}")
    
    links = []
    for i in range(1, tr_count + 1):
        link_xpath = f'{tbody_xpath}/tr[{i}]/td[1]/div[1]/span[1]/span[2]/a'
        link_element = page.query_selector('xpath=' + link_xpath)
        if link_element is not None:
            href = link_element.get_attribute('href')
            links.append(href)
    return links

def save_links_to_file(links, filename):
    with open(filename, 'a') as f:
        for link in links:
            f.write("https://oguser.com/" + link + '\n')

def post_body(page, link):
    page.goto(link)
    post_body_xpath = '//div[@class="post_body scaleimages"]'
    page.wait_for_selector('xpath=' + post_body_xpath)
    post_body = page.query_selector('xpath=' + post_body_xpath).inner_text()
    return post_body

def scrape_all_links(page):
    page_number = 1
    total_pages_count = total_pages(page)
    for page_number in range(1, total_pages_count + 1):
        page.goto(f'https://oguser.com/Forum-OG-Instagram-Usernames?page={page_number}')
        links = extract_links(page, '//*[@id="noa-transition"]/table/tbody')
        save_links_to_file(links, 'links.txt')
        sleep(randint(1, 5))