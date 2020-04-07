import requests
from bs4 import BeautifulSoup
import RPi.GPIO as GPIO
from time import sleep, strftime
from datetime import datetime
from datetime import datetime

from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.led_matrix.device import max7219
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, LCD_FONT

#Set up for 32x8 LED Matrix
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, width=32, height=8, block_orientation=-90)
device.contrast(1)
virtual = viewport(device, width=32, height=8)

#Set up for the web scraper 
url = 'https://www.worldometers.info/coronavirus/'

#text(draw, (0, 1), datetime.now().strftime('%I:%M'), fill="white", font=proportional(CP437_FONT))

while True:
    
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')
    
    #total
    total = soup.find_all('div', {'class': 'maincounter-number'})
    total_world = total[0]
    dead_world = total[1]
    active_world = soup.find('div', {'class': 'number-table-main'})
    
    #usa
    usa_total = soup.find("td", text="USA").find_next_sibling("td").text
    usa_dead = soup.find('td', text = usa_total).find_next_sibling('td').find_next_sibling('td').text
    
    #Canada
    canada_total = soup.find("td", text="Canada").find_next_sibling("td").text
    canada_dead = soup.find('td', text = canada_total).find_next_sibling('td').find_next_sibling('td').text
    
    now = datetime.now()
    d1 = now.strftime("%d-%m-%Y %H:%M:%S")
    
    show_message(device, d1 + ' World Total: ' + total_world.text, fill ='white', font=proportional(LCD_FONT), scroll_delay=0.04)
    show_message(device, 'World Dead: ' + dead_world.text, fill ='white', font=proportional(LCD_FONT), scroll_delay=0.04)
    show_message(device, 'World Active: ' + active_world.text, fill ='white', font=proportional(LCD_FONT), scroll_delay=0.04)
    
    show_message(device, 'USA Total: ' + usa_total, fill ='white', font=proportional(LCD_FONT), scroll_delay=0.04)
    show_message(device, 'USA Dead: ' + usa_dead, fill ='white', font=proportional(LCD_FONT), scroll_delay=0.04)

    show_message(device, 'Canada Total: ' + canada_total, fill ='white', font=proportional(LCD_FONT), scroll_delay=0.04)
    show_message(device, 'Canada Dead: ' + canada_dead, fill ='white', font=proportional(LCD_FONT), scroll_delay=0.04)
