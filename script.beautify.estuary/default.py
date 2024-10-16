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
import time

addon = xbmcaddon.Addon('script.beautify.estuary')
skin_addon = xbmcaddon.Addon('skin.estuary')
script_name = addon.getAddonInfo('name')
script_id = addon.getAddonInfo('id')
skin_version = skin_addon.getAddonInfo('version')
home = xbmcvfs.translatePath(addon.getAddonInfo('path'))
old_skin_folder = xbmcvfs.translatePath(skin_addon.getAddonInfo('path'))
new_skin_id = 'skin.estuary.bf'
skin_folder = home.replace(script_id, new_skin_id)
addon_data_folder = xbmcvfs.translatePath(addon.getAddonInfo('profile'))
#library_folder = os.path.join(addon_data_folder, 'library')
library_folder = os.path.join( xbmcvfs.translatePath('special://profile'), 'library', 'video')
# icon = os.path.join(home, 'icon.png')
positions = ['first', 'second', 'third', 'fourth', 'fiveth', 'sixth', 'seventh', 'eighth', 'nineth']
menu_options_name = []
menu_options_id = ['EsBFid1','EsBFid2','EsBFid3','EsBFid4','EsBFid5','EsBFid6','EsBFid7','EsBFid8','EsBFid9']
#menu_options_id = []
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
# Includes.xml
# TIME_IN_TOPBAR = "$INFO[System.Time]"
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
    # xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (script_name, msg.encode('utf-8'), timeout, addon.getAddonInfo('icon')))
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (script_name, msg, timeout, addon.getAddonInfo('icon')))
    log(msg, xbmc.LOGINFO)


def notifyAndOpenSettings(line1='Neúplné hodnoty v nastavení', line2='Změny nebudou provedeny', line3=''):
    global failsafe
    failsafe = True
    okdialog = xbmcgui.Dialog()
    okdialog.ok(script_name, line1 + '\n' + line2 + '\n' + line3)
    addon.openSettings()


def main():
    # notify('Button YES pressed')
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
            #menu_options_id.append(xbmcvfs.makeLegalFilename(addon.getSetting(name)))
        if addon.getSetting(icon) != '':
            num_menu_options_icon.append(int(addon.getSetting(icon)))
        if addon.getSetting(action).strip() != '':
            menu_options_action.append(addon.getSetting(action))
        else:
            menu_options_action.append('unset')
        if addon.getSetting(widget) == 'true':
            widgets_posters = {}
            for sub_pos in positions:
                widget_name = 'widget_' + pos + '_name_' + sub_pos
                widget_xml_node = 'widget_' + pos + '_node_name_' + sub_pos
                widget_xml_node_sort = 'widget_' + pos + '_node_sort_' + sub_pos
                if addon.getSetting(widget_name).strip() != '' and addon.getSetting(widget_xml_node).strip() != '':
                    widgets_posters[sub_pos] = dict(name=addon.getSetting(widget_name), path=addon.getSetting(widget_xml_node), sort=addon.getSetting(widget_xml_node_sort))
                elif bool(addon.getSetting(widget_name).strip() == '') ^ bool(addon.getSetting(widget_xml_node).strip() == ''):
                    notifyAndOpenSettings()
            widgets[pos] = widgets_posters
    log('Menu options name: ' + str(menu_options_name), 'D')
    log('Menu options icons: ' + str(menu_options_icon), 'D')
    log('Menu options actions: ' + str(menu_options_action), 'D')
    log('Widgets dic: ' + str(widgets), 'D')
    log('home folder var: ' + str(home), 'D')
    log('skin_version: ' + str(skin_version), 'D')
    log('script_id: ' + str(script_id), 'D')
    log('(NUM) Menu options icons: ' + str(num_menu_options_icon), 'D')

    if not failsafe:
        backup()
    else:
        notify('Změny NEBYLY provedeny!')


