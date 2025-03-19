import logging
from patchright.sync_api import sync_playwright
from utils import login, total_pages, extract_links, save_links_to_file, post_body, scrape_all_links

from time import sleep
from random import randint
from analyze import analyze_post

logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

def main():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                channel='chrome',
                headless=False,
                slow_mo=100,
                args=[
                    '--disable-blink-features=AutomationControlled',
                ]
            )
            page = browser.new_page()
            login(page=page)
            
            while True:
                print("Menu:")
                print("1. Scrape all posts links")
                print("2. Analyze all posts")
                print("3. Analyze a specific post")
                print("4. Auto Mode (Clouflare captcha can appear. Sit in front of PC!)")
                print("5. Exit")
                choice = input("Enter your choice: ")
                
                if choice == '1':
                    scrape_all_links(page)
                    print("DONE! Check links.txt file.")

                elif choice == '2':
                    with open('links.txt', 'r') as f:
                        links = f.readlines()
                    for link in links:
                        post_text = post_body(page, link)
                        post_analysis = analyze_post(post_text=post_text)
                        print("Analysis Result:")
                        print(post_analysis)
                        with open('post_analysis.txt', 'w') as f:
                            f.write(post_analysis)
                        sleep(randint(1, 5))
                    print("DONE! Check post.txt file.")

                elif choice == '3':
                    link = input("Enter the post link: ")
                    if not link.startswith("https://"):
                        link = "https://" + link
                    post_text = post_body(page, link)
                    post_analysis = analyze_post(post_text=post_text)
                    print("Analysis Result:")
                    print(post_analysis)
                    with open('post_analysis.txt', 'w') as f:
                        f.write(post_analysis)
                    print("DONE! Check post_analysis.txt file for results")

                elif choice == '4':
                    scrape_all_links(page)
                    with open('links.txt', 'r') as f:
                        links = f.readlines()
                    for link in links:
                        post_text = post_body(page, link)
                        post_analysis = analyze_post(post_text=post_text)
                        print("Analysis Result:")
                        print(post_analysis)
                        with open('post_analysis.txt', 'w') as f:
                            f.write(post_analysis)
                        sleep(randint(1, 5))
                    print("DONE! Check post.txt file.")
                elif choice == '5':
                    break
                else:
                    print("Invalid choice. Please try again.")
            browser.close()
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        logging.info("Exiting...")

if __name__ == "__main__":
    main()
