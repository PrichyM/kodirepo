# -*- coding: utf-8 -*-
"""
#############################
#### DialogButtonMenu.xml ###
#############################
"""
reload_skin = """
<item>
    <label>Reload skin</label>
	<onclick>ReloadSkin()</onclick>
</item>
"""
debug_toggle_skin = """
<item>
    <label>Skin debug toggle</label>
	<onclick>Skin.ToggleDebug()</onclick>
</item>
"""
debug_toggle = """
<item>
    <label>Debug toggle</label>
	<onclick>ToggleDebug()</onclick>
</item>
"""
"""
#############################
######## Includes.xml #######
#############################
"""
# HOW MANY VIP DAYS GET LEFT
vip_days_node = """
    <control type="group">
		<visible>Window.IsActive(home)</visible>
		<left>85</left>
		<top>60</top>
		<align>center</align>
		<aligny>center</aligny>
		<aspectratio>keep</aspectratio>
		<control type="image">
			<width>70</width>
			<height>70</height>
			<texture colordiffuse="REPLACE_COLOR">buttons/roundbutton-fo.png</texture>
		</control>
		<control type="label">
			<width>44</width>
			<height>44</height>
			<top>12</top>
			<left>12</left>
			<align>center</align>
			<aligny>center</aligny>
			<font>REPLACE_FONT</font>
			<label>$INFO[Window(Home).Property(ws.days)]</label>
		</control>
	</control>
"""
time_finish_watching_node = """
<control type="group">
    <width>115</width>
    <visible>!String.IsEmpty(ListItem.Duration) + !String.IsEmpty(ListItem.EndTimeResume)</visible>
    <control type="image">
        <top>20</top>
        <left>10</left>
        <width>20</width>
        <height>20</height>
        <fadetime>0</fadetime>
        <aspectratio aligny="center" align="center">keep</aspectratio>
        <texture>icons/pvr/pvr-hastimer.png</texture>
    </control>
    <control type="label">
        <left>20</left>
        <width>95</width>
        <height>60</height>
        <align>center</align>
        <aligny>center</aligny>
        <label>$INFO[ListItem.EndTimeResume]</label>
        <font>font_flag</font>
    </control>
    <include content="MediaFlag">
        <param name="texture" value="flags/flag.png" />
    </include>
</control>
"""
"""
#############################
##### Includes_Home.xml #####
#############################
"""
# append to root
widget_info_node_includes_home = """
  <include name="WidgetInfo">
        <param name="episode">false</param>
        <definition>
            <control type="grouplist">
                <left>10</left>
                <top>100</top>
                <bottom>40</bottom>
                <visible>Control.HasFocus($PARAM[container_id])</visible>
                <control type="textbox">
                    <height>100</height>
                    <width>442</width>
                    <aligny>center</aligny>
                    <scroll>true</scroll>
                    <font>font36_title</font>
                    <label>$INFO[Container($PARAM[container_id]).ListItem.Label]</label>
                    <shadowcolor>text_shadow</shadowcolor>
                    <autoscroll delay="5000" time="1500" repeat="5000">Skin.HasSetting(autoscroll)</autoscroll>
                    <visible>!$PARAM[episode]</visible>
                </control>
                <control type="textbox">
                    <height>100</height>
                    <width>442</width>
                    <aligny>center</aligny>
                    <font>font36_title</font>
                    <label>$INFO[Container($PARAM[container_id]).ListItem.TVShowTitle] $INFO[Container($PARAM[container_id]).ListItem.Label]</label>
                    <shadowcolor>text_shadow</shadowcolor>
                    <autoscroll delay="5000" time="1500" repeat="5000">Skin.HasSetting(autoscroll)</autoscroll>
                    <visible>$PARAM[episode]</visible>
                </control>
                <control type="label">
                    <height>50</height>
                    <width>442</width>
                    <aligny>center</aligny>
                    <font>font27</font>
                    <!-- <label color="grey">($INFO[Container($PARAM[container_id]).ListItem.Year])</label> -->
                    <label color="button_focus">$INFO[Container($PARAM[container_id]).ListItem.Genre]</label>
                    <!-- <shadowcolor>text_shadow</shadowcolor> -->
                    <visible>!String.IsEmpty(Container($PARAM[container_id]).ListItem.Genre) + !Container($PARAM[container_id]).ListItem.IsCollection</visible>
                </control>
                <control type="image">
                    <height>320</height>
                    <width>442</width>
                    <aspectratio aligny="center" align="left">keep</aspectratio>
                    <texture background="true">$INFO[Container($PARAM[container_id]).ListItem.Art(fanart)]</texture>
                    <visible>!String.IsEmpty(Container($PARAM[container_id]).ListItem.Art(fanart))</visible>
                </control>
                <control type="textbox">
                    <height>450</height>
                    <width>442</width>
                    <label>$INFO[Container($PARAM[container_id]).ListItem.Tagline,[I],[/I][CR][CR]]$INFO[Container($PARAM[container_id]).ListItem.Plot][CR][CR]</label>
                    <shadowcolor>text_shadow</shadowcolor>
¨                    <autoscroll delay="3500" time="2500" repeat="5000">Skin.HasSetting(autoscroll)</autoscroll>
                    <visible>!Container($PARAM[container_id]).ListItem.IsCollection</visible>
                </control>
            </control>
        </definition>
    </include>
    """
