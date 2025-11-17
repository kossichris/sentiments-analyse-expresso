from facebook_scraper import get_posts
import pandas as pd
from tqdm import tqdm

def scrape_facebook_page(page_name="expresso.sn", pages=3, output_file="data/facebook_expresso.csv"):
    """
    Scrape les posts publics d'une page Facebook (ex: Expresso Sénégal)
    et enregistre les résultats dans un fichier CSV.
    """

    print(f"📘 Scraping de la page Facebook : {page_name}")
    data = []

    for post in tqdm(
        get_posts(page_name, pages=pages, options={"comments": True, "reactions": True}),
        desc="Récupération des posts"
    ):
        data.append({
            "platform": "facebook",
            "brand": "Expresso",
            "post_id": post.get("post_id"),
            "post_url": post.get("post_url"),
            "post_date": post.get("time"),
            "content": post.get("text"),
            "like_count": post.get("likes"),
            "comment_count": len(post.get("comments_full", [])),
            "share_count": post.get("shares"),
            "reactions_json": post.get("reactions")
        })

    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False, encoding="utf-8-sig")
    print(f"✅ Scraping terminé — {len(df)} posts enregistrés dans {output_file}")

if __name__ == "__main__":
    # Si le nom de la page est différent, on l’ajustera ici
    scrape_facebook_page(page_name="expresso.sn", pages=3)

