import streamlit as st
import requests
from urllib.parse import urlparse, urljoin

def fetch_robots_txt(site_url):
    try:
        url = urljoin(site_url, 'robots.txt')
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX/5XX
        return response.text
    except requests.RequestException:
        return None

def extract_sitemap_urls_from_robots_txt(robots_txt):
    sitemap_urls = []
    for line in robots_txt.splitlines():
        if line.startswith('Sitemap:'):
            sitemap_url = line.split(":", 1)[1].strip()
            sitemap_urls.append(sitemap_url)
    return sitemap_urls

def try_common_sitemap_urls(site_url):
    common_paths = [
        'sitemap.xml',
        'sitemap_index.xml',
        'post-sitemap.xml',
        'sitemap',
        'rss',
        'rss.xml',
        'sitemap.txt',
        'atom.xml'
    ]
    found_sitemaps = []
    for path in common_paths:
        url = urljoin(site_url, path)
        try:
            response = requests.head(url)  # Using HEAD to check if the URL exists
            if response.status_code == 200:
                found_sitemaps.append(url)
        except requests.RequestException:
            continue
    return found_sitemaps

def main():
    st.title('Sitemap Extractor')
    
    site_url = st.text_input('Enter the website URL:', '')

    if site_url:
        sitemaps = []
        robots_txt = fetch_robots_txt(site_url)
        if robots_txt:
            sitemaps.extend(extract_sitemap_urls_from_robots_txt(robots_txt))
        
        if not sitemaps:  # If no sitemaps were found in robots.txt
            sitemaps.extend(try_common_sitemap_urls(site_url))
        
        # Note: Automated Google search is not implemented due to potential ToS violation.
        # Encourage users to manually search and input URLs.
        
        manual_sitemap_url = st.text_input('Enter a sitemap URL found via Google search or other means:', '')
        if manual_sitemap_url:
            sitemaps.append(manual_sitemap_url)
        
        if sitemaps:
            st.success("Found Sitemaps:")
            for sitemap in sitemaps:
                st.write(sitemap)
        else:
            st.error("No sitemaps found. Try entering URLs manually.")

if __name__ == '__main__':
    main()