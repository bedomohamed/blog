import urllib
import re

# Opening current URL file for reading
file_object = open('H:/programming/projects/blog/app/templates/pi_display/urls.txt', 'r')
bad_urls = open('H:/programming/projects/blog/app/templates/pi_display/bad_urls.txt', 'r')

# Creating list from urls.txt, closing the file
urls = list(file_object)
bad_urls_list = list(bad_urls)
file_object.close()
bad_urls.close()

regex = re.compile(r".gif")

# Function to determine size of URL via HTML header data
def getsize(uri):
    image_file = urllib.urlopen(uri)
    size = image_file.headers.get("content-length")
    image_file.close()
    if size is None:
        return 'None'
    else:
        return int(size)

url = 'http://img.imaggifsy.com/aO'
print bool(regex.search(url))