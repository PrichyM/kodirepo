# -*- coding: utf-8 -*-
import os
import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs
import shutil
import xml.etree.ElementTree as ET
import random
import resources.lib.node_vars as nvars
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
menu_options_id = ['EsBFid1','EsBFid2','EsBFid3','EsBFid4','EsBFid5','EsBFid6','EsBFid7','EsBFid8','EsBFid9']
menu_options_icon = nvars.icons_from_settings.replace('\n', '').split(',')
num_id = []

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


def notifyAndOpenSettings(line1='Neúplné hodnoty v nastavení', line2='Změny nebudou provedeny', line3='', open_settings=True):
    okdialog = xbmcgui.Dialog()
    okdialog.ok(addon_name, line1 + '\n' + line2 + '\n' + line3)
    if open_settings:
        addon.openSettings()

def createID():
    x = random.randrange(57000, 100000, 1000)
    if x not in num_id:
        num_id.append(x)
        return str(x)
    else:
        createID()

def main():
    ''' 
    Fresh start - copy original Estuary skin and create skin.estuary.bf
                - backup advancedsettings.xml
    '''
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
            notify('Změny NEBYLY provedeny!')
            return
    
    # creating skin.estuary.bf
    tree = ET.parse(new_skin_folder + '/addon.xml')
    root = tree.getroot()
    root.set('id', new_skin_id)
    root.set('name', addon_name)
    tree.write(new_skin_folder + '/addon.xml')
    
    # advancedsettings.xml backup
    if addon.getSetting('advancedsettings') == 'true':
        if not os.path.exists(advancedsettings_file):
            # create basic advancedsettings.xml with no additional settings
            root = ET.Element('advancedsettings')
            ET.ElementTree(root).write(advancedsettings_file)
        # backup
        shutil.copy2(advancedsettings_file, os.path.join(xbmcvfs.translatePath(addon_data_folder), 'advancedsettings.xml.bak'))
        # apply required settings
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
    
    # Enable skin.estuary.bf
    xbmc.executeJSONRPC('{"id":1, "jsonrpc":"2.0", "method":"Addons.SetAddonEnabled", "params":{"addonid":"%s", "enabled":True}' % new_skin_id)
    
    ''' 
    Create Custom menu items and poster widgets in Home.xml
    '''
    
    #############################
    ######### Home.xml ##########
    #############################
    tree = ET.parse(new_skin_folder + '/xml/Home.xml')
    root = tree.getroot()

    if addon.getSetting('top_menu') == 'true':
        top_menu = ET.fromstring(nvars.top_menu)
        root.find(XPATH_TOP_MENU).remove(root.find(XPATH_TOP_MENU_REMOVE))
        root.find(XPATH_TOP_MENU).append(top_menu)
    
    menu_items = addon.getSettings().getInt('menu_nums')
    #if menu_items == 0:
    #    return

    widgetinfo_base = ET.fromstring(nvars.widget_info_node_home)
    int_pos = 0
    for pos in positions[:menu_items]:
        widget = 'widget_%s' % pos
        menu_id_folder = os.path.join(library_folder, menu_options_id[int_pos])
        # create library folders (can be used for category widget)
        if not os.path.exists(menu_id_folder):
            xbmcvfs.mkdirs(menu_id_folder)
        '''
        Create MENU
        '''
        num = createID()
        menu_base = nvars.menu.replace('REPLACE_ID', menu_options_id[int_pos])
        menu_base = menu_base.replace('REPLACE_POS', pos)
        menu_base = menu_base.replace('REPLACE_NUM', '$NUMBER[%s]' % num)
        root.find(XPATH_MENU).insert(int_pos, ET.fromstring(menu_base))

        if addon.getSetting(widget) == 'true':
            '''
            Create WIDGET
            '''
            grouplist_id = str(int(num) + 1)
            widget_base = nvars.movie_widget_base.replace('REPLACE_NUM', str(num))
            widget_base = widget_base.replace('REPLACE_GROUP_NUM', grouplist_id)
            widget_base = widget_base.replace('REPLACE_ID',  menu_options_id[int_pos])
            widget_base = ET.fromstring(widget_base)
            if addon.getSetting('widget_%s_category' % pos) == 'true':
                '''
                Show CATEGORIES in the widget
                '''
                category_id = str(int(num) + 10)
                category = nvars.movie_widget_category.replace('REPLACE_CAT_NUM', category_id)
                category = category.replace('REPLACE_ID', menu_options_id[int_pos])
                category = ET.fromstring(category)
                widget_base.find('*/[@type="grouplist"]').append(category)
            for sub_pos in positions[:addon.getSettings().getInt(widget + '_nums')]:
                '''
                Create POSTERS for the widget and INFOPANEL with picture and plot
                '''
                num = int(num) + 100
                widgetinfo = nvars.widget_info_node_home_append.replace('REPLACE_POSTER_NUM', str(num))
                widgetinfo = ET.fromstring(widgetinfo)
                widgetinfo_base.append(widgetinfo)
                widgetinfo_base.find('visible').text += '| Control.HasFocus(%d)' % num
                poster = nvars.movie_widget_poster.replace('REPLACE_POSTER_NUM', str(num))
                poster = poster.replace('REPLACE_ID', menu_options_id[int_pos])
                # Poster Label and Path are stored as Skin.String and can by loaded dynamically from addon settings
                poster = poster.replace('REPLACE_XML_PATH', 'widget_%s_poster_%s.List' % (pos, sub_pos))
                poster = poster.replace('REPLACE_HEADER', 'widget_%s_poster_%s.Label' % (pos, sub_pos))
                poster_sort = addon.getSetting('widget_%s_node_sort_%s' % (pos, sub_pos))
                if poster_sort == '0':
                    sort = 'rating'
                elif poster_sort == '2':
                    sort = 'lastplayed'
                else:
                    # default
                    sort = 'dateAdded'
                poster = poster.replace('REPLACE_SORT', sort)
                poster = ET.fromstring(poster)
                widget_base.find('*/[@type="grouplist"]').append(poster)
            root.find(XPATH_WIDGET).append(widget_base)
        int_pos += 1
    root.find(XPATH_WIDGETINFO).insert(3, widgetinfo_base)
    tree.write(new_skin_folder + '/xml/Home.xml')

    ''' 
    Make changes in other XML files 
    '''          

    #############################
    #### DialogButtonMenu.xml ###
    #############################
    
    # TODO: rewrite, so menu Labels and Actions are stored as Skin.Strings or Window Property and change settings from hardcoded bools to custom strings
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

    
    #############################
    ##### Includes_Home.xml #####
    #############################
    
    tree = ET.parse(new_skin_folder + '/xml/Includes_Home.xml')
    root = tree.getroot()
    root.append(ET.fromstring(nvars.widget_info_node_includes_home))
    tree.write(new_skin_folder + '/xml/Includes_Home.xml')

    
    #############################
    ######## Includes.xml #######
    #############################
    
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
    # HOW MANY WS VIP DAYS GET LEFT
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


