import requests
import xml.etree.ElementTree as ET

# Define your array of sitemap URLs here
sitemap_urls = [
    'https://www.1mg.com/sitemap.xml',
    'https://1mg.com/doctors/sitemap.xml'
]

# Output file where URLs will be stored
output_file = 'urls.txt'

def fetch_and_process_sitemap(sitemap_url):
    try:
        # Make a GET request to fetch the sitemap
        response = requests.get(sitemap_url)
        response.raise_for_status()  # Raises HTTPError for bad responses

        # Parse the XML content
        root = ET.fromstring(response.content)
        # Update namespace if required for different sitemap formats
        urls = [url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text for url in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url')]

        # Append URLs to the output file
        with open(output_file, 'a') as file:
            file.write('\n'.join(urls) + '\n')

        print(f'Appended {len(urls)} URLs from {sitemap_url} to {output_file}')
    except requests.exceptions.HTTPError as e:
        print(f'Failed to fetch sitemap from {sitemap_url} - ({e.response.status_code}): {e.response.reason}')
    except requests.exceptions.RequestException as e:
        print(f'Request failed for {sitemap_url}: {e}')
    except ET.ParseError as e:
        print(f'Failed to parse XML from {sitemap_url}: {e}')
    except Exception as e:
        print(f'An error occurred with {sitemap_url}: {e}')

def main():
    # Process each sitemap URL from the array
    for sitemap_url in sitemap_urls:
        fetch_and_process_sitemap(sitemap_url)

if __name__ == '__main__':
    main()