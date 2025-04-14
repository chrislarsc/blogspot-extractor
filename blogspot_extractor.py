#!/usr/bin/env python3

import sys
import re
import logging
import requests
import feedparser
from bs4 import BeautifulSoup
from tqdm import tqdm
import html2text

class BlogspotExtractor:
    def __init__(self, domain):
        self.domain = domain
        self.output_file = "blogspot_posts.md"
        self.h = html2text.HTML2Text()
        self.h.body_width = 0  # Don't wrap text
        self.h.ignore_links = False
        self.h.ignore_images = False
        self.h.ignore_emphasis = False
        self.h.ignore_tables = False
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('extraction.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def get_feed_url(self, start_index=1, max_results=500):
        """Construct the RSS feed URL with pagination parameters."""
        return f"https://{self.domain}/feeds/posts/default?start-index={start_index}&max-results={max_results}"

    def get_all_posts(self):
        """Fetch all blog posts using pagination."""
        all_entries = []
        start_index = 1
        max_results = 500

        while True:
            feed_url = self.get_feed_url(start_index, max_results)
            self.logger.info(f"Fetching feed from: {feed_url}")
            
            try:
                response = requests.get(feed_url, verify=False)
                feed = feedparser.parse(response.content)
                
                if not feed.entries:
                    break
                    
                all_entries.extend(feed.entries)
                if len(feed.entries) < max_results:
                    break
                    
                start_index += max_results
                
            except Exception as e:
                self.logger.error(f"Error fetching feed: {str(e)}")
                break

        return all_entries

    def clean_text(self, text):
        """Clean and format the Markdown text while preserving formatting."""
        # Normalize line endings
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        # Handle images: ensure only two newlines after them
        text = re.sub(r'!\[.*?\]\(.*?\)\n+', r'\g<0>\n\n', text)
        
        # First pass: remove excessive blank lines
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Second pass: ensure proper spacing around headers
        text = re.sub(r'(\n#{1,6} .*?)\n{0,1}', r'\1\n\n', text)
        
        # Third pass: ensure proper spacing around blockquotes
        text = re.sub(r'(\n> .*?)\n{0,1}', r'\1\n\n', text)
        
        # Final pass: limit consecutive blank lines to 2
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        return text.strip()

    def extract_post_content(self, url):
        """Extract the main content from a blog post and convert to Markdown."""
        try:
            response = requests.get(url, verify=False)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Try multiple selectors for finding the main content
            content = None
            selectors = [
                '.post-body',
                '.entry-content',
                '.post-content',
                'article',
                '.blog-post'
            ]
            
            for selector in selectors:
                content = soup.select_one(selector)
                if content:
                    break
            
            if not content:
                self.logger.warning(f"Could not find main content for {url}")
                return ""
            
            # Convert HTML to Markdown
            markdown = self.h.handle(str(content))
            return self.clean_text(markdown)
            
        except Exception as e:
            self.logger.error(f"Error extracting content from {url}: {str(e)}")
            return ""

    def extract_all_posts(self):
        """Extract all posts from the blog and save to a file."""
        self.logger.info(f"Starting extraction at {self.domain}")
        self.logger.info(f"Output will be saved to {self.output_file}")
        
        entries = self.get_all_posts()
        self.logger.info(f"Found {len(entries)} posts to process")
        
        with open(self.output_file, 'w', encoding='utf-8') as f:
            for entry in tqdm(entries, desc="Extracting posts"):
                try:
                    title = entry.title
                    date = entry.published.split('T')[0]
                    url = entry.link
                    content = self.extract_post_content(url)
                    
                    # Write post with Markdown formatting
                    f.write(f"# {title}\n\n")
                    f.write(f"**Date:** {date}\n")
                    f.write(f"**URL:** [{url}]({url})\n\n")
                    f.write(f"{content}\n\n")
                    f.write("---\n\n")  # Separator between posts
                    
                except Exception as e:
                    self.logger.error(f"Error processing entry: {str(e)}")
                    continue
        
        self.logger.info(f"Extraction completed. Results saved to {self.output_file}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 blogspot_extractor.py domain.blogspot.com")
        sys.exit(1)
        
    domain = sys.argv[1]
    extractor = BlogspotExtractor(domain)
    extractor.extract_all_posts()

if __name__ == "__main__":
    main()