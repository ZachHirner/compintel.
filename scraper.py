import os
import time
from bs4 import BeautifulSoup
import undetected_chromedriver as uc

def scrape_site(url):
    options = uc.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # Matches the Chrome 150 version on GitHub's runner
    driver = uc.Chrome(options=options, use_subprocess=True, version_main=150)
    try:
        driver.get(url)
        # Give the page 6 seconds to fully render
        time.sleep(6) 
        
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        
        # Clean up script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
            
        text_content = soup.get_text(separator="\n", strip=True)
        return text_content[:25000] # Grab the first 25,000 characters
    finally:
        driver.quit()

if __name__ == "__main__":
    # Targeting OpenText's ValueEdge / DevOps Quality product page
    target_url = "https://www.opentext.com/products/valueedge"
    print(f"Starting cloud scrape of {target_url}...")
    result_text = scrape_site(target_url)
    
    with open("raw_competitor_data.txt", "w", encoding="utf-8") as f:
        f.write(result_text)
    print("Scrape complete!")