def backup():
    log('Skin folder: ' + str(skin_folder), 'D')
    if not os.path.exists(skin_folder):
        shutil.copytree(old_skin_folder, skin_folder)
        shutil.copy2(home + '/resources/icon.png', skin_folder + '/resources/')
    else:
        dialog = xbmcgui.Dialog()
        if dialog.yesno(script_name, 'Tato akce vymaže obsah složky skinu Beautify Estuary!' + '\n' + 'Veškeré změny, které nebyly provedeny přes nastavení tohoto scriptu budou ztraceny!' + '\n' + 'Pokračovat?'):
            shutil.rmtree(skin_folder)
            shutil.copytree(old_skin_folder, skin_folder)
            shutil.copy2(home + '/resources/icon.png', skin_folder + '/resources/')
        else:
            global failsafe
            failsafe = True

    if not failsafe:
        tree = ET.parse(skin_folder + '/addon.xml')
        root = tree.getroot()
        root.set('id', new_skin_id)
        root.set('name', script_name)
        tree.write(skin_folder + '/addon.xml')
        process()
    else:
        notify('Změny NEBYLY provedeny!')


def process():
    """
    #############################
    #### DialogButtonMenu.xml ###
    #############################
    """
    tree = ET.parse(skin_folder + '/xml/DialogButtonMenu.xml')
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
    tree.write(skin_folder + '/xml/DialogButtonMenu.xml')
    """
    #############################
    ######### Home.xml ##########
    #############################
    """
    # TODO: menu_system_functions
    tree = ET.parse(skin_folder + '/xml/Home.xml')
    root = tree.getroot()
    if menu_options_name:
        create_menu(root)
    if widgets:
        create_widgets(root)
    tree.write(skin_folder + '/xml/Home.xml')

    """
    #############################
    ##### Includes_Home.xml #####
    #############################
    """
    tree = ET.parse(skin_folder + '/xml/Includes_Home.xml')
    root = tree.getroot()
    root.append(ET.fromstring(nvars.widget_info_node_includes_home))
    tree.write(skin_folder + '/xml/Includes_Home.xml')

    """
    #############################
    ######## Includes.xml #######
    #############################
    """
    tree = ET.parse(skin_folder + '/xml/Includes.xml')
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
    tree.write(skin_folder + '/xml/Includes.xml')

    # Enable skin.estuary.bf
    xbmc.executeJSONRPC('{"id":1, "jsonrpc":"2.0", "method":"Addons.SetAddonEnabled", "params":{"addonid":"skin.estuary.bf", "enabled":True}')

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
    #return root


def create_widgets(root):
    base_widgetinfo = ET.fromstring(nvars.widget_info_node_home)
    for pos in range(0, len(widgets)):
        int_id = int(num_id[pos])
        grouplist_id = str(int_id + 1)
        base = nvars.movie_widget_base.replace('REPLACE_NUM', num_id[pos])
        base = base.replace('REPLACE_GROUP_NUM', grouplist_id)
        #base = base.replace('REPLACE_LIBRARY_PATH',  library_folder)
        base = base.replace('REPLACE_ID',  menu_options_id[pos])
        if addon.getSetting('widget_' + positions[pos] + '_category') == 'true':
            category_id = str(int_id + 10)
            category = nvars.movie_widget_category.replace('REPLACE_CAT_NUM', category_id)
            #category = category.replace('REPLACE_LIBRARY_PATH',  library_folder)
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
            #poster = poster.replace('REPLACE_LIBRARY_PATH',  library_folder)
            poster = poster.replace('REPLACE_ID', menu_options_id[pos])
            poster = poster.replace('REPLACE_XML_PATH', widgets[positions[pos]][positions[subpos]]['path'])
            poster = poster.replace('REPLACE_HEADER', widgets[positions[pos]][positions[subpos]]['name'])
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
            poster = ET.fromstring(poster)
            base.find('*/[@type="grouplist"]').append(poster)
        root.find(XPATH_WIDGET).append(base)
    root.find(XPATH_WIDGETINFO).insert(3, base_widgetinfo)
    #return root


if (__name__ == '__main__'):
    dialog = xbmcgui.Dialog()
    if dialog.yesno(script_name, 'Provést změny skinu dle nastavení?'):
        main()
        time.sleep(2)
        xbmc.executebuiltin('ReloadSkin()')
        current_skin = xbmc.executeJSONRPC('{"id":1, "jsonrpc":"2.0", "method":"Settings.GetSkinSettings"}')
        if current_skin['result']['skin'] != 'skin.estuary.bf':
            xbmcgui.Dialog().ok(script_name, 'Aktivujte nový skin (Doplňky - Vzhled a chování - Vzhled)!')