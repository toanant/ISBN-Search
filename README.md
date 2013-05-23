ISBN-Search
===========

Designed to crawl for book details &amp; prices from books selling website in india &amp; search books 
using ISBN or keywords for price comparison.

#Getting Started
1. Read `INSTALL.md` for installation instructions.
2. Once instllation has been completed, go through the different steps of ISBN collection, Details collection &amp;
price collection directory and run crawl.py to assign tasks to celery worker using RabbitMQ broker.


```bash
## `cd` to `isbn_collection/`
cd isbn_collection/
## Run celery worker under screen session
screen -dmS "celery" celery -A tasks worker --loglevel=info --concurrency=4
## Run crawler using
python crawl.py
```
