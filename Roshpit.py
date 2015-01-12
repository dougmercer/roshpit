import sys
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool
# import the correct version of urllib, depending on python version
if sys.version_info < (3, 0, 0):
    import urllib2 as urllib
else:
    import urllib.request as urllib


class Rosh():
    def __init__(self):
        # constructor
        self.path = 'https://roshpit.ca/'
        self.gold_ids = []
        self.silver_ids = []
        self.gold_top = []
        self.silver_top = []

    def top_five(self, check_top_n):
        '''
        top_five is the primary function of this module (so far, at least)
        Inputs:
            check_top_n - number of users on the gold ladder to compare
        Outputs:
            gold_top - 5 users with greatest outstanding gold bets
            silver_top - 5 users with greatest silver balances
        '''
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

    def _get_uids(self):
        '''
        Method _get_uids stores the user ids of the top gold and silver users
        in the gold_ids and silver_ids attributes
        '''
        can = self.path + 'leaderboards'
        soup = can_opener(can)
        self.gold_ids = self._get_uids_by_type(soup, 'gold_content')
        self.silver_ids = self._get_uids_by_type(soup, 'silver_content')
        return self

    def _get_uids_by_type(self, soup, id_type):
        '''
        _get_uids_by_type is a helper function to _get_uids.
        This function iterates through each player-row of the given type
        either (silver or gold), extracts, and returns a list of user ids.
        '''
        block = soup.find('div', id=id_type)
        prs = block.find_all('div', 'player-row')
        ids = []
        for pr in prs:
            ids.append(int(pr.get('data-user-id')))
        return ids

    def _get_users_info(self, top_type, nthreads, nuids):
        '''
        _get_users_info is a multithreaded function that creates a pool
        of workers tasked with computing _get_user_info for each user in
        ids[0:nuids]
        Inputs:
            top_type - distinguishes whether we are looking for gold or silver
            nthreads - number of threads in the pool
            nuids - number of users to check
        '''
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

    def _get_user_info(self, uid):
        '''
        Helper function to _get_users_info. Tabulates the following info
        for the user, uid:
            user name
            current outstanding bet
            current silver balances
            current multiplier
        Output:
            user_info - summary of the above data for uid
        '''
        can = '{}users/{}'.format(self.path, uid)
        soup = can_opener(can)
        user = self._get_user_name(soup)
        gold_bet = self._get_user_gold(soup)
        silver = self._get_user_silver(soup)
        mult = self._get_user_mult(soup)
        user_info = [user, mult, gold_bet, silver]
        return user_info

    def _get_user_name(self, soup):
        '''
        Parse soup for username
        '''
        name_plate = soup.find('div', 'name-plate')
        names = name_plate.find_all('div')
        name = names[0].text
        if name == '\n\n':
            name = names[1].text
        return name

    def _get_user_gold(self, soup):
        '''
        Parse soup for outstanding gold
        '''
        tag = 'outstanding_gold_bets'
        gold_bet = int(soup.find('div', id=tag).text.replace(',', ''))
        return gold_bet

    def _get_user_silver(self, soup):
        '''
        Parse soup for silver balance
        '''
        silver = int(soup.find('span', id='silver-bal').get('data-silver'))
        return silver

    def _get_user_mult(self, soup):
        '''
        Parse soup for current multiplier
        '''
        mult_element = soup.find('img', id='multiplier')
        if not mult_element:
            mult = 1
        else:
            mult = int(mult_element.get('src')[-5])
        return mult

    def printer(self, gold, silver):
        print('Top five gold users:')
        self._print_helper(gold)
        print('\nTop five silver users:')
        self._print_helper(silver)

    def _print_helper(self, blob):
        for b in blob:
            print('|%-12s|%-2dx|%-9d|%-11d' % (b[0], b[1], b[2], b[3]))


def can_opener(can):
    soup = BeautifulSoup(urllib.urlopen(can))
    return soup


if __name__ == '__main__':
    if len(sys.argv) == 1:
        check_top_n = 50
    else:
        check_top_n = int(sys.argv[1])
    r = Rosh()
    gold, silver = r.top_five(check_top_n)
    r.printer(gold, silver)