"""
#############################
######### Home.xml ##########
#############################
"""

menu = """
        <item>
            <label>$INFO[Skin.String(menu_REPLACE_POS_name)]</label>
            <property name="menu_id">REPLACE_NUM</property>
            <onclick>RunAddon($INFO[Skin.String(menu_REPLACE_POS_addon)])</onclick>
            <thumb>icons/sidemenu/$INFO[Skin.String(menu_REPLACE_POS_icon)]</thumb>
            <property name="id">REPLACE_ID</property>
        </item>
        """

movie_widget_base = """
                <control type="group" id="REPLACE_NUM">
                    <visible>String.IsEqual(Container(9000).ListItem.Property(id),REPLACE_ID)</visible>
                    <include content="Visible_Right_Delayed">
                        <param name="id" value="REPLACE_ID"/>
                    </include>
                    <control type="grouplist" id="REPLACE_GROUP_NUM">
                        <include>WidgetGroupListCommon</include>
                    </control>
                </control>
"""

movie_widget_category = """
                        <include content="WidgetListCategories">
                            <param name="content_path" value="library://video/REPLACE_ID/"/>
                            <param name="widget_header" value="$LOCALIZE[31148]"/>
                            <param name="widget_target" value="videos"/>
                            <param name="list_id" value="REPLACE_CAT_NUM"/>
                        </include>
"""

movie_widget_poster = """
                        <include content="WidgetListPoster">
                            <param name="content_path" value="$INFO[Skin.String(REPLACE_XML_PATH)]"/>
                            <param name="widget_header" value="$INFO[Skin.String(REPLACE_HEADER)]"/>
                            <param name="widget_target" value="videos"/>
                            <param name="list_id" value="REPLACE_POSTER_NUM"/>
                            <param name="title" value="$INFO[Container($PARAM[list_id]).ListItem.Title,: ]$INFO[Container($PARAM[list_id]).ListItem.Genre, - [COLOR button_focus],[/COLOR]]"/>
                            <param name="sortby" value="REPLACE_SORT"/>
                            <param name="sortorder" value="descending"/>
                        </include>
                        """
                        # if you want to limit number of items...
                        #<param name="item_limit" value="$INFO[Container($PARAM[list_id]).NumItems]"/>

# append widget_info_node_home after this code:
#           <include content="IconButton">
#               <param name="control_id" value="803" />
#               <param name="onclick" value="Fullscreen" />
#               <param name="icon" value="icons/now-playing/fullscreen.png" />
#               <param name="label" value="$LOCALIZE[31000]" />
#               <param name="visible" value="Player.HasMedia" />
#           </include>
#       </control>
#   </control>
widget_info_node_home = """
 <control type="group">
                <visible>Control.HasFocus(5100) | Control.HasFocus(5200) | Control.HasFocus(5300) | Control.HasFocus(5400) | Control.HasFocus(5600) | Control.HasFocus(6100) | Control.HasFocus(6200) | Control.HasFocus(6300)</visible>
                <animation type="Visible">
                    <effect type="fade" start="0" end="100" time="300" tween="sine" easing="out" />
                    <effect type="slide" start="-320" end="0" time="400" tween="cubic" easing="out" />
                </animation>
                <animation type="Hidden">
                    <effect type="fade" start="100" end="0" time="300" tween="sine" easing="out" />
                    <effect type="slide" start="0" end="-320" time="300" tween="cubic" easing="out" />
                </animation>
                <left>0</left>
                <top>0</top>
                <control type="image">
                    <width>462</width>
                    <bottom>0</bottom>
                    <texture>colors/black.png</texture>
                </control>
                <include content="WidgetInfo">
                    <param name="container_id" value="5100" />
                </include>
                <include content="WidgetInfo">
                    <param name="container_id" value="5200" />
                </include>
                <include content="WidgetInfo">
                    <param name="container_id" value="5300" />
                </include>
                <include content="WidgetInfo">
                    <param name="container_id" value="5400" />
                </include>
                <include content="WidgetInfo">
                    <param name="container_id" value="5600" />
                </include>
                <include content="WidgetInfo">
                    <param name="container_id" value="6100" />
                </include>
                <include content="WidgetInfo">
                    <param name="container_id" value="6200" />
                    <param name="episode" value="true" />
                </include>
                <include content="WidgetInfo">
                    <param name="container_id" value="6300" />
                </include>
</control>
"""

