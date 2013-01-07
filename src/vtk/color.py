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
from constant import ALPHA_PRECISION, PARAM_PRECISION   


def exponential_blue(surface, radius,  width, height):
    if radius < 1: 
        return False;
    # init alpha.
    alpha = (1 << ALPHA_PRECISION) * (1.0 - math.exp(-2.3 / (radius + 1.0))) 
    #
    original = new_surface(width, height) 
    cr = cairo.Context(original)
    #
    cr.set_operator(cairo.OPERATOR_SOURCE)
    cr.set_source_furface(surface, 0, 0)
    cr.paint()
    
    pixels = original.get_data()
    try:
        # process rows. 
        exponential_blue_rows (pixels,
                                 width,
                                 height,
                                 0, 
                                 height / 2,
                                 0,
                                 width,
                                 alpha)
        #
        exponential_blur_rows (pixels, 
                               width, 
                               height, 
                               height / 2, 
                               height, 
                               0, 
                               width, 
                               alpha)
        # process columns.
        exponential_blur_columns (pixels, 
                                  width, 
                                  height, 
                                  0, 
                                  width / 2, 
                                  0, 
                                  height, 
                                  alpha)
        #
        exponential_blur_columns (pixels, 
                                  width, 
                                  height, 
                                  width / 2, 
                                  width, 
                                  0, 
                                  height, 
                                  alpha)
         
    except Exception, e:
        print "exponential_blue[error]:", e

def exponential_blue_columns(pixels,
                             width,
                             height,
                             start_col,
                             end_col,
                             start_y,
                             end_y,
                             alpha): 
    for column_index in range(start_col, end_col):
        column = pixels[column_index * 4]
        #
        z_A = column[0] << PARAM_PRECISION
        z_R = column[1] << PARAM_PRECISION
        z_G = column[2] << PARAM_PRECISION
        z_B = column[3] << PARAM_PRECISION
        # top to bottom.
        temp_start_y = width * (start_y + 1)
        temp_end_y   = (end_y - 1) * width
        for index in range(temp_start_y, temp_endy, width):
            column[index * 4], z_A, z_R, z_G, z_B = exponential_blur_inner (
                    column[index * 4], z_A, z_R, z_G, z_B)
            # save. 
            pixels[column_index * 4][index * 4] = column[index * 4]
        # bottom to top.
        temp_end_y = (end_y - 2) * width
        temp_start_y = start_y
        for index in range(temp_end_y, temp_start_y, -width):
            column[index * 4], z_A, z_R, z_G, z_B = exponential_blur_inner (
                    column[index * 4], z_A, z_R, z_G, z_B) 
            # save.
            pixels[column_index * 4][index * 4] = column[index * 4]

def exponential_blue_rows(pixels,
                          width,
                          height,
                          start_row,
                          end_row,
                          start_x,
                          end_x,
                          alpha):
    #
    for row_index in range(start_row, end_row):
        row = pixels[row_index * width * 4:]
        #
        z_A = row[start_x + 0] << PARAM_PRECISION 
        z_R = row[start_x + 1] << PARAM_PRECISION 
        z_G = row[start_x + 2] << PARAM_PRECISION 
        z_B = row[start_x + 3] << PARAM_PRECISION 
        # left to right.
        for index in range(start_x + 1, end_x):
            row[index * 4], z_A, z_R, z_G, z_B = exponential_blur_inner(
                    row[index * 4], z_A, z_R, z_G, z_B, alpha
                    )
            # save. 
            pixels[row_index * width * 4:][index * 4] = row[index * 4]
        # right to left.
        for index in range(end_x - 2, start_x, -1):
            row[index * 4], z_A, z_R, z_G, z_B = exponential_blur_inner(
                    row[index * 4], z_A, z_R, z_G, z_B, alpha
                    )
            # save.
            pixels[row_index * width * 4:][index * 4] = row[index * 4] 

def exponential_blur_inner(pixel, z_A, z_R, z_G, z_B, alpha):
    #
    z_A += (alpha * ((pixel[0] << PARAM_PRECISION) - z_A)) >> ALPHA_PRECISION
    z_R += (alpha * ((pixel[1] << PARAM_PRECISION) - z_R)) >> ALPHA_PRECISION
    z_G += (alpha * ((pixel[2] << PARAM_PRECISION) - z_G)) >> ALPHA_PRECISION
    z_B += (alpha * ((pixel[3] << PARAM_PRECISION) - z_B)) >> ALPHA_PRECISION
    # 
    pixel[0] = z_A >> PARAM_PRECISION 
    pixel[1] = z_R >> PARAM_PRECISION 
    pixel[2] = z_G >> PARAM_PRECISION 
    pixel[3] = z_B >> PARAM_PRECISION 
    # return moidfy values.
    return pixel, z_A, z_R, z_G, z_B

def new_surface(width, height):
    return cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height) 

