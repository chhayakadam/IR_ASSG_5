#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup

# List of Pune engineering college websites
college_urls = [
    "http://www.coep.org.in",  # College of Engineering Pune
    "https://www.viit.ac.in",  # Vishwakarma Institute of Information Technology
    "http://www.mitpune.edu.in",  # MIT Pune
    # Add more college websites here
]

# Function to fetch and parse the page using BeautifulSoup
def fetch_page_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup
        else:
            print(f"Failed to retrieve {url} - Status Code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error occurred while fetching {url}: {e}")
        return None

# Initialize index to store link counts and PageRank
index = {url: {'outgoing_count': 0, 'incoming_count': 0, 'page_rank': 1.0} for url in college_urls}

# Fetch and analyze links from each college website
def fetch_college_data():
    for url in college_urls:
        print(f"\nFetching data from: {url}")
        page_content = fetch_page_content(url)

        if page_content:
            links = page_content.find_all('a')
            outgoing_count = 0

            for link in links:
                href = link.get('href')
                if href:
                    href = requests.compat.urljoin(url, href)
                    outgoing_count += 1

                    # Check if the link points to another college in the list
                    for target_url in college_urls:
                        if href.startswith(target_url) and href != url:
                            index[target_url]['incoming_count'] += 1

            index[url]['outgoing_count'] = outgoing_count
        else:
            print(f"Could not retrieve content from {url}")

# Simple PageRank calculation function
def calculate_page_rank(iterations=10, damping_factor=0.85):
    for i in range(iterations):
        new_ranks = {}
        for url in college_urls:
            # Calculate new rank based on incoming links
            new_rank = (1 - damping_factor) / len(college_urls)
            for target_url in college_urls:
                if url != target_url and index[target_url]['outgoing_count'] > 0:
                    # Each incoming link adds to the rank based on target's rank and outgoing links
                    new_rank += (damping_factor * index[target_url]['page_rank'] /
                                 index[target_url]['outgoing_count'])
            new_ranks[url] = new_rank

        # Update ranks after each iteration
        for url in college_urls:
            index[url]['page_rank'] = new_ranks[url]

# Run the crawler and calculate PageRank
fetch_college_data()
calculate_page_rank()

# Print results
print("\nCount of Links and PageRank:")
for college, counts in index.items():
    print(f"{college}:")
    print(f"  Outgoing Links Count: {counts['outgoing_count']}")
    print(f"  Incoming Links Count: {counts['incoming_count']}")
    print(f"  PageRank Score: {counts['page_rank']:.4f}")


# In[ ]:




