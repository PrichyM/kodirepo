# -*- coding: utf-8 -*-
import os
import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs
import shutil
import xml.etree.ElementTree as ET
import random
import node_vars as nvars
import json
import sys


addon = xbmcaddon.Addon('script.beautify.estuary')
addon_name = addon.getAddonInfo('name')
addon_id = addon.getAddonInfo('id')
addon_main_folder_path = xbmcvfs.translatePath(addon.getAddonInfo('path'))
addon_data_folder = xbmcvfs.translatePath(addon.getAddonInfo('profile'))

old_skin_addon = xbmcaddon.Addon('skin.estuary')
old_skin_version = old_skin_addon.getAddonInfo('version')
old_skin_folder = xbmcvfs.translatePath(old_skin_addon.getAddonInfo('path'))
old_skin_data_folder = xbmcvfs.translatePath(old_skin_addon.getAddonInfo('profile'))

new_skin_id = 'skin.estuary.bf'
new_skin_folder = addon_main_folder_path.replace(addon_id, new_skin_id)
new_skin_data_folder = addon_data_folder.replace(addon_id, new_skin_id)

library_folder = os.path.join(xbmcvfs.translatePath('special://profile'), 'library', 'video')
advancedsettings_file = os.path.join(xbmcvfs.translatePath('special://masterprofile'), 'advancedsettings.xml')
# icon = os.path.join(addon_main_folder_path, 'icon.png')

positions = ['first', 'second', 'third', 'fourth', 'fiveth', 'sixth', 'seventh', 'eighth', 'nineth']
menu_options_name = []
menu_options_id = ['EsBFid1','EsBFid2','EsBFid3','EsBFid4','EsBFid5','EsBFid6','EsBFid7','EsBFid8','EsBFid9']
num_menu_options_icon = []
menu_options_icon = nvars.icons_from_settings.replace('\n', '').split(',')
menu_options_action = []

widgets = {}
num_id = []

failsafe = False

# Home.xml
XPATH_WIDGET = "./controls/control/control[@id='2000']"
XPATH_MENU = "./controls/control[4]/control[2]/control[1]/content"
XPATH_WIDGETINFO = './controls/control[4]'
XPATH_TOP_MENU = './controls/control[4]/control[2]'
XPATH_TOP_MENU_REMOVE = './/*[@id="700"]'

# Includes.xml
TIME_IN_TOPBAR = "[B]$INFO[System.Time(hh)][COLOR red]:[/COLOR]$INFO[System.Time(mm)][/B]"
TIME_IN_TOPBAR_calname_part = "$INFO[Window(Home).Property(calendar_nameDay),, ]"
TIME_IN_TOPBAR_date_part = "[CR]$INFO[System.Date(d. MMM)] [COLOR red]$INFO[System.Date(DDD)][/COLOR]"
XPATH_TOPBAR = "*/[@name='TopBar']"
XPATH_RATING = "./include[@name='UserRatingContent']"
XPATH_TIME_IN_TOPBAR = "*/[@name='TopBar']/definition/control[@type='group']/control[6]/control[3]/label"
XPATH_TIME_IN_TOPBAR_FONT = "*/[@name='TopBar']/definition/control[@type='group']/control[6]/control[3]/font"
XPATH_WATCHING_FINISH_TIME = "./include[@name='MediaFlags']/definition/control[@type='grouplist']"

# DialogButtonMenu.xml
XPATH_QUIT_MENU = './controls/control/control/content'


def log(msg, level):
    if level == 'D':
        level = xbmc.LOGDEBUG
    elif level == 'I':
        level = xbmc.LOGINFO
    elif level == 'N':
        level = xbmc.LOGNOTICE
    elif level == 'W':
        level = xbmc.LOGWARNING
    elif level == 'E':
        level = xbmc.LOGERROR
    msg = '[EsBF]: ' + str(msg)
    xbmc.log(msg, level)

def notify(msg, timeout=7000):
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (addon_name, msg, timeout, addon.getAddonInfo('icon')))
    log(msg, xbmc.LOGINFO)


def notifyAndOpenSettings(line1='Neúplné hodnoty v nastavení', line2='Změny nebudou provedeny', line3=''):
    global failsafe
    failsafe = True
    okdialog = xbmcgui.Dialog()
    okdialog.ok(addon_name, line1 + '\n' + line2 + '\n' + line3)
    addon.openSettings()


