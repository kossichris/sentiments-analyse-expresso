

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# --- CONFIGURATION ---
PAGE_URL = "https://www.facebook.com/Expresso221"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2})
driver = webdriver.Chrome(options=chrome_options)

# --- LOGIN ---
driver.get("https://www.facebook.com/")
print("Veuillez vous connecter manuellement dans la fenêtre ouverte.")
input("Appuyez sur Entrée ici une fois connecté...")

def get_post_links(page_url, max_posts=10):
    """Scrape post links from the Facebook classic page (Posts tab)."""
    post_links = set()
    driver.get(page_url)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    # Find post links: look for <a> tags with href containing '/posts/' or '/permalink/' or '?story_fbid='
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if ("/posts/" in href or "/permalink/" in href or "?story_fbid=" in href) and "Expresso221" in href:
            # Make absolute URL if needed
            if href.startswith("https://"):
                post_links.add(href)
            else:
                post_links.add("https://www.facebook.com" + href)
        if len(post_links) >= max_posts:
            break
    return list(post_links)

def get_comments_from_post(post_url):
    """Scrape comments from a Facebook post (classic version)."""
    names = []
    comments = []
    driver.get(post_url)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    # Facebook classic: comments are in <div> with aria-label containing 'Comment by'
    for comment_div in soup.find_all("div", attrs={"aria-label": lambda x: x and "Comment by" in x}):
        # Get author name
        name_tag = comment_div.find("a")
        # Get comment text
        comment_body = comment_div.find("div", attrs={"dir": "auto"})
        if name_tag and comment_body:
            names.append(name_tag.text.strip())
            comments.append(comment_body.text.strip())
    return names, comments

all_names = []
all_comments = []
all_posts = []


print("Scraping post links...")
post_links = get_post_links(PAGE_URL, max_posts=10)
print(f"Trouvé {len(post_links)} posts.")

for idx, post_url in enumerate(post_links):
    print(f"Scraping post {idx+1}/{len(post_links)}: {post_url}")
    names, comments = get_comments_from_post(post_url)
    all_names.extend(names)
    all_comments.extend(comments)
    all_posts.extend([post_url]*len(names))
    print(f"  {len(names)} commentaires trouvés.")
    time.sleep(5)  # pause entre posts

# --- SAVE DATA ---
data = pd.DataFrame({"Post": all_posts, "Name": all_names, "Comment": all_comments})
data.to_csv("data/facebook_comments.csv", index=False, encoding="utf-8-sig")
print("✅ Données enregistrées dans data/facebook_comments.csv")
