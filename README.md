### Project Summary: Sitemap Search, Clustering, and Visualization Tool

This project is focused on extracting, analyzing, and visualizing sitemaps from websites. It combines methods to find all available sitemaps, clusters the extracted URLs based on trends, and offers an intuitive visualization of the results. Here's a breakdown of the key components:

#### **1. Sitemap Extraction**
   - **Automated Sitemap Discovery**: 
     - Fetches `robots.txt` to locate sitemaps.
     - Attempts common sitemap URLs (like `/sitemap.xml` or `/rss.xml`).
     - Provides a manual input option for users to add any sitemap URLs found via external search.
   - **Recursion through Nested Sitemaps**: 
     - The tool can recursively crawl nested sitemaps, ensuring all URLs are found.
   - **Outputs**: 
     - A list of discovered URLs, including any available "last modified" dates.

#### **2. URL Data Scraping**
   - **Detailed Sitemap Scraping**: 
     - Uses `BeautifulSoup` to parse XML files and extract individual page URLs along with metadata.
   - **CSV Export**: 
     - Users can download the extracted URL data as a CSV file for further analysis or records.
    

#### **3. Clustering and Trend Analysis**
   - **Natural Language Processing (NLP)**: 
     - Uses n-gram analysis and filtering techniques to extract meaningful patterns from URLs and queries.
   - **Cluster-Based Taxonomy Creation**: 
     - Applies clustering models (like HDBSCAN) to group URLs into relevant topics or categories based on their content.
     - Supports both local and OpenAI-powered models for clustering and embedding.
   - **Automatic Trend Detection**: 
     - Analyzes trends from extracted URLs to reveal search behaviors or web structure trends.

#### **4. Visualization and Downloadable Results**
   - **Taxonomy Visualization**: 
     - The tool generates a structured taxonomy (category hierarchy) from clustered URLs.
   - **Downloadable CSV**: 
     - The results can be downloaded as a CSV for external analysis.
   - **User Interface**: 
     - Built using **Streamlit**, making the tool user-friendly and accessible through an interactive web-based UI.

#### **Use Case**
   - This tool is beneficial for SEO professionals, data analysts, or anyone looking to analyze website structure and trends from sitemaps. By automating the sitemap discovery process and offering trend analysis and clustering, it streamlines tasks that would otherwise require manual inspection of large datasets.

In summary, the project is designed to simplify sitemap discovery and analysis by automating URL extraction, clustering, and visualization to uncover trends and web structure insights.