def create_settings():
    menu_items = addon.getSettings().getInt('menu_nums')
    # No custom menu, nothing to create
    if menu_items == 0:
        return
    tree = ET.parse(os.path.join(addon_main_folder_path, 'resources', 'settings.xml'))
    root = tree.getroot()
    visible_condition = 0
    # create skin menu item constructors for each menu category in settings
        # - name; icon; addon (action after click)
        # + widget & widget category bools
    # create poster constructors for each menu category in settings 
        # - generate button; sorting method
    for pos in positions[:menu_items]:
        # number of 'group' nodes that are children of node with id="widget_POS_category_node"
        already_existed_groups = len(root.findall('.//*[@id="widget_' + pos + '_category_node"]/group'))
        log('already_existed_groups for (' + pos + ') : ' + str(already_existed_groups), 'I')

        ### create poster constructors
        # get number of required posters for this menu item
        poster_items = addon.getSettings().getInt('widget_' + pos + '_nums')
        # set proper group_id and group_label
        group_id = 2 if already_existed_groups <= 1 else already_existed_groups + 1
        group_label = 30111 if already_existed_groups <= 1 else 30111 + already_existed_groups - 1
        poster_list = []
        # TODO: Remove posters and 
        # process only newly added posters
        start_pos = 0 if already_existed_groups <= 1 else already_existed_groups-1
        sub_visible_condition = start_pos
        for subpos in positions[start_pos:poster_items]:
            node_settings_menu_poster = nvars.settings_menu_poster.replace('REPLACE_ID', pos)
            node_settings_menu_poster = node_settings_menu_poster.replace('REPLACE_SUBID', subpos)
            node_settings_menu_poster = node_settings_menu_poster.replace('REPLACE_GROUP_ID', str(group_id))
            node_settings_menu_poster = node_settings_menu_poster.replace('REPLACE_GROUP_LABEL', str(group_label))
            node_settings_menu_poster = node_settings_menu_poster.replace('REPLACE_VISIBLE_CONDITION', str(sub_visible_condition))
            node_settings_menu_poster = ET.fromstring(node_settings_menu_poster)
            # append each poster node to list, so it can be inserted all at once
            poster_list.append(node_settings_menu_poster)
            group_id += 1
            group_label += 1
            sub_visible_condition += 1
        # append all poster constructor nodes
        root.find('.//*[@id="widget_' + pos + '_category_node"]').extend(poster_list)
        
        ### create skin menu item constructors
        # if already_existed_groups > 0, then menu constructor already exists
        if already_existed_groups != 0:
            visible_condition += 1
            continue
        node_settings_menu = nvars.settings_menu.replace('REPLACE_ID', pos)
        node_settings_menu = node_settings_menu.replace('REPLACE_VISIBLE_CONDITION', str(visible_condition))
        node_settings_menu = ET.fromstring(node_settings_menu)
        visible_condition += 1
        # insert skin menu constructor node on top of setting category
        root.find('.//*[@id="widget_' + pos + '_category_node"]').insert(0, node_settings_menu)

    notifyAndOpenSettings(line1='Menu nastavení bylo vygenerováno!', line2='', line3='Nyní můžete pokračovat v nastavení.', open_settings=False)
    
    tree.write(os.path.join(addon_main_folder_path, 'resources', 'settings.xml'))

