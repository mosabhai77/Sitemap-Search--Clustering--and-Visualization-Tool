import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin

st.set_page_config(page_title='Sitemap Scraper', layout='wide')
st.sidebar.title("About")
st.sidebar.info(
    "This tool scrapes the sitemap of a given website, including any nested sitemaps, "
    "and allows you to download the results as a CSV file."
)

# Function to recursively scrape sitemap
def scrape_sitemap(url):
    sitemap_urls = []
    r = requests.get(url)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'xml')
        sitemap_tags = soup.find_all("sitemap")
        url_tags = soup.find_all("url")

        for sitemap in sitemap_tags:
            sitemap_url = sitemap.findNext("loc").text
            sitemap_urls.extend(scrape_sitemap(sitemap_url))

        for url_tag in url_tags:
            page_url = url_tag.findNext("loc").text
            sitemap_urls.append(page_url)

    return sitemap_urls

# Streamlit UI
st.title('Sitemap Scraper')

# Input for website URL
website_url = st.text_input('Enter website URL (including http/https):', '')

if st.button('Scrape Sitemap'):
    if website_url:
        # Ensure the URL ends with /sitemap.xml
        if not website_url.endswith('/sitemap.xml'):
            website_url = urljoin(website_url, '/sitemap.xml')

        # Scrape the sitemap
        try:
            all_urls = scrape_sitemap(website_url)

            # Convert to DataFrame
            df = pd.DataFrame(all_urls, columns=['URL'])

            # Display the DataFrame in the app
            st.dataframe(df)

            # Convert DataFrame to CSV
            csv = df.to_csv(index=False).encode('utf-8')

            # Download link for CSV
            st.download_button(label="Download CSV",
                               data=csv,
                               file_name='sitemap_urls.csv',
                               mime='text/csv')

            st.success('Sitemap scraped successfully!')

        except Exception as e:
            st.error(f'An error occurred: {e}')
    else:
        st.error('Please enter a valid website URL.')