def main():
    menu_items = addon.getSettings().getInt('menu_nums')
    if menu_items == 0:
        backup()
        return
    
    for pos in positions[:menu_items]:
        name = 'menu_' + pos + '_name'
        icon = 'menu_' + pos + '_icon'
        action = 'menu_' + pos + '_addon'
        widget = 'widget_' + pos
        if addon.getSetting(name).strip() != '':
            menu_options_name.append(addon.getSetting(name))
        if addon.getSetting(icon) != '':
            num_menu_options_icon.append(int(addon.getSetting(icon)))
        if addon.getSetting(action).strip() != '':
            menu_options_action.append(addon.getSetting(action))
        else:
            menu_options_action.append('unset')
        if addon.getSetting(widget) == 'true':
            widgets_posters = {}
            for sub_pos in positions[:addon.getSettings().getInt(widget + '_nums')]:
                poster_base = widget + '_poster_' + sub_pos
                poster_name = poster_base + '.Label'
                poster_name = xbmc.getInfoLabel('Skin.String(' + poster_name + ')')
                poster_path = poster_base + '.List'
                poster_path = xbmc.getInfoLabel('Skin.String(' + poster_path + ')')
                poster_xml_node_sort = 'widget_' + pos + '_node_sort_' + sub_pos
                widgets_posters[sub_pos] = dict(name=poster_name, path=poster_path, sort=addon.getSetting(poster_xml_node_sort))
                '''
                if widget_name.strip() != '':
                    widgets_posters[sub_pos] = dict(name=widget_name, path=widget_path, sort=addon.getSetting(widget_xml_node_sort))
                else:
                    notifyAndOpenSettings()
                '''
            widgets[pos] = widgets_posters
    log('Menu options name: ' + str(menu_options_name), 'D')
    log('Menu options icons: ' + str(menu_options_icon), 'D')
    log('Menu options actions: ' + str(menu_options_action), 'D')
    log('Widgets dic: ' + str(widgets), 'D')

    if not failsafe:
        backup()
    else:
        notify('Změny NEBYLY provedeny!')


def backup():
    log('Skin folder: ' + str(new_skin_folder), 'D')
    if not os.path.exists(new_skin_folder):
        shutil.copytree(old_skin_folder, new_skin_folder)
        shutil.copy2(addon_main_folder_path + '/resources/icon.png', new_skin_folder + '/resources/')
        shutil.copytree(old_skin_data_folder, new_skin_data_folder)
    else:
        dialog = xbmcgui.Dialog()
        if dialog.yesno(addon_name, 'Tato akce vymaže obsah složky skinu Beautify Estuary!' + '\n' + 'Veškeré změny, které nebyly provedeny přes nastavení tohoto scriptu budou ztraceny!' + '\n' + 'Pokračovat?'):
            shutil.rmtree(new_skin_folder)
            shutil.copytree(old_skin_folder, new_skin_folder)
            shutil.copy2(addon_main_folder_path + '/resources/icon.png', new_skin_folder + '/resources/')
        else:
            global failsafe
            failsafe = True

    if not failsafe:
        tree = ET.parse(new_skin_folder + '/addon.xml')
        root = tree.getroot()
        root.set('id', new_skin_id)
        root.set('name', addon_name)
        tree.write(new_skin_folder + '/addon.xml')
        if addon.getSetting('advancedsettings') == 'true':
            if not os.path.exists(advancedsettings_file):
                root = ET.Element('advancedsettings')
                ET.ElementTree(root).write(advancedsettings_file)
            shutil.copy2(advancedsettings_file, os.path.join(xbmcvfs.translatePath(addon_data_folder), 'advancedsettings.xml.bak'))
        process()
    else:
        notify('Změny NEBYLY provedeny!')


