# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

import time
import subprocess
import shlex
import commands
import re

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

BLINK_LED_SCRIPT = "/home/pi/programming/rpi2_blink_led/blink_led.py"

# This one is a little dangerous hehe -- naming it '__<url>' makes it inacessible to anything but this script
def __system(cmd, block):
    result = ''

    if block:
        try:
            result = commands.getstatusoutput(cmd)[1]
        except:
            pass
    else:
        try:
            args = shlex.split(cmd)
            p = subprocess.Popen(args)
        except:
            pass

    return result

def index():
    return dict(message="Hello WWW, my name is Nathan and today I'll be learning about the MVC pattern, web2py, and RPI 2 GPIO.")

def foo():
    f = open("/home/pi/TEST_FILE.txt", 'w')
    f.write("bar!!!!\n")
    f.close()
    return "Foo, bro!"

def button():
    return HTML(BODY(CENTER(FORM(BUTTON("Cycle LEDs", _name="cycle_btn", _value="cycle"), _action="", _method="post"))))

def cputempf():
    try:
        raw_temp = int(__system("cat /sys/class/thermal/thermal_zone0/temp", True))
        raw_temp = raw_temp / 1000.0
        f_temp = (raw_temp*(9.0/5.0)) + 32.0
    except Exception as err:
        return err
        
    return "{0:.2f}".format(f_temp)

def gputempf():
    try:
        raw_temp = __system("/opt/vc/bin/vcgencmd measure_temp", True)
        match = re.search(r'temp=(\d+\.\d*)', raw_temp)
        if match:
            f_temp = (float(match.group(1))*(9.0/5.0)) + 32.0
    except Exception as err:
        return err
        
    return "{0:.2f}".format(f_temp)

def ambienttempf():
    try:
        temp_f = __system("sudo python /home/pi/programming/bmp085/bmp085.py --temp=f", True)
    except Exception as err:
        return err
                     
    return temp_f   
                                       
def ambientpressureb():
    try:
        pressure_b = __system("sudo python /home/pi/programming/bmp085/bmp085.py --pressure=b", True)
    except Exception as err:
        return err
                                                                       
    return pressure_b

def ambient_tempf_pressureb():
    try:
        result = __system("sudo python /home/pi/programming/bmp085/bmp085.py --temp=f --pressure=b", True)
    except Exception as err:
        return err
                                                                       
    return result

def cycle():
    # Attempt to get the rate parameter
    rate = request.vars['rate']
    return __cycle(rate)

def __cycle(rate):
    # This is defined as the default rate in blink_led.py
    DEF_RATE = -1

    if rate == None:
        rate = DEF_RATE

    __system("python {0} --cycle_rgb {1}".format(BLINK_LED_SCRIPT, rate), False)

    if rate == DEF_RATE:
        rate = "default rate"

    return HTML(BODY(H1("Cycling LEDS @ rate: {0}!".format(rate))))

def read():
    pin = request.vars['pin']
    return __read(pin)

def __read(pin):
    # This is the default pin defined in blink_led.py.
    DEF_PIN = 19

    if pin == None:
        pin = DEF_PIN

    val = __system("python {0} --read_input {1}".format(BLINK_LED_SCRIPT, pin), True)
    return val

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
