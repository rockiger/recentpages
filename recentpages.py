#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Search instantly as you type. Edvard Rejthar
# https://github.com/e3rd/zim-plugin-instantsearch
#
from collections import defaultdict, OrderedDict
import copy
import gobject
import gtk
import logging
from pprint import pprint
from zim.actions import action
from zim.gui.widgets import Dialog
from zim.gui.widgets import InputEntry
from zim.history import HistoryList
from zim.history import HistoryPath
from zim.notebook import Path
from zim.plugins import PluginClass
from zim.plugins import WindowExtension
from zim.plugins import extends
from zim.search import *
from zim.index import IndexPath
from copy import deepcopy
import sys
import inspect

logger = logging.getLogger('zim.plugins.recentpages')

class RecentPagesPlugin(PluginClass):

    plugin_info = {
        'name': _('Recent Pages'), # T: plugin name
        'description': _('''\
Show the recently viewed pages in a popup window.

(V 0.1.0)
'''),
        'author': "Marco Laspe"
    }


@extends('MainWindow')
class RecentPagesMainWindowExtension(WindowExtension):

    uimanager_xml = '''
    <ui>
    <menubar name='menubar'>
            <menu action='tools_menu'>
                    <placeholder name='plugin_items'>
                            <menuitem action='recentpages'/>
                    </placeholder>
            </menu>
    </menubar>
    </ui>
    '''


    gui = "";

    @action(_('_Recent Pages'), accelerator='<ctrl><shift>r') # T: menu item
    def recentpages(self):

        #init
        #TODO: Get Items from pathbar
        self.history = self.window.ui.history.get_recent()

        # preferences
        # self.plugin.preferences['keystroke_delay']


        # Gtk
        self.gui = Dialog(self.window.ui, _('Recent Pages'), buttons=None, defaultwindowsize=(300, -1))

        (px, py) = self.window.get_position()
        (pw, ph) = self.window.get_size()
        (x, y) = self.gui.get_position()
        self.gui.resize(300,100)
        self.gui.move(px + (pw / 2) - 150, py + (ph / 2) - 250)

        # Maybe add a filter field, like atom dialogs
        #self.inputEntry = InputEntry()
        #self.inputEntry.connect('key_press_event', self.move)
        #self.inputEntry.connect('changed', self.change) # self.change is needed by GObject or something
        #self.gui.vbox.pack_start(self.inputEntry, False)


        self.listmodel = gtk.ListStore(str)

        # My own model for creating dialog labels and later retrieving them
        self.model = OrderedDict()
        for page in self.history:
            ky = str(page)
            ky = ky[1:-1]
            ky = ky.split(":")
            ky = ky[-1].strip()
            self.model[ky] = page

        # populate the treeview
        for row in self.model.keys():
            self.listmodel.append([row])
        self.treeview = gtk.TreeView(model=self.listmodel)
        self.treeview.set_headers_visible(False)
        # cellrenderer to render the text
        cell = gtk.CellRendererText()
        # the text in the first column should be in boldface
        # the column is created
        col = gtk.TreeViewColumn("", cell, text=0)
        # and it is appended to the treeview
        self.treeview.append_column(col)

        self.treeview.connect("row-activated", self.on_row_activated)

        self.gui.vbox.pack_start(self.treeview, False)

        self.gui.show_all()


    def on_row_activated(self, path, view_column,user_param):
        #self.gui.move(600, 600)
        #ui.open_page(path)
        (tm, it) = self.treeview.get_selection().get_selected()
        ky = tm[it][0]
        self.window.ui.open_page(self.model[ky])
        self.gui.destroy()
        print "on_change"
        print selection
