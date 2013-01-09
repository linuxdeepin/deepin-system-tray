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


import cairo
import pango
import math
import struct
from constant import ALPHA_PRECISION, PARAM_PRECISION   

def exponential_blue(surface, surface_context, radius,  width, height, process_count=2):
    if radius < 1: 
        return False;
    # init alpha.
    alpha = (1 << ALPHA_PRECISION) * (1.0 - math.exp(-2.3 / (radius + 1.0)))
    print "alpha:", alpha, width, height
    #
    original = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    cr = cairo.Context(original)
    #
    cr.set_operator(cairo.OPERATOR_SOURCE)
    cr.set_source_surface(surface, 0, 0)
    cr.paint()
    #
    pixels = original.get_data()
    print "test pixels:", ord(pixels[300])
    #
    w = width
    h = height
    channels = 4
    if (radius > w - 1) or (radius > h - 1):
        return False
    vmin = []
    for i in range(0, int(max(w, h))):
        vmin.append(0)

    vmax = []
    for i in range(0, int(max(w, h))):
        vmax.append(0)
    div = 2 * radius + 1;
    dv = range(0, 256 * div)
    buffer = []
    for i in range(0, w * h * channels):
        buffer.append(0)

    for i in range(0, len(dv)):
        dv[i] = i / div
        
    while process_count > 0: 
        # Top to Bottom.
        for x in range(0, w):
            vmin[x] = int(min(x + radius + 1, w - 1)) 
            vmax[x] = int(max(x - radius, 0))

        for y in range(0, h):
            #print "y:", y
            asum, rsum, gsum, bsum = 0, 0, 0, 0
            cur_pixel = y * w * channels
            asum += radius * ord(pixels[cur_pixel + 0])
            rsum += radius * ord(pixels[cur_pixel + 1])
              gsum += radius * ord(pixels[cur_pixel + 2])
            bsum += radius * ord(pixels[cur_pixel + 3])
            for i in range(0, radius):
                asum += ord(pixels[cur_pixel + 0])
                rsum += ord(pixels[cur_pixel + 1])
                gsum += ord(pixels[cur_pixel + 2])
                bsum += ord(pixels[cur_pixel + 3])
                cur_pixel += channels
            #
            cur_pixel = y * w * channels
            for x in range(0, w):
                p1 = (y * w + vmin[x]) * channels
                p2 = (y * w + vmax[x]) * channels

                buffer[cur_pixel + 0] = dv[asum]
                buffer[cur_pixel + 1] = dv[rsum]
                buffer[cur_pixel + 2] = dv[gsum]
                buffer[cur_pixel + 3] = dv[bsum]
                #
                asum += ord(pixels[p1 + 0]) - ord(pixels[p2 + 0])
                rsum += ord(pixels[p1 + 1]) - ord(pixels[p2 + 1])
                gsum += ord(pixels[p1 + 2]) - ord(pixels[p2 + 2])
                bsum += ord(pixels[p1 + 3]) - ord(pixels[p2 + 3])
                cur_pixel += channels

        # left to right.
        for y in range(0, h):
            vmin[y] = int(min(y + radius + 1, h - 1)) * w
            vmax[y] = int(max(y - radius, 0)) * w
        #
        for x in range(0, w):
            asum, rsum, gsum, bsum = 0, 0, 0, 0
            cur_pixel = x * channels

            asum += radius * buffer[cur_pixel + 0]
            rsum += radius * buffer[cur_pixel + 1]
            gsum += radius * buffer[cur_pixel + 2]
            bsum += radius * buffer[cur_pixel + 3]

            for i in range(0, radius):
                asum += buffer[cur_pixel + 0]
                rsum += buffer[cur_pixel + 1]
                gsum += buffer[cur_pixel + 2]
                bsum += buffer[cur_pixel + 3]

                cur_pixel += w * channels
                
            cur_pixel = x * channels

            for y in range(0, h):
                p1 = (x + vmin[y]) * channels
                p2 = (x + vmax[y]) * channels
                pixels[cur_pixel + 1] = struct.pack('b', dv[rsum])
                pixels[cur_pixel + 2] = struct.pack('b', dv[gsum])
                pixels[cur_pixel + 3] = struct.pack('b', dv[bsum])
                #
                asum += buffer[p1 + 0] - buffer[p2 + 0]
                asum += buffer[p1 + 1] - buffer[p2 + 1]
                asum += buffer[p1 + 2] - buffer[p2 + 2]
                asum += buffer[p1 + 3] - buffer[p2 + 3]

                cur_pixel += w * channels

        process_count -= 1
    #
    surface_context.set_operator (cairo.OPERATOR_SOURCE);
    surface_context.set_source_surface (original, 0, 0);
    surface_context.paint ();
    surface_context.set_operator (cairo.OPERATOR_OVER);
    