def create_skin_strings():
    for pos in positions:
        name = 'menu_%s_name' % pos
        icon = 'menu_%s_icon' % pos
        action = 'menu_%s_addon' % pos
        xbmc.executebuiltin('Skin.SetString(%s,%s)' % (name, addon.getSetting(name),))
        xbmc.executebuiltin('Skin.SetString(%s,%s)' % (icon, menu_options_icon[int(addon.getSetting(icon))],))
        xbmc.executebuiltin('Skin.SetString(%s,%s)' % (action, addon.getSetting(action),))
    notify('Menu updated')
        #xbmc.executebuiltin('Skin.Reset(%s)' % name)
    '''
    WINDOW = xbmcgui.Window(10000)
    WINDOW.setProperty('favourite.%d.path' % (count + 1,) , path)
    WINDOW.clearProperty('favourite.%d.path' % (idx_count))
    WINDOW.getProperty('favourite.count')
    '''

def parse_argv(params):
        try:
            params = dict(arg.split('=') for arg in params[1].split('&'))
        except:
            return
        log('params: %s' % params, 'D')
        if params.get('action', '') == 'create_settings':
            create_settings()
        elif params.get('action', '') == 'create_skin_strings':
            create_skin_strings()
    
if (__name__ == '__main__'):
    if len(sys.argv) > 1:
        parse_argv(sys.argv)
    else:
        dialog = xbmcgui.Dialog()
        if dialog.yesno(addon_name, 'Provést změny skinu dle nastavení?'):
            main()
            xbmc.executebuiltin('ReloadSkin()')
            current_skin = json.loads(xbmc.executeJSONRPC('{"id":1, "jsonrpc":"2.0", "method":"Settings.GetSkinSettings"}'))
            if current_skin['result']['skin'] != new_skin_id:
                xbmcgui.Dialog().ok(addon_name, 'Aktivujte nový skin (Doplňky - Vzhled a chování - Vzhled)!')