widget_info_node_home_append = """
<include content="WidgetInfo">
    <param name="container_id" value="REPLACE_POSTER_NUM" />
</include>
"""

# REMOVE original control id=700 ! 
# https://www.xbmc-kodi.cz/prispevek-estuary-easy?pid=85185#pid85185
top_menu = """
                <control type="fixedlist" id="700">
                    <left>7</left>
                    <top>150</top>
                    <width>450</width>
                    <height>110</height>
                    <orientation>horizontal</orientation>
                    <movement>5</movement>
                    <focusposition>0</focusposition>
                    <onup>SetFocus(9000)</onup>
                    <onup>PageDown</onup>
                    <onup>PageDown</onup>
                    <ondown>SetFocus(9000)</ondown>
                    <ondown>PageUp</ondown>
                    <ondown>PageUp</ondown>
                    <onright>700</onright>
                    <onleft>700</onleft>
                    <scrolltime tween="cubic" easing="out">500</scrolltime>
                    <focusedlayout width="92">
                        <width>92</width>
                        <align>center</align>
                        <control type="image">
                            <left>20</left>
                            <width>40</width>
                            <height>40</height>
                            <align>center</align>
                            <texture>$INFO[ListItem.Art(thumb)]</texture>
                            <visible>Control.HasFocus(700)</visible>
                        </control>
                        <control type="image">
                            <left>20</left>
                            <width>40</width>
                            <height>40</height>
                            <align>center</align>
                            <texture colordiffuse="44FFFFFF">$INFO[ListItem.Art(thumb)]</texture>
                            <visible>!Control.HasFocus(700)</visible>
                        </control>
                        <control type="label">
                            <top>40</top>
                            <left>-2</left>
                            <width>200</width>
                            <align>left</align>
                            <font>font_flagL</font>
                            <label>$INFO[ListItem.Label]</label>
                            <shadowcolor>text_shadow</shadowcolor>
                            <visible>Control.HasFocus(700)</visible>
                        </control>
                        <control type="label">
                            <top>55</top>
                            <left>-2</left>
                            <width>200</width>
                            <align>left</align>
                            <font>font_flagL</font>
                            <label>$INFO[ListItem.Label2]</label>
                            <shadowcolor>text_shadow</shadowcolor>
                            <visible>Control.HasFocus(700)</visible>
                        </control>
                    </focusedlayout>
                    <itemlayout width="92">
                        <control type="image">
                            <left>20</left>
                            <width>40</width>
                            <height>40</height>
                            <align>center</align>
                            <texture colordiffuse="44FFFFFF">$INFO[ListItem.Art(thumb)]</texture>
                        </control>
                    </itemlayout>
                    <content>
                        <item>
                            <label>Napájení</label>
                            <label2></label2>
                            <onclick>ActivateWindow(shutdownmenu)</onclick>
                            <thumb>icons/power.png</thumb>
                        </item>
                        <item>
                            <label>Hledání</label>
                            <label2></label2>
                            <onclick>ActivateWindow(1107)</onclick>
                            <thumb>icons/search.png</thumb>
                        </item>
                        <item>
                            <label>Files</label>
                            <label2>Manager</label2>
                            <onclick>ActivateWindow(filemanager)</onclick>
                            <thumb>icons/filemanager.png</thumb>
                        </item>
                        <item>
                            <label>System</label>
                            <label2>Setting</label2>
                            <onclick>ActivateWindow(settings)</onclick>
                            <thumb>icons/settings.png</thumb>
                        </item>
                        <!--<item>
                            <label>Skin</label>
                            <label2>Setting</label2>
                            <onclick>ActivateWindow(SkinSettings)</onclick>
                            <thumb>icons/settings/skin.png</thumb>
                        </item>-->
                        <item>
                            <label>System</label>
                            <label2>Info</label2>
                            <onclick>ActivateWindow(systeminfo)</onclick>
                            <thumb>icons/settings/sysinfo.png</thumb>
                        </item>
                        <item>
                            <label>Full</label>
                            <label2>Screen</label2>
                            <onclick>Fullscreen</onclick>
                            <thumb>icons/now-playing/fullscreen.png</thumb>
                            <visible>Player.HasMedia</visible>
                        </item>
                    </content>
                </control>
"""

#############################
####### Settings.xml ########
#############################