def process():
    """
    #############################
    #### DialogButtonMenu.xml ###
    #############################
    """
    tree = ET.parse(new_skin_folder + '/xml/DialogButtonMenu.xml')
    root = tree.getroot()
    if addon.getSetting('skin_reload') == 'true':
        reload_skin = ET.fromstring(nvars.reload_skin)
        root.find(XPATH_QUIT_MENU).append(reload_skin)
    if addon.getSetting('debug_toggle_skin') == 'true':
        debug_skin = ET.fromstring(nvars.debug_toggle_skin)
        root.find(XPATH_QUIT_MENU).append(debug_skin)
    if addon.getSetting('debug_toggle') == 'true':
        debug_toggle = ET.fromstring(nvars.debug_toggle)
        root.find(XPATH_QUIT_MENU).append(debug_toggle)
    tree.write(new_skin_folder + '/xml/DialogButtonMenu.xml')
    """
    #############################
    ######### Home.xml ##########
    #############################
    """
    tree = ET.parse(new_skin_folder + '/xml/Home.xml')
    root = tree.getroot()
    if menu_options_name:
        create_menu(root)
    if widgets:
        create_widgets(root)
    if addon.getSetting('top_menu') == 'true':
        top_menu = ET.fromstring(nvars.top_menu)
        root.find(XPATH_TOP_MENU).remove(root.find(XPATH_TOP_MENU_REMOVE))
        root.find(XPATH_TOP_MENU).append(top_menu)
    tree.write(new_skin_folder + '/xml/Home.xml')

    """
    #############################
    ##### Includes_Home.xml #####
    #############################
    """
    tree = ET.parse(new_skin_folder + '/xml/Includes_Home.xml')
    root = tree.getroot()
    root.append(ET.fromstring(nvars.widget_info_node_includes_home))
    tree.write(new_skin_folder + '/xml/Includes_Home.xml')

    """
    #############################
    ######## Includes.xml #######
    #############################
    """
    tree = ET.parse(new_skin_folder + '/xml/Includes.xml')
    root = tree.getroot()
    # NAME DAY AND DATE IN TOPBAR - instead of only time
    if addon.getSetting('calendar_nameDay') == 'true' or addon.getSetting('date') == 'true':
        global TIME_IN_TOPBAR
        if addon.getSetting('calendar_nameDay') == 'true':
            TIME_IN_TOPBAR += ' ' + TIME_IN_TOPBAR_calname_part
        if addon.getSetting('date') == 'true':
            TIME_IN_TOPBAR += TIME_IN_TOPBAR_date_part
        root.find(XPATH_TIME_IN_TOPBAR).text = TIME_IN_TOPBAR
        root.find(XPATH_TIME_IN_TOPBAR_FONT).text = "font14"
    # HOW MANY VIP DAYS GET LEFT
    if addon.getSetting('vip') == 'true':
        webshare_vip = nvars.vip_days_node.replace('REPLACE_COLOR', addon.getSetting('vip_color'))
        webshare_vip = webshare_vip.replace('REPLACE_FONT', addon.getSetting('vip_font'))
        webshare_vip = ET.fromstring(webshare_vip)
        root.find(XPATH_TOPBAR + 'definition/control').append(webshare_vip)

    # WATCHING FINISH TIME
    if addon.getSetting('wft') == 'true':
        wft_node = ET.fromstring(nvars.time_finish_watching_node)
        root.find(XPATH_WATCHING_FINISH_TIME).append(wft_node)
    if addon.getSetting('rating').strip() != '':
        root.find(XPATH_RATING + '/control[1]/width').text = addon.getSetting('rating').strip()
        root.find(XPATH_RATING + '/control[1]/height').text = addon.getSetting('rating').strip()
        root.find(XPATH_RATING + '/control[2]/width').text = addon.getSetting('rating').strip()
        root.find(XPATH_RATING + '/control[2]/height').text = addon.getSetting('rating').strip()
    if addon.getSetting('rating_color').strip() != '':
        root.find(XPATH_RATING + '/control[1]/texture').set('colordiffuse', addon.getSetting('rating_color'))
    if addon.getSetting('rating_font').strip() != '':
        root.find(XPATH_RATING + '/control[2]/font').text = addon.getSetting('rating_font').strip()
    tree.write(new_skin_folder + '/xml/Includes.xml')

    # Enable skin.estuary.bf
    xbmc.executeJSONRPC('{"id":1, "jsonrpc":"2.0", "method":"Addons.SetAddonEnabled", "params":{"addonid":"' + new_skin_id + '", "enabled":True}')
    
    if addon.getSetting('advancedsettings') == 'true':
        tree = ET.parse(advancedsettings_file)
        root = tree.getroot()
        video_el = root.find('video')
        if video_el is None:
            # video tag missing -> create video and subsdelayrange tags 
            video_el = ET.SubElement(root, 'video')
            ET.SubElement(video_el, 'subsdelayrange').text = addon.getSetting('ads_subsdelay')
        else:
            subsdelayrange_el = video_el.find('subsdelayrange')
            if subsdelayrange_el is None:
                # subsdelayrange tag missing -> create subsdelayrange tag 
                ET.SubElement(video_el, 'subsdelayrange').text = addon.getSetting('ads_subsdelay')
            else:
                # all tags found -> change value 
                subsdelayrange_el.text = addon.getSetting('ads_subsdelay')
        ET.indent(root)
        ET.ElementTree(root).write(advancedsettings_file)

def createID():
    x = random.randrange(57000, 100000, 1000)
    if x not in num_id:
        return str(x)
    else:
        createID()


