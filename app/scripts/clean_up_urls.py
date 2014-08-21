import urllib2
from datetime import datetime


class Log(object):
    def __init__(self, count, bad_urls, large_urls):
        self.count = count
        self.bad_urls = bad_urls
        self.large_urls = large_urls

    def counter(self):
        self.count += 1

    def bad_urls_counter(self):
        self.bad_urls += 1

    def large_urls_counter(self):
        self.large_urls += 1

# Instantiating Log class
log = Log(0, 0, 0)


def clean_up_urls(path, urls_file):
    log.count = 0
    log.bad_urls = 0
    log.large_urls = 0
    print '\nBeginning cleanup of %s\n' % urls_file

    # Function to determine size of URL via HTTP header data
    def getsize(image_url):
        try:
            image_url = urllib2.urlopen(image_url)
            size = int(image_url.info()['content-length'])
            return size
        except(KeyError, urllib2.HTTPError, urllib2.URLError):
            return 'None'

    url_number = 0

    # Opening files, converting to Python lists
    with open('%s/%s' % (path, urls_file), 'a+') as temp_file:
        urls_list = list(temp_file)
    bad_urls_file = open('%s/bad_urls.txt' % path, 'a+')
    bad_urls_list = list(bad_urls_file)
    large_urls_file = open('%s/large_urls.txt' % path, 'a+')
    large_urls_list = list(large_urls_file)
    clean_urls_file = open('%s/clean_urls.txt' % path, 'a+')

    for url in urls_list:
        end_point = url.find('\n')
        url_test = url[:end_point]
        url_number += 1
        print 'URL %d of %d' % (url_number, len(urls_list))
        # Already in urls.txt
        if url + '\n' in bad_urls_list:
            log.bad_urls_counter()
            continue
        # Known Large URL
        elif url + '\n' in large_urls_list:
            log.large_urls_counter()
            continue
        # Not a .gif file
        elif not url_test.endswith('.gif'):
            print '%s is not a GIF file, skipping...' % url
            bad_urls_file.write(str(url))
            log.bad_urls_counter()
            continue
        # Don't want gifsound links
        elif 'sound' in url:
            print '%s is a gifsound link, skipping...' % url
            bad_urls_file.write(str(url))
            log.bad_urls_counter()
            continue
        try:
            r = urllib2.urlopen(url)
        except (urllib2.HTTPError, urllib2.URLError):
            print '%s returns 403 forbidden or timed out, skipping...' % url
            bad_urls_file.write(str(url))
            log.bad_urls_counter()
            continue
        # 404 status code is a broken link
        if r.getcode == 404:
            print '%s is a broken link (404), skipping...' % url
            # Logging bad URL
            bad_urls_file.write(str(url))
            log.bad_urls_counter()
            continue
        # 302 is redirection, meaning bad link
        elif r.getcode == 302:
            print '%s is a broken link (302), skipping...' % url
            # Logging bad URL
            bad_urls_file.write(str(url))
            log.bad_urls_counter()
            continue
        # The Pi has a hard time with GIFs larger than 8MBs
        if getsize(url) > 8192000:
            print '%s is larger than 8MBs, skipping...' % url
            large_urls_file.write(str(url))
            log.large_urls_counter()
            continue
        # Imgur 'removed' image is 503 bytes
        elif getsize(url) == 503:
            print '%s is a broken link (503 bytes), skipping...' % url
            bad_urls_file.write(str(url))
            log.bad_urls_counter()
            continue
        # If the getsize function returned None, there was an error
        elif getsize(url) == 'None':
            print '%s has no length data in HTTP header, skipping...' % url
            bad_urls_file.write(str(url))
            log.bad_urls_counter()
            continue
        else:
            print 'Clean URL, adding...'
            log.counter()
            clean_urls_file.write(str(url))

    # Closing files
    bad_urls_file.close()
    large_urls_file.close()
    clean_urls_file.close()

    # Creating Python list from newly populated clean_urls.txt
    with open('%s/clean_urls.txt' % path, 'r') as updated_clean_urls:
        clean_urls_list = list(updated_clean_urls)

    # Opening/closing urls.txt (taking advantage of side effect to erase contents)
    open('%s/%s' % (path, urls_file), 'w').close()

    # Re-opening urls.txt, appending with contents of the clean_urls.txt list, closing the file
    url_file = open('%s/%s' % (path, urls_file), 'a+')
    for url in clean_urls_list:
        url_file.write(url)
    url_file.close()

    # Opening and closing the clean_urls.txt file.  Side effect to erase contents of file.
    print '\n\n\n\nErasing contents of clean_urls.txt...'
    open('%s/clean_urls.txt' % path, 'w').close()

    # Opening updated file, printing # of URLs
    with open('%s/%s' % (current_path, urls_file), 'r') as f:
        number_of_gifs = len(list(f))
        print '\nTotal number of GIFS: %d' % number_of_gifs
    print '%d bad links removed' % log.bad_urls
    print '%d large GIFs removed' % log.large_urls


if __name__ == '__main__':
    prompt = raw_input('Are you running this file from work or home? > ').lower()
    if prompt == 'work':
        current_path = 'E:/programming/projects/blog/app/templates/pi_display/logs'
    else:
        current_path = 'H:/programming/projects/blog/app/templates/pi_display/logs'

    time_start = str(datetime.now().strftime('%I:%M %p on %A, %B %d, %Y'))

    files = ['all_urls.txt', 'animals_urls.txt', 'gaming_urls.txt', 'strange_urls.txt', 'educational_urls.txt']
    for entry in files:
        clean_up_urls(current_path, entry)

    time_end = str(datetime.now().strftime('%I:%M %p on %A, %B %d, %Y'))

    print 'URL cleanup began at %s' % time_start
    print 'URL cleanup finished at %s' % time_end