import sys
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool
# import the correct version of urllibx
if sys.version_info < (3, 0, 0):
    import urllib2 as urllib
else:
    import urllib.request as urllib


class Rosh():
    def __init__(self):
        self.path = 'https://roshpit.ca/'
        self.gold_ids = []
        self.silver_ids = []
        self.gold_top = []
        self.silver_top = []

    def _get_uids(self):
        can = 'https://roshpit.ca/leaderboards'
        soup = can_opener(can)
        self.gold_ids = self._get_uids_sub(soup, 'gold_content')
        self.silver_ids = self._get_uids_sub(soup, 'silver_content')
        return self

    def _get_uids_sub(self, soup, id_type):
        k = 0
        block = soup.find('div', id=id_type)
        prs = block.find_all('div', 'player-row')
        ids = []
        for pr in prs:
            ids.append(int(pr.get('data-user-id')))
            k = k + 1
        return ids

    def _get_user_info(self, uid):
        can = '{}users/{}'.format(self.path, uid)
        soup = can_opener(can)
        gold_bet = get_user_gold(soup)
        user = get_user_name(soup)
        silver = get_user_silver(soup)
        mult = get_user_mult(soup)
        user_info = [user, mult, gold_bet, silver]
        return user_info

    def _get_users_info(self, top_type, nthreads, nuids):
        if top_type.lower() == 'gold':
            property_tag = 'gold_top'
            ids = getattr(self, 'gold_ids')
        else:
            property_tag = 'silver_top'
            ids = getattr(self, 'silver_ids')
        pool = Pool(nthreads)
        top = pool.map(self._get_user_info, ids[0:nuids])
        setattr(self, property_tag, top)
        return self

    def top_five(self, check_top_n):
        if not self.gold_ids or not self.silver_ids:
            self._get_uids()
        if not self.gold_top:
            self._get_users_info('gold', 10, check_top_n)
        if not self.silver_top:
            self._get_users_info('silver', 2, 5)
        self.gold_top.sort(key=lambda x: x[2])
        gold_top = self.gold_top[-5::]
        gold_top.reverse()
        return gold_top, self.silver_top


def get_user_gold(soup):
    tag = 'outstanding_gold_bets'
    gold_bet = int(soup.find('div', id=tag).text.replace(',', ''))
    return gold_bet


def get_user_name(soup):
    name_plate = soup.find('div', 'name-plate')
    names = name_plate.find_all('div')
    name = str(names[0].text)
    if name == '\n\n':
        name = str(names[1].text)
    return name


def get_user_mult(soup):
    mult_element = soup.find('img', id='multiplier')
    if not mult_element:
        mult = 1
    else:
        mult = int(mult_element.get('src')[-5])
    return mult


def get_user_silver(soup):
    silver = int(soup.find('span', id='silver-bal').get('data-silver'))
    return silver


def can_opener(can):
    soup = BeautifulSoup(urllib.urlopen(can))
    return soup


def printer(gold, silver):
    print('Top five gold users:')
    _print_helper(gold)
    print('\nTop five silver users:')
    _print_helper(silver)


def _print_helper(blob):
    for b in blob:
        print('|%-12s|%-2dx|%-9d|%-11d' % (b[0], b[1], b[2], b[3]))

if __name__ == '__main__':
    if len(sys.argv) == 1:
        check_top_n = 50
    else:
        check_top_n = int(sys.argv[1])
    r = Rosh()
    gold, silver = r.top_five(check_top_n)
    printer(gold, silver)