def create_menu(root):
    for pos in range(0, len(menu_options_name)):
        menu_id_folder = os.path.join(library_folder, menu_options_id[pos])
        if not os.path.exists(menu_id_folder):
            xbmcvfs.mkdirs(menu_id_folder)
        num = createID()
        num_id.append(num)
        num = '$NUMBER[' + num + ']'
        base = nvars.menu.replace('REPLACE_NAME', menu_options_name[pos])
        base = base.replace('REPLACE_NUM', num)
        base = base.replace('REPLACE_ID', menu_options_id[pos])
        base = base.replace('REPLACE_ICON', menu_options_icon[num_menu_options_icon[pos]])
        if menu_options_action[pos] != 'unset':
            base = base.replace('REPLACE_ACTION', 'RunAddon(' + menu_options_action[pos] + ')')
        else:
            base = base.replace('REPLACE_ACTION', '')
        root.find(XPATH_MENU).insert(pos, ET.fromstring(base))


def create_widgets(root):
    base_widgetinfo = ET.fromstring(nvars.widget_info_node_home)
    for pos in range(0, len(widgets)):
        int_id = int(num_id[pos])
        grouplist_id = str(int_id + 1)
        base = nvars.movie_widget_base.replace('REPLACE_NUM', num_id[pos])
        base = base.replace('REPLACE_GROUP_NUM', grouplist_id)
        base = base.replace('REPLACE_ID',  menu_options_id[pos])
        if addon.getSetting('widget_' + positions[pos] + '_category') == 'true':
            category_id = str(int_id + 10)
            category = nvars.movie_widget_category.replace('REPLACE_CAT_NUM', category_id)
            category = category.replace('REPLACE_ID', menu_options_id[pos])
            base = ET.fromstring(base)
            category = ET.fromstring(category)
            base.find('*/[@type="grouplist"]').append(category)
        else:
            base = ET.fromstring(base)
        posters_limit = addon.getSetting('widget_' + positions[pos] + '_nums')
        for subpos in range(0, int(posters_limit)):
            int_id += 100
            widgetinfo = nvars.widget_info_node_home_append.replace('REPLACE_POSTER_NUM', str(int_id))
            widgetinfo = ET.fromstring(widgetinfo)
            base_widgetinfo.append(widgetinfo)
            base_widgetinfo.find('visible').text += '| Control.HasFocus(' + str(int_id) + ')'
            poster = nvars.movie_widget_poster.replace('REPLACE_POSTER_NUM', str(int_id))
            poster = poster.replace('REPLACE_ID', menu_options_id[pos])
            poster = poster.replace('REPLACE_XML_PATH', 'widget_' + positions[pos] + '_poster_' + positions[subpos] + '.List')
            poster = poster.replace('REPLACE_HEADER', 'widget_' + positions[pos] + '_poster_' + positions[subpos] + '.Label')
            sort = 'widget_' + positions[pos] + '_node_sort_' + positions[subpos]
            if widgets[positions[pos]][positions[subpos]]['sort'] == '0':
                sort = 'rating'
            elif widgets[positions[pos]][positions[subpos]]['sort'] == '2':
                sort = 'lastplayed'
            else:
                # default
                sort = 'dateAdded'
            poster = poster.replace('REPLACE_SORT', sort)
            log('REPLACE_SORT: ' + str(sort), 'D')
            log('FOR: ' + str(widgets[positions[pos]][positions[subpos]]), 'D')
            log('poster: ' + str(poster), 'D')
            poster = ET.fromstring(poster)
            base.find('*/[@type="grouplist"]').append(poster)
        root.find(XPATH_WIDGET).append(base)
    root.find(XPATH_WIDGETINFO).insert(3, base_widgetinfo)

def create_settings():
    menu_items = addon.getSettings().getInt('menu_nums')
    if menu_items == 0:
        return  
    tree = ET.parse(os.path.join(addon_main_folder_path, 'resources', 'settings.xml'))
    root = tree.getroot()
    
    for pos in positions[:menu_items]:
        widget = 'widget_' + pos
    
    tree.write(os.path.join(addon_main_folder_path, 'resources', 'settings.xml'))

def _parse_argv(params):
        try:
            params = dict(arg.split('=') for arg in params[1].split('&'))
        except:
            return
        log('params: %s' % params)
        if params.get('action', '') == 'create_settings':
            create_settings()
    
if (__name__ == '__main__'):
    if len(sys.argv) > 1:
        _parse_argv(sys.argv)
        sys.exit()

    dialog = xbmcgui.Dialog()
    if dialog.yesno(addon_name, 'Provést změny skinu dle nastavení?'):
        main()
        xbmc.executebuiltin('ReloadSkin()')
        current_skin = json.loads(xbmc.executeJSONRPC('{"id":1, "jsonrpc":"2.0", "method":"Settings.GetSkinSettings"}'))
        if current_skin['result']['skin'] != new_skin_id:
            xbmcgui.Dialog().ok(addon_name, 'Aktivujte nový skin (Doplňky - Vzhled a chování - Vzhled)!')