settings_menu = """
            <group id="1">
				<setting id="menu_REPLACE_ID_name" type="string" label="30128" help="">
					<level>0</level>
					<default>1</default>
					<constraints>
						<allowempty>false</allowempty>
					</constraints>
					<dependencies>
						<dependency type="visible">
							<condition operator="gt" setting="menu_nums">REPLACE_VISIBLE_CONDITION</condition>
						</dependency>
					</dependencies>
					<control type="edit" format="string">
						<heading>30128</heading>
					</control>
				</setting>
				<setting id="menu_REPLACE_ID_icon" type="integer" label="30130" help="">
					<level>0</level>
					<default>0</default>
					<constraints>
						<options>
							<option label="30320">0</option>
							<option label="30321">1</option>
							<option label="30322">2</option>
							<option label="30323">3</option>
							<option label="30324">4</option>
							<option label="30325">5</option>
							<option label="30326">6</option>
							<option label="30327">7</option>
							<option label="30328">8</option>
							<option label="30329">9</option>
							<option label="30330">10</option>
							<option label="30331">11</option>
							<option label="30332">12</option>
							<option label="30333">13</option>
							<option label="30334">14</option>
							<option label="30335">15</option>
							<option label="30336">16</option>
						</options>
					</constraints>
					<dependencies>
						<dependency type="visible">
							<condition operator="gt" setting="menu_nums">REPLACE_VISIBLE_CONDITION</condition>
						</dependency>
					</dependencies>
					<control type="list" format="string">
						<heading>30130</heading>
					</control>
				</setting>
        		<setting id="menu_REPLACE_ID_addon" type="addon" label="30131" help="">
					<level>0</level>
					<default/>
					<constraints>
						<addontype>xbmc.python.pluginsource</addontype>
						<allowempty>true</allowempty>
					</constraints>
					<dependencies>
						<dependency type="visible">
							<condition operator="gt" setting="menu_nums">REPLACE_VISIBLE_CONDITION</condition>
						</dependency>
					</dependencies>
					<control type="button" format="addon">
						<heading>30131</heading>
						<show more="true" details="true">installed</show>
					</control>
				</setting>
                <setting id="menu_REPLACE_ID_generate_strings" type="string" label="30101" help="">
					<level>0</level>
					<default/>
					<constraints>
						<allowempty>true</allowempty>
					</constraints>
					<control type="button" format="action">
						<data>RunScript(script.beautify.estuary,action=create_skin_strings)</data>
						<close>false</close>
					</control>
				</setting>
                <setting id="widget_REPLACE_ID" type="boolean" label="30216" help="">
					<level>0</level>
					<default>false</default>
					<control type="toggle"/>
				</setting>
				<setting id="widget_REPLACE_ID_category" type="boolean" label="30217" help="">
					<level>0</level>
					<default>false</default>
					<dependencies>
						<dependency type="enable">
							<condition operator="is" setting="widget_REPLACE_ID">true</condition>
						</dependency>
					</dependencies>
					<control type="toggle"/>
				</setting>
			</group>
"""

settings_menu_poster = """
            <group id="REPLACE_GROUP_ID" label="REPLACE_GROUP_LABEL">
				<setting id="widget_REPLACE_ID_poster_REPLACE_SUBID" type="string" label="30210" help="">
					<level>0</level>
					<default/>
					<constraints>
						<allowempty>true</allowempty>
					</constraints>
					<control type="button" format="action">
						<data>RunScript(script.favourites,property=widget_REPLACE_ID_poster_REPLACE_SUBID&amp;changetitle=true)</data>
					</control>
                    <dependencies>
					    <dependency type="visible">
                            <and>
						        <condition operator="is" setting="widget_REPLACE_ID">true</condition>
                                <condition operator="gt" setting="widget_REPLACE_ID_nums">REPLACE_VISIBLE_CONDITION</condition>
                            </and>
					    </dependency>
				    </dependencies>
				</setting>
				<setting id="widget_REPLACE_ID_node_sort_REPLACE_SUBID" type="integer" label="30212" help="">
					<level>0</level>
					<default>1</default>
					<constraints>
						<options>
							<option label="30219">0</option>
							<option label="30220">1</option>
							<option label="30221">2</option>
						</options>
					</constraints>
					<control type="list" format="string">
						<heading>30212</heading>
					</control>
                    <dependencies>
					    <dependency type="visible">
						    <and>
						        <condition operator="is" setting="widget_REPLACE_ID">true</condition>
                                <condition operator="gt" setting="widget_REPLACE_ID_nums">REPLACE_VISIBLE_CONDITION</condition>
                            </and>
					    </dependency>
				    </dependencies>
				</setting>
			</group>
"""

"""
#############################
######### Miscs.xml #########
#############################
"""
icons_from_settings = """
addons.png,
android.png,
disc.png,
download.png,
favourites.png,
games.png,
livetv.png,
manage.png,
movies.png,
music.png,
musicvideos.png,
pictures.png,
programs.png,
radio.png,
tv.png,
videos.png,
weather.png
"""


"""
#############################
######### TODO ##############
#############################
"""

# SPLASH SCREEN
# https://www.xbmc-kodi.cz/prispevek-estuary-easy?pid=128397#pid128397