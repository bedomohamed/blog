from requests import exceptions
import requests
import praw
import time


class Log(object):
    def __init__(self, all_gifs, animals_gifs, gaming_gifs, strange_gifs, educational_gifs, temp_count):
        self.all_gifs = all_gifs
        self.animals_gifs = animals_gifs
        self.gaming_gifs = gaming_gifs
        self.strange_gifs = strange_gifs
        self.educational_gifs = educational_gifs
        self.temp_count = temp_count

    def gif_counter(self, category):
        if category == 'all':
            self.all_gifs += 1
        elif category == 'animals':
            self.animals_gifs += 1
        elif category == 'gaming':
            self.gaming_gifs += 1
        elif category == 'strange':
            self.strange_gifs += 1
        elif category == 'educational':
            self.educational_gifs += 1
        self.temp_count += 1

    def readout(self):
        all_categories = ['all', 'animals', 'gaming', 'strange', 'educational']
        numbers = [self.all_gifs, self.animals_gifs, self.gaming_gifs, self.strange_gifs, self.educational_gifs]
        counter = 0
        print '\n'
        for entry in all_categories:
            print '%d GIFs added to %s_urls.txt' % (numbers[counter], entry)
            counter += 1


# Object to hold all URLs to be written to txt file
class Temp(object):
    def __init__(self, urls):
        self.urls = urls


def request_url(url):
    try:
        r = requests.get(url, stream=True)
        size_in_bytes = int(r.headers['content-length'])
        float_size = float(size_in_bytes) / 1051038
        code = r.status_code
        data = {
            'size': size_in_bytes,
            'float_size': float_size,
            'code': code
        }
        return data
    except (KeyError, requests.exceptions.SSLError, requests.exceptions.ConnectionError):
        # No content-length HTTP header or error with request handshake
        return None


def get_reddit_urls(sub, path, category):
    print '\nGathering image URLs from /r/%s...' % sub
    temp_list = []

    # Creating Python list from url file
    with open('%s/%s_urls.txt' % (path, category), 'a+') as f:
        current_urls = list(f)

    # Accessing Reddit API
    r = praw.Reddit(user_agent='Raspberry Pi Project by billcrystals')
    submissions = r.get_subreddit(sub).get_hot(limit=200)
    for submission in submissions:
        if submission.url + '\n' in current_urls:
            continue
        else:
            temp_list.append(submission.url)

    return temp_list


def process_urls(url_list):
    print 'Processing URLs...'
    temp_list = []
    for url in url_list:
        if not url.endswith('gif'):
            continue
        else:
            try:
                url_info = request_url(url)
                if not url_info['code'] == 200:
                    continue
                elif url_info['size'] == 503:
                    continue
                elif url_info['float_size'] > 6.00:
                    continue
                else:
                    temp_list.append(url)
            except TypeError:
                continue

    return temp_list


def write_urls(url_list, path, category):
    unique_urls = []

    # Creating Python list from url file
    with open('%s/%s_urls.txt' % (path, category), 'a+') as f:
        current_urls = list(f)

    for url in url_list:
        if str(url) + '\n' in current_urls:
            continue
        else:
            log.gif_counter(category)
            unique_urls.append(url + '\n')

    # Appending contents of unique_urls to current url file
    with open('%s/%s_urls.txt' % (path, category), 'a+') as f:
        for line in unique_urls:
            try:
                f.write(line)
            except UnicodeEncodeError:
                continue

    # Appending contents of unique_urls to current url_to_play file
    with open('%s/%s_urls_to_play.txt' % (path, category), 'a+') as f:
        for line in unique_urls:
            try:
                f.write(line)
            except UnicodeEncodeError:
                continue


if __name__ == '__main__':
    log = Log(0, 0, 0, 0, 0, 0)
    current_path = '/home/tylerkershner/app/templates/pi_display/logs/'
    categories = ['all', 'animals', 'gaming', 'strange', 'educational']
    subreddits = [
        # All
        ['gifs', 'gif', 'blackpeoplegifs', 'SpaceGifs', 'physicsgifs', 'educationalgifs', 'chemicalreactiongifs',
         'SurrealGifs', 'Puggifs', 'slothgifs', 'asianpeoplegifs', 'gaming_gifs', 'Movie_GIFs', 'funnygifs',
         'wheredidthesodago', 'reactiongifs', 'creepy_gif', 'perfectloops', 'aww_gifs', 'AnimalsBeingJerks',
         'AnimalGIFs', 'whitepeoplegifs', 'interestinggifs', 'cinemagraphs', 'wtf_gifs',
         'MichaelBayGifs', 'naturegifs', 'pugs', 'gaming', 'Wastedgifs', 'GamePhysics', 'catgifs',
         'opticalillusions', 'wrestlinggifs', 'shittyreactiongifs', 'IdiotsFightingThings', 'Whatcouldgowrong',
         'interestingasfuck', 'AnimalsBeingBros', 'PerfectTiming', 'holdmybeer', 'StartledCats', 'combinedgifs',
         'Damnthatsinteresting', 'shittyrobots', 'catpranks', 'Awwducational', 'instant_regret', 'oddlysatisfying',
         'Perfectfit', 'SuperShibe', 'shibe', 'corgi', 'animalgifs', 'doggifs',
         'sleepinganimals', 'StoppedWorking', 'AnimalsFailing', 'brushybrushy', 'AnimalsBeingPolite',
         'AnimalsBeingFunny', 'SloMoAnimals', 'AnimalReactions', 'awwakeup'],
        # Animals
        ['Puggifs', 'slothgifs', 'aww_gifs', 'AnimalsBeingJerks', 'AnimalGIFs', 'pugs', 'CatGifs', 'SuperShibe',
         'shibe', 'corgi', 'Awwducational', 'AnimalsBeingBros', 'StartledCats', 'catpranks', 'animalgifs', 'doggifs',
         'sleepinganimals', 'StoppedWorking', 'AnimalsFailing', 'brushybrushy', 'AnimalsBeingPolite',
         'AnimalsBeingFunny', 'SloMoAnimals', 'AnimalReactions', 'awwakeup'],
        # Gaming
        ['gaming_gifs', 'gaming', 'GamePhysics', 'ps4gifs'],
        # Strange
        ['creepy_gif', 'wtf_gifs', 'SurrealGifs'],
        # Educational
        ['physicsgifs', 'educationalgifs', 'chemicalreactiongifs', 'interestinggifs', 'Damnthatsinteresting',
         'interestingasfuck']
    ]
    start = time.time()
    count = 0
    for cat in categories:
        print '\n####################################'
        print 'Now scraping %s subreddits' % cat
        print '####################################'
        temp_urls = Temp([])
        for subreddit in subreddits[int('%d' % count)]:
            raw_urls = get_reddit_urls(subreddit, current_path, cat)
            processed_urls = process_urls(raw_urls)
            for processed_url in processed_urls:
                temp_urls.urls.append(processed_url)
        write_urls(temp_urls.urls, current_path, cat)
        count += 1
    log.readout()
    end = time.time()
    print '\nScript Execution Time: %.2f seconds' % float(end - start)