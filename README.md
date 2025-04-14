# Blogspot Extractor

A tool to extract and display blog posts from Blogspot blogs, with HTML/Markdown conversion and a clean Tailwind CSS interface.

## Features

- Extracts all posts from a Blogspot blog using RSS feed
- Converts HTML content to clean Markdown format
- Preserves formatting, images, links, and metadata
- Provides a beautiful web interface using Tailwind CSS
- Handles pagination and rate limiting
- Includes logging and error handling

## Requirements

- Python 3.6+
- Required Python packages (see requirements.txt):
  - requests
  - feedparser
  - beautifulsoup4
  - tqdm
  - html2text

## Installation

1. Clone the repository:
```bash
git clone https://github.com/chrislarsc/blogspot-extractor.git
cd blogspot-extractor
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Extract blog posts:
```bash
python3 blogspot_extractor.py example.blogspot.com
```
This will create a `blogspot_posts.md` file with all the extracted posts.

2. View the blog archive:
- Start a local web server:
```bash
python3 -m http.server 8000
```
- Open `http://localhost:8000` in your web browser

## Output Format

The extracted posts are saved in Markdown format with the following structure:

```markdown
# Post Title

**Date:** YYYY-MM-DD
**URL:** [Original Post URL](https://example.blogspot.com/post-url)

Post content with preserved formatting, images, and links...
```

## Web Interface

The included `index.html` file provides a clean, responsive interface for viewing the extracted posts:

- Responsive layout using Tailwind CSS
- Beautiful typography with Merriweather font
- Proper handling of images, links, and text formatting
- Clean white cards for each post
- Automatic conversion of Markdown to HTML

## License

MIT License