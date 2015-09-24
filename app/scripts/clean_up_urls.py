from requests import exceptions
from datetime import datetime
import requests


class Log(object):
    def __init__(self, clean_urls_all, bad_urls_all, clean_urls_animals, bad_urls_animals, clean_urls_gaming,
                 bad_urls_gaming, clean_urls_strange, bad_urls_strange, clean_urls_educational,
                 bad_urls_educational):
        self.clean_urls_all = clean_urls_all
        self.bad_urls_all = bad_urls_all
        self.clean_urls_animals = clean_urls_animals
        self.bad_urls_animals = bad_urls_animals
        self.clean_urls_gaming = clean_urls_gaming
        self.bad_urls_gaming = bad_urls_gaming
        self.clean_urls_strange = clean_urls_strange
        self.bad_urls_strange = bad_urls_strange
        self.clean_urls_educational = clean_urls_educational
        self.bad_urls_educational = bad_urls_educational

    def counter(self, list_type, url_type):
        if url_type == 'clean':
            if list_type == 'all_urls':
                self.clean_urls_all += 1
            elif list_type == 'animals_urls':
                self.clean_urls_animals += 1
            elif list_type == 'gaming_urls':
                self.clean_urls_gaming += 1
            elif list_type == 'strange_urls':
                self.clean_urls_strange += 1
            elif list_type == 'educational_urls':
                self.clean_urls_educational += 1
        else:
            if list_type == 'all_urls':
                self.bad_urls_all += 1
            elif list_type == 'animals_urls':
                self.bad_urls_animals += 1
            elif list_type == 'gaming_urls':
                self.bad_urls_gaming += 1
            elif list_type == 'strange_urls':
                self.bad_urls_strange += 1
            elif list_type == 'educational_urls':
                self.bad_urls_educational += 1

    def readout(self):
        print '\nStats:'
        print 'Added %d clean URLs to all_urls.txt' % self.clean_urls_all
        print 'Removed %d bad URLs from all_urls.txt' % self.bad_urls_all
        print '\nAdded %d clean URLs to animals_urls.txt' % self.clean_urls_animals
        print 'Removed %d bad URLs from animals_urls.txt' % self.bad_urls_animals
        print '\nAdded %d clean URLs to gaming_urls.txt' % self.clean_urls_gaming
        print 'Removed %d bad URLs from gaming_urls.txt' % self.bad_urls_gaming
        print '\nAdded %d clean URLs to strange_urls.txt' % self.clean_urls_strange
        print 'Removed %d bad URLs from strange_urls.txt' % self.bad_urls_strange
        print '\nAdded %d clean URLs to educational_urls.txt' % self.clean_urls_educational
        print 'Removed %d bad URLs from educational_urls.txt' % self.bad_urls_educational


def remove_dupes(path, filename):
    with open('%s/%s' % (path, filename), 'r') as f:
        urls = [url.rstrip('\r\n') for url in f]
        unique_urls = []
        duplicate_urls = []

        for url in urls:
            if url + '\n' in unique_urls:
                duplicate_urls.append(url + '\n')
            else:
                unique_urls.append(url + '\n')

        # Open/close file in write mode to erase it
        open('%s/%s' % (path, filename), 'w').close()

        # Write contents of clean_urls list to file
        with open('%s/%s' % (path, filename), 'a+') as clean_file:
            for url in unique_urls:
                clean_file.write(url)

        print '%d duplicate URLs in %s' % (len(duplicate_urls), filename)
        print '%d total unique URLs now in %s' % (len(unique_urls), filename)


def clean_up_urls(path, filename):
    clean_urls = []
    url_number = 0
    list_type = filename[:filename.find('.txt')]
    with open('%s/%s' % (path, filename), 'a+') as f:
        urls_list = [url.rstrip('\r\n') for url in f]
    for image_url in urls_list:
        url_number += 1
        # Uncomment to see progress of script at runtime
        # print 'URL %d of %d' % (url_number, len(urls_list))
        if image_url in bad_urls_list:
            print '%s is in the bad_urls_list, skipping...' % image_url
            log.counter(list_type, 'bad')
            continue
        elif not image_url.endswith('.gif'):
            print '%s is not a .gif file, skipping...' % image_url
            log.counter(list_type, 'bad')
            continue
        else:
            try:
                r = requests.get(image_url, stream=True)
            except exceptions.ConnectionError:
                print 'Connection error, skipping URL...'
                continue
            code = r.status_code
            if not code == 200:
                print '%s is a broken link, skipping...' % image_url
                log.counter(list_type, 'bad')
                continue
            else:
                log.counter(list_type, 'clean')
                clean_urls.append(image_url + '\n')

    # Open/close file in write mode to erase it
    open('%s/%s' % (path, filename), 'w').close()

    # Write contents of clean_urls list to file
    with open('%s/%s' % (path, filename), 'a+') as clean_file:
        for url in clean_urls:
            clean_file.write(url)

if __name__ == '__main__':
    # Uncomment to run script off server
    # prompt = raw_input('Are you running this file from work or home? > ').lower()
    # if prompt == 'work':
    #     current_path = 'E:/programming/projects/blog/app/templates/pi_display/logs'
    # else:
    #     current_path = 'H:/programming/projects/blog/app/templates/pi_display/logs'

    # Server path
    current_path = '/home/tylerkershner/app/templates/pi_display/logs/'

    files = ['all_urls.txt', 'animals_urls.txt', 'gaming_urls.txt', 'strange_urls.txt', 'educational_urls.txt']

    with open('%s/%s' % (current_path, 'bad_urls.txt'), 'a+') as temp_file:
        bad_urls_list = [url.rstrip('\r\n') for url in temp_file]

    log = Log(0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    time_start = str(datetime.now().strftime('%I:%M %p on %A, %B %d, %Y'))
    for entry in files:
        print '\n#########################'
        print 'Beginning clean up of %s...' % entry
        clean_up_urls(current_path, entry)
        remove_dupes(current_path, entry)
    log.readout()
    time_end = str(datetime.now().strftime('%I:%M %p on %A, %B %d, %Y'))

    print '\nURL cleanup began at %s' % time_start
    print 'URL cleanup finished at %s' % time_end