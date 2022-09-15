import requests
from bs4 import BeautifulSoup


class MovieInnerPage:
    def __init__(self, user_url):
        self._moviePage_url = user_url
        self._moviePage_req = requests.get(self._moviePage_url)
        self._moviePage_html = self._moviePage_req.text
        self._moviePage_soup = BeautifulSoup(self._moviePage_html, 'html.parser')
        self._moviePage_section = self._moviePage_soup.find(
                                                'section', {
                                                    'class': 
                                                    ['ipc-page-section',
                                                    'ipc-page-section--baseAlt',
                                                    'ipc-page-section--tp-none',
                                                    'ipc-page-section--bp-xs',
                                                    'sc-2a827f80-1',
                                                    'gvCXlM']
                                                    })
        self._moviePage_ul = self._moviePage_soup.find(
            'ul', {
                'data-testid': 'hero-title-block__metadata'})
        self._moviePage_discr_div = self._moviePage_section.find(
            'div', {
                'class': 'sc-16ede01-7'})
        self._moviePage_catg_div = self._moviePage_section.find(
            'div', {
                'class': 'ipc-chip-list__scroller'})
        self._moviePage_rating_div = self._moviePage_section.find(
            'div', {
                'class': 'sc-7ab21ed2-0'})
    

    def htmlGenerate(self):
        """ Saving the each movie page in a html format """
        filename = (self._moviePage_url.strip('/').split('/')[-1]) + '.html'
        with open(f'downloads/html/{filename}', 'w') as f:
            f.write(self._moviePage_html)


    def movieCert(self):
        """ Getting the details of Movie certification """
        return ([li.span.string  for li in self._moviePage_ul.findAll('li') if li.span != None][1])


    def movieHours(self):
        """ Getting the total running time of Movie """
        return self._moviePage_ul.findAll('li')[-1].text.strip()


    def movieStory(self):
        """ Grtting the stroyline of the Movie """
        return (self._moviePage_discr_div.span.string)


    def movieCategories(self):
        """ Getting the genre of the Movie """
        return (', '.join([span.string for span in self._moviePage_catg_div.findAll('span')]))


    def movieRating(self):
        """ This is to extract the IMDb rating for the Movie """
        # movieRating = ''.join([span.text for span in self._moviePage_rating_div.findAll('span')])
        return ([div.text for div in self._moviePage_rating_div.findAll('div')][0])


    def movieVote(self):
        """ This is the total votes given by each users of IMDb """
        return ([div.text for div in self._moviePage_rating_div.findAll('div')][2])

