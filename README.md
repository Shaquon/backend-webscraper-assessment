# Webscraper 

A command line program to scrape a single web page, extracting any URLs, email addresses, and phone numbers it contains.

You may find you need to tweak the patterns a bit for your application. For example, if you're using re.findall to search for emails in a large block of text, your pattern shouldn't use the ^ and $ meta-characters to limit matches to the full string.

You should be able to get some useful initial results, but you may also see some spurious results due to regular expressions matching text within <script> blocks, for example.

You can experiment with using regular expressions to strip tags by doing things like:

re.sub(r"<[^>]*>", " ", text)
Before going too far down this path however, you may also find it worthwhile to explore the HTMLParser (Links to an external site.)Links to an external site. library, which can give you more robust options for navigating an HTML document.

Output
Your scraper doesn't have to conform to a specific output format, but running it with a command like:

python scraper.py http://kenzie.academy/
Should output some reasonably formatted text listing the URLs, email addresses, and phone numbers found in the page.