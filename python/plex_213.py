#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""This module displays plex stats on the 2in13 display"""
import sys
import os
import logging
import epd2in13_V3
from PIL import Image,ImageDraw,ImageFont
import check_plex as plex

fontdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'fonts')

logging.basicConfig(level=logging.DEBUG)

FONT22 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 22)
FONT18 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 18)
FONT14 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 14)
FONT11 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 11)

def main():
    """Main Method, updates the display stats"""
    try:
        logging.info("Running Plex Display")

        epd = epd2in13_V3.EPD()
        logging.info("init and Clear")
        epd.init()
        epd.Clear(0xFF)

        logging.info("Clearing display...")
        image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(image)

        client = plex.PlexClient()

        draw.rectangle([(0,0),(242, 44)],outline = 0)

        if plex.check_if_alive(client):
            draw.text((5, 5), "Plex Online", font = FONT22, fill = 0)
        else:
            draw.text((5, 5), "Plex Offline", font = FONT22, fill = 0)

        status = plex.get_activity(client)
        if status:
            draw.text((140, 4), f"Streams: {status[0]}", font = FONT14, fill = 0)
            draw.text((140, 18), f"{status[1]}kbs", font = FONT14, fill = 0)
            loc_y = 44
            for session in status[2]:
                # if tvshow
                if session['grandparent_title']:
                    draw.text((5, loc_y), f"{session['username']} - "\
                        f"{session['grandparent_title']}", font = FONT11, fill = 0)
                else:
                    draw.text((5, loc_y), f"{session['username']} - "\
                        f"{session['title']}", font = FONT11, fill = 0)
                loc_y += 12
        else:
            draw.text((10, 44), "Error", font = FONT22, fill = 0)

        if plex.check_for_update(client):
            draw.text((5, 26), "Update Available", font = FONT14, fill = 0)
        else:
            draw.text((5, 26), "Up to date", font = FONT14, fill = 0)

        image = image.rotate(180) # rotate
        epd.display(epd.getbuffer(image))

    except KeyboardInterrupt:
        logging.info("ctrl + c:")
        epd2in13_V3.epdconfig.module_exit()
        sys.exit()

if __name__ == "__main__":
    main()