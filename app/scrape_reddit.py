import praw
import sys
from datetime import datetime


def log():
    time = str(datetime.now().strftime('%I:%M %p on %A, %B %d, %Y'))
    log_data = '\n\nAdded %d gifs from /r/%s at %s.' % (count, target_subreddit, time)
    number_of_gifs = '\nTotal number of GIFs: %d' % (len(urls) + count)
    with open('/home/tylerkershner/app/reddit_scraper_log.txt', 'a') as log_file:
        log_file.write(log_data)
        log_file.write(number_of_gifs)
    print log_data
    print number_of_gifs

count = 0

if len(sys.argv) < 2:
    # no command line options sent:
    print('Usage:')
    print('  python %s [subreddit]' % (sys.argv[0]))
    sys.exit()

target_subreddit = sys.argv[1]

print '\n\n\n\nGathering image URLs from /r/%s...' % target_subreddit

r = praw.Reddit(user_agent='Raspberry Pi Project by billcrystals')

# Uncomment to scrape top results from year/month/all
submissions = r.get_subreddit(target_subreddit).get_hot(limit=50)
#submissions = r.get_subreddit(target_subreddit).get_top_from_year(limit=50)
#submissions = r.get_subreddit(target_subreddit).get_top_from_month(limit=50)
#submissions = r.get_subreddit(target_subreddit).get_top_from_all(limit=50)

file_object = open('/home/tylerkershner/app/urls.txt', 'r+')
urls = list(file_object)

for submission in submissions:
    if submission.url + '\n' in urls:
        pass
    elif '.gif' not in submission.url:
        pass
    elif 'minus' in submission.url:
        pass
    elif 'gifsound' in submission.url:
        pass
    elif 'gifsoup' in submission.url:
        pass
    elif 'Von_Karman' in submission.url:
        pass
    elif '?' in submission.url:
        print '? found in URL, snipping and adding...'
        url_snip = submission.url.find('?')
        file_object.write(submission.url[:url_snip])
        file_object.write('\n')
        count += 1

    else:
        print '%s not found in urls.txt, adding...' % submission.url
        file_object.write(submission.url)
        file_object.write('\n')
        count += 1

file_object.close()

log()

