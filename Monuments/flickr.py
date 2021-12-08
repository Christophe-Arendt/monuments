from flickrapi import FlickrAPI
from urllib.request import urlretrieve
from pprint import pprint
import os,time,sys


key = "fd2df8bd0ae6b507ec22b93ec98cf8aa"
secret = "4cae9373f9d6d2b4"
wait_time = 1

#Get the first value of the command line argument. In the following cases[cat]Get
# python download.py cat

def arrange_folders(monument):
    savedir = os.path.join("photos", monument)

    try:
        # Create target Directory
        os.makedirs(savedir)
        print("Directory ", savedir,  " Created ")
    except FileExistsError:
        print("Directory ", savedir,  " already exists")

    return savedir


def scrap_flickr(monument):

    """
    text :Search keyword
    per_page :Number of data you want to acquire
    media :Type of data to search
    sort :Sequence of data
    safe_seach :Whether to display UI content
    extras :The value of the option you want to get(url_q Image address information)
    """
    # Arrange folder structure
    savedir = arrange_folders(monument)

    # format:Data to receive(Receive with json)
    flickr = FlickrAPI(key, secret, format='parsed-json')
    result  = flickr.photos.search(
        text=monument,
        per_page = 400,
        media = 'photos',
        sort = 'relevance',
        safe_seach = 1,
        extras = 'url_q, licence'
    )

    #result
    photos = result['photos']
    #pprint(photos)


    for i, photo in enumerate(photos['photo']):
        url_q = photo['url_q']
        filepath = savedir + '/' + photo['id'] + '.jpg'

      #If there are duplicate files, skip them.
        if os.path.exists(filepath):
            continue
      #Download image data
        urlretrieve(url_q, filepath)
      #Wait 1 second to avoid overloading the server
        time.sleep(wait_time)


if __name__ == '__main__':
    #monumentname = sys.argv[1]
    monuments = ['Eiffel Tour', 'The Louvre', "Musée d'Orsay", 'Notre Dame de Paris',
                 'Les Invalides', 'Pont Alexandre III', 'Sacré-Coeur Paris', 'Place de la Concorde',
                 'Champ de Mars', 'Arc de Triomphe', 'Jardin du Luxembourg', 'Église Saint-Sulpice', 'Pantheon Paris',
                 'Pont Neuf', 'Pont Au Change', "Pont d'Iéna"]
    for monumentname in monuments:
        print(monumentname)
        scrap_flickr(monumentname)

