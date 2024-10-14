# -*- coding: utf-8 -*-
import os
import xbmc
import xbmcaddon
import time
import requests
import xbmcgui
import xml.etree.ElementTree as ET
import hashlib

addon = xbmcaddon.Addon('script.beautify.estuary')

if addon.getSetting('vip') == 'true':
    from resources.lib.passlib.hash import md5_crypt

script_name = addon.getAddonInfo('name')
script_id = addon.getAddonInfo('id')

def log(msg, level='D'):
    if level == 'I':
        level = xbmc.LOGINFO
    elif level == 'N':
        level = xbmc.LOGNOTICE
    elif level == 'W':
        level = xbmc.LOGWARNING
    elif level == 'E':
        level = xbmc.LOGERROR
    else:
        level = xbmc.LOGDEBUG
    msg = '[EsBF-service]: ' + str(msg)
    xbmc.log(msg, level)


def notify(msg, timeout=7000):
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (script_name, msg, timeout, addon.getAddonInfo('icon')))
    log(msg, 'I')

# class WebshareAPI převzata od 
class WebshareAPI:
    def __init__(self):
        self._base_url = 'https://webshare.cz/api/'
        self._token = ''
        self.vipdays = ''
        self._username = addon.getSetting('username').strip()
        self._password = addon.getSetting('password').strip()
        self.login(self._username , self._password)
        self.vip_left()

    def login(self, user_name, password):
        """Logs {user_name} in Webshare API"""
        salt = self.get_salt(user_name)
        log(salt, 'I')
        headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        url = self._base_url + 'login/'
        password, digest = self.hash_password(user_name, password, salt)
        data = {
                'username_or_email' : user_name,
                'password' : password,
                'digest' : digest,
                'keep_logged_in' : 1
                }
        response = requests.post(url, data=data, headers=headers)
        assert(response.status_code == 200)
        root = ET.fromstring(response.content)
        assert root.find('status').text == 'OK', 'Return code was not OK, debug info: status: {}, code: {}, message: {}'.format(
                    root.find('status').text,
                    root.find('code').text,
                    root.find('message').text)

        self._token = root.find('token').text
        log('WS Login successfull', 'I')

    def hash_password(self, user_name, password, salt):
        """Creates password hash used by Webshare API"""
        password = hashlib.sha1(md5_crypt.encrypt(password, salt=salt).encode('utf-8')).hexdigest()
        digest = hashlib.md5((user_name + ':Webshare:' + password).encode('utf-8')).hexdigest()
        return password, digest

    def get_salt(self, user_name):
        """Retrieves salt for password hash from webshare.cz"""
        headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        url = self._base_url + 'salt/'
        data = {'username_or_email' : user_name}
        response = requests.post(url, data=data, headers=headers)
        assert(response.status_code == 200)
        root = ET.fromstring(response.content)
        assert root.find('status').text == 'OK', 'Return code was not OK, debug info: status: {}, code: {}, message: {}'.format(
                    root.find('status').text, 
                    root.find('code').text, 
                    root.find('message').text)
        return root.find('salt').text
    
    def vip_left(self):
        """Retrieves salt for password hash from webshare.cz"""
        headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        url = self._base_url + 'user_data/'
        data = {'wst' : self._token}
        response = requests.post(url, data=data, headers=headers)
        assert(response.status_code == 200)
        root = ET.fromstring(response.content)
        assert root.find('status').text == 'OK', 'Return code was not OK, debug info: status: {}, code: {}, message: {}'.format(
                    root.find('status').text, 
                    root.find('code').text, 
                    root.find('message').text)

        self.vipdays = root.find('vip_days').text
        log('Reamin WS VIP days: ' + self.vipdays)
    
    def show_vip_left(self):
        try:
            return int(self.vipdays)
        except:
            return self.vipdays



if __name__ == '__main__':
    monitor = xbmc.Monitor()

    while not monitor.abortRequested():
        curr_time_hour = time.localtime()[3]
        curr_time_minutes = time.localtime()[4]
        curr_time_seconds = time.localtime()[5]
        sleep_until_next_day = (((24 - curr_time_hour) * 60) - curr_time_minutes) * 60 + 5
        log('Start at ' + str(curr_time_hour) + ':' + str(curr_time_minutes) + ':' + str(curr_time_seconds))
        log('Next name day update: ' + str(sleep_until_next_day / 60) + ' minutes', 'I')
        # from urllib.request import Request, urlopen
        cal_url = 'https://svatky.vanio.cz/api/'
        headers = {'Accept': 'application/json'}
        response = requests.get(cal_url, headers=headers)
        data = response.json()
        """
        Odpověď serveru obsahuje tyto pole:
            date (string): Datum ve formátu yyyy-mm-dd
            month (array): Český název měsíce
            nominative (string): v prvním pádě
            genitive (string): ve druhém pádě
            dow (string): Český název dne v týdnu
            name (string): Jméno, které slaví svátek
            isPublicHoliday (boolean): Zda je dané datum státním svátkem
            holidayName (string): Pouze, pokud je dané datum státním svátkem, název státního svátku
            shopsClosed (boolean|string): Pouze, pokud je dané datum státním svátkem. Informace, zda jsou podle zákona zavřené obchody. V případě 24.12. je hodnota string ("po 12. hodině"), u ostatních svátků je hodnota boolean.

        https://www.xbmc-kodi.cz/prispevek-estuary-easy?page=26
        """
        log('Name day: ' + data['name'])
        log('isPublicHoliday: ' + str(data['isPublicHoliday']))
        win = xbmcgui.Window(10000)
        win.setProperty('calendar_nameDay', data['name'])
        if data['isPublicHoliday']:
            win.setProperty('calendar_isPublicHoliday', str(data['isPublicHoliday']))
            win.setProperty('calendar_holidayName', data['holidayName'])
            if data['shopsClosed']:
                win.setProperty('shops_closed', str(data['shopsClosed']))
        # Sleep/wait for abort
        if addon.getSetting('vip') == 'true':
            webshare = WebshareAPI()
            ws_days = webshare.show_vip_left()
            win.setProperty('ws.days', str(ws_days))
            try:
                if ws_days <= 30:
                    notify('Webshare VIP už pouze: ' + str(ws_days) + ' dní!', 30000)
            except:
                pass
        if monitor.waitForAbort(sleep_until_next_day):
            # Abort was requested while waiting. We should exit
            log('Exiting...')
            break
