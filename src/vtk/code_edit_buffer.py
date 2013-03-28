#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2012 Deepin, Inc.
#               2012 Hailong Qiu
#
# Author:     Hailong Qiu <356752238@qq.com>
# Maintainer: Hailong Qiu <356752238@qq.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gobject

class TextTag(object):
    def __init__(self):
        pass

class TextMark(object):
    def __init__(self):
        pass

class TextChildAnchor(object):
    def __init__(self):
        pass

class TextIter(object):
    def __init__(self):
        pass

class TextTagTable(object):
    def __init__(self):
        pass

class TextBTree(object):
    '''
    B+ 树.
    '''
    def __init__(self):
        pass


class TextLogAttrCache(object):
    def __init__(self):
        self.line     = None # gint
        self.char_len = None # gint
        self.attrs    = LogAttr()

class LogAttr(object):
    def __init__(self):
        ''' guint type>>>
        is_line_break
        is_mandatory_break
        is_char_break
        is_white
        is_cursor_position
        is_word_start
        is_word_end
        is_sentence_boundary
        is_sentence_start
        is_sentence_end
        backspace_deletes_character
        is_expandable_space
        is_word_boundary
        '''
        pass
        
class TextBufferClass(gobject.GObject):
    __gsignals__ = {
            "insert-text" : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (
                gobject.TYPE_PYOBJECT, gobject.TYPE_STRING, gobject.TYPE_INT))
            }
    def __init__(self):
        gobject.GObject.__init__(self)
        self.tag_table = TextTagTable() #gtk_text_tag_table_new()
        self.btree     = TextBTree()
        # gtk_text_tag_table_add_buffer(buffer->tag_table, buffer)
        pass

    # tag table.
    def set_table(self, table): 
        self.tag_table = table

    def get_table(self):
        return self.tag_table

    # property. 
    def set_property(self, prop_id, vlaue, pspec):
        if prop_id == "PROP_TAG_TABLE":
            self.set_table(value)
        elif prop_id == "PROP_TEXT":
            self.set_text(value, -1)
        else:
            pass

    def get_property(self, prop_id):
        return value, pspec

    # 
    def notify(self, pspec):
        pass

    def set_text(self, text, len):
        self.emit("insert-text", self.btree, text, len)
        # ... ...

    def insert_text(self, pos, text, length):
        # gtk_text_buffer_real_insert_text
        pass

    def get_text(self, start, ned, check):
        pass

    def get_start_iter(self):
        pass

    def get_end_iter(self):
        pass
    
    def insert_pixbuf(self, pos, pixbuf):
        #  gtk_text_buffer_real_insert_pixbuf
        pass

    def insert_child_anchor(self, pos, anchor):
        # gtk_text_buffer_real_insert_anchor; 
        pass

    def delete_range(self, start, end):
        # gtk_text_buffer_real_delete_range;
        pass

    def changed(self):
        # gtk_text_buffer_real_changed;
        pass

    def modified_changed(self):
        pass

    def mark_set(self, location, mark):
        # gtk_text_buffer_real_mark_set;
        pass

    def mark_deleted(self, mark):
        pass

    def apply_tag(self, tag, start_char, end_char):
        # gtk_text_buffer_real_apply_tag;
        pass

    def remove_tag(self, tag, start_chr, end_char):
        # gtk_text_buffer_real_remove_tag; 
        pass

    def begin_user_action(self):
        pass

    def end_user_action(self):
        pass

    def paste_done(self, clipboard):
        pass


class TextBuffer(TextBufferClass):
    def __init__(self):
        TextBufferClass.__init__(self)
        pass

if __name__ == "__main__":
    def insert_text_test(text_buffer, iter, text, len):
        print "insert_text_test:", iter, text, len

    text_buffer = TextBuffer()
    text_buffer.connect("insert-text", insert_text_test)
    text_buffer.set_text("fjdsklfjsdlf", 10)



