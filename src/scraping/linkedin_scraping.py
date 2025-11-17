from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import pandas as pd
from datetime import datetime

def scrape_linkedin_posts(company_url, num_posts=30, output_file="data/linkedin_posts.csv", headless=False):
    """
    Scrape les posts LinkedIn d'une page entreprise
    
    Args:
        company_url: URL de la page LinkedIn de l'entreprise (ex: https://www.linkedin.com/company/orange-senegal/)
        num_posts: Nombre de posts à récupérer
        output_file: Fichier CSV de sortie
        headless: Exécuter Chrome en mode headless (sans interface graphique)
    """
    
    print(f"🔍 Démarrage du scraping LinkedIn pour: {company_url}")
    
    # Configuration du driver Chrome
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    driver = webdriver.Chrome(options=options)
    
    try:
        # Accéder à LinkedIn pour permettre la connexion
        print("📄 Chargement de LinkedIn...")
        driver.get("https://www.linkedin.com/login")
        print("\n⏳ Veuillez vous connecter manuellement dans le navigateur qui s'est ouvert...")
        print("   Appuyez sur ENTRÉE dans ce terminal une fois connecté.\n")
        input(">>> ")
        
        # Accéder à la page de l'entreprise
        print(f"📄 Chargement de la page de l'entreprise...")
        driver.get(company_url + "posts/")
        time.sleep(3)  # Attendre le chargement initial
        
        posts_data = []
        
        # Scroll pour charger plus de posts
        print(f"📜 Scroll pour charger les posts...")
        last_height = driver.execute_script("return document.body.scrollHeight")
        scroll_attempts = 0
        max_scrolls = 10
        
        while scroll_attempts < max_scrolls and len(posts_data) < num_posts:
            # Scroll vers le bas
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            # Vérifier si de nouveaux contenus ont été chargés
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            scroll_attempts += 1
        
        # Récupérer les posts
        print(f"🔎 Extraction des posts...")
        try:
            # Chercher les posts avec différents sélecteurs possibles
            posts = driver.find_elements(By.CLASS_NAME, "feed-shared-update-v2")
            
            if not posts:
                # Essayer un autre sélecteur
                posts = driver.find_elements(By.CSS_SELECTOR, "[data-urn*='urn:li:activity']")
            
            print(f"📊 {len(posts)} posts trouvés")
            
            for idx, post in enumerate(posts[:num_posts]):
                if idx >= num_posts:
                    break
                    
                try:
                    # Extraire le texte du post
                    try:
                        text_element = post.find_element(By.CLASS_NAME, "feed-shared-text")
                        texte = text_element.text
                    except NoSuchElementException:
                        try:
                            text_element = post.find_element(By.CSS_SELECTOR, ".update-components-text")
                            texte = text_element.text
                        except NoSuchElementException:
                            texte = post.text
                    
                    # Extraire la date (si disponible)
                    try:
                        date_element = post.find_element(By.CSS_SELECTOR, "span.update-components-actor__sub-description")
                        post_date = date_element.text
                    except NoSuchElementException:
                        post_date = datetime.now().strftime("%Y-%m-%d")
                    
                    # Extraire les réactions (likes, etc.)
                    try:
                        reactions_element = post.find_element(By.CSS_SELECTOR, ".social-details-social-counts__reactions-count")
                        reactions = reactions_element.text
                    except NoSuchElementException:
                        reactions = "0"
                    
                    # Extraire les commentaires
                    try:
                        comments_element = post.find_element(By.CSS_SELECTOR, ".social-details-social-counts__comments")
                        comments = comments_element.text
                    except NoSuchElementException:
                        comments = "0"
                    
                    if texte and len(texte.strip()) > 10:  # Ignorer les posts vides ou trop courts
                        posts_data.append({
                            "platform": "linkedin",
                            "brand": "Expresso",  # À adapter selon l'entreprise
                            "post_id": f"linkedin_post_{idx+1}",
                            "post_url": company_url,
                            "post_date": post_date,
                            "content": texte.strip(),
                            "like_count": reactions,
                            "comment_count": comments,
                            "share_count": None,
                            "reactions_json": None
                        })
                        print(f"  ✓ Post {len(posts_data)}/{num_posts} extrait")
                    
                except Exception as e:
                    print(f"  ⚠️  Erreur lors de l'extraction du post {idx+1}: {str(e)}")
                    continue
                
                time.sleep(0.5)  # Petit délai entre chaque extraction
        
        except Exception as e:
            print(f"❌ Erreur lors de la recherche des posts: {str(e)}")
        
        # Sauvegarder les données
        if posts_data:
            df = pd.DataFrame(posts_data)
            df.to_csv(output_file, index=False, encoding="utf-8-sig")
            print(f"✅ Scraping terminé — {len(df)} posts enregistrés dans {output_file}")
        else:
            print("⚠️  Aucun post n'a pu être extrait. Vérifiez l'URL et les sélecteurs CSS.")
            print("💡 Note: LinkedIn nécessite souvent une connexion pour voir les posts complets.")
    
    finally:
        driver.quit()
        print("🔒 Navigateur fermé")


def scrape_multiple_companies(companies, num_posts=30):
    """
    Scrape plusieurs pages LinkedIn d'entreprises de télécommunications
    
    Args:
        companies: Dictionnaire {nom_entreprise: url_linkedin}
        num_posts: Nombre de posts par entreprise
    """
    all_data = []
    
    for company_name, company_url in companies.items():
        print(f"\n{'='*60}")
        print(f"📱 Scraping de {company_name}")
        print(f"{'='*60}")
        
        output_file = f"data/linkedin_{company_name.lower().replace(' ', '_')}.csv"
        scrape_linkedin_posts(company_url, num_posts, output_file)
        
        # Pause entre chaque entreprise
        time.sleep(5)


if __name__ == "__main__":
    import sys
    
    print("\n" + "="*80)
    print("🌐 LINKEDIN SCRAPER - Opérateurs Télécom Sénégal")
    print("="*80)
    print("\n⚠️  IMPORTANT: LinkedIn nécessite une authentification!")
    print("\n📋 Instructions:")
    print("   1. Le navigateur Chrome va s'ouvrir")
    print("   2. Connectez-vous manuellement à LinkedIn")
    print("   3. Une fois connecté, le script continuera automatiquement")
    print("\n💡 Astuce: Pour éviter de se reconnecter à chaque fois,")
    print("   vous pouvez configurer les cookies de session.\n")
    
    input("Appuyez sur ENTRÉE pour continuer...")
    
    # Exemple d'utilisation pour Expresso Sénégal
    # Note: Vous devrez adapter l'URL selon la vraie page LinkedIn
    
    # Une seule entreprise
    scrape_linkedin_posts(
        company_url="https://www.linkedin.com/company/expressosenegal/",
        num_posts=30,
        output_file="data/linkedin_posts_expresso.csv",
        headless=False  # Mettez True pour exécuter sans interface graphique
    )
    
    # Ou plusieurs entreprises à la fois
    # companies = {
    #     "Orange": "https://www.linkedin.com/company/orange-senegal/",
    #     "Expresso": "https://www.linkedin.com/company/expresso-senegal/",
    #     "Free": "https://www.linkedin.com/company/free-senegal/"
    # }
    # scrape_multiple_companies(companies, num_posts=20)
