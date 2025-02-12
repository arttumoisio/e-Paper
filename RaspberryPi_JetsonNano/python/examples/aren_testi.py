#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in9
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd2in9 Demo")

    epd = epd2in9.EPD()
    logging.info("init and Clear")
    epd.init(epd.lut_full_update)
    epd.Clear(0xFF)

    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

    # partial update
    logging.info("5.show perkeles")
    epd.init(epd.lut_partial_update)
    epd.Clear(0xFF)
    time_image = Image.new('1', (epd.height, epd.width), 255)
    time_draw = ImageDraw.Draw(time_image)
    # num = 0
    perkeles = True
    while (True):
        if perkeles:
            text = "  PERKELES   "
        else :
            text = "  JUMALAUTS  "
        time_draw.rectangle((10, 10, 250, 50), fill = 255)
        time_draw.text((10, 10), text, font = font24, fill = 0)

        perkeles = not perkeles

        newimage = time_image.crop([10, 10, 120, 50])
        time_image.paste(newimage, (10,10))
        epd.display(epd.getbuffer(time_image))

    logging.info("Clear...")
    epd.init(epd.lut_full_update)
    epd.Clear(0xFF)

    logging.info("Goto Sleep...")
    epd.sleep()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd2in9.epdconfig.module_exit()
    exit()