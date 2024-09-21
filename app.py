import streamlit as st
import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from datetime import datetime, timedelta

def get_sitemap(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except Exception as e:
        st.error(f"Error: {e}")
        return None


def parse_sitemap(xml_content, last_month_cutoff):
    try:
        soup = BeautifulSoup(xml_content, 'lxml')
        urls = []
        for url_elem in soup.find_all('url'):
            loc = url_elem.find('loc').text
            lastmod_str = url_elem.find('lastmod').text if url_elem.find('lastmod') else None

            if lastmod_str:
                lastmod_date = datetime.strptime(lastmod_str, '%Y-%m-%d')
                if lastmod_date >= last_month_cutoff:
                    urls.append(loc)

        return urls
    except Exception as e:
        st.error(f"Error parsing sitemap: {e}")
        return None

def assign_topics(urls, num_topics):
    # Use the last word from each URL as the document
    documents = [url.split('/')[-1].lower() for url in urls]

    # Vectorize the documents using CountVectorizer
    vectorizer = CountVectorizer(stop_words='english')
    X = vectorizer.fit_transform(documents)

    # Apply Latent Dirichlet Allocation (LDA) for topic modeling
    lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
    lda.fit(X)

    # Get the dominant topic for each URL
    topic_assignments = lda.transform(X).argmax(axis=1)

    # Create a dictionary to store clusters and topic words
    clusters = {i: {'urls': [], 'topic_words': []} for i in range(num_topics)}

    # Assign URLs to clusters
    for i, url in enumerate(urls):
        cluster_id = topic_assignments[i]
        clusters[cluster_id]['urls'].append(url)

    # Get top words for each topic
    for topic_id in range(num_topics):
        feature_names = vectorizer.get_feature_names_out()
        topic_word_weights = lda.components_[topic_id]
        top_word_indices = topic_word_weights.argsort()[-5:][::-1]
        top_words = [feature_names[index] for index in top_word_indices]
        clusters[topic_id]['topic_words'] = top_words

    return clusters

def main():
    st.title("URL Clustering App")

    url = st.text_input("Enter the URL of the Sitemap:", "https://example.com/sitemap.xml")
    if st.button("Fetch and Cluster URLs"):
        xml_content = get_sitemap(url)
        if xml_content is not None:
            st.success("Sitemap fetched successfully!")

            # Calculate the cutoff date for URLs modified in the last month
            last_month_cutoff = datetime.now() - timedelta(days=30)

            # Parse the sitemap and get the list of URLs modified in the last month
            urls = parse_sitemap(xml_content, last_month_cutoff)
            if urls is not None:
                st.write("List of URLs Modified in the Last Month:")
                for i, url in enumerate(urls, start=1):
                    st.write(f"{i}. {url}")

                # Cluster URLs and display clusters with topic words
                num_topics = st.slider("Select the number of topics:", min_value=1, max_value=10, value=3)
                clusters = assign_topics(urls, num_topics)
                st.write("Clusters:")
                for cluster_id, cluster_info in clusters.items():
                    st.write(f"Cluster {cluster_id + 1} (Topic Words: {', '.join(cluster_info['topic_words'])}):")
                    for url in cluster_info['urls']:
                        st.write(f"- {url}")


if __name__ == "__main__":
    main()
