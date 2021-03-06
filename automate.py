import glib
import os
import glob
from shutil import copy
import pyudev
from pyudev import Context, Monitor
from usb_path import Usb
import shutil


try:
    from pyudev.glib import MonitorObserver
  
    def device_event(observer, device):
        if device.action == 'add':
            # some function to run on insertion of usb
            if(device.device_type=='usb_interface'):
                #print usb.get_mount_points()
                path=usb.get_mount_points()
                print path
                if not path[0][1]:
                    print('empty')
                else:
                    csv_path= find_that_file_latest(path[0][1])
                    print('path is :'+csv_path);
                    if os.path.isfile(csv_path):
                        copy_file_to_dest(csv_path)


except:
    from pyudev.glib import GUDevMonitorObserver as MonitorObserver
   
    def device_event(observer, action, device):
        print 'event {0} on device {1}'.format(action, device)

def delete_directory(path):
    folder =os.path.dirname(path)
    try:
        shutil.rmtree(folder)
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))

def find_that_file(path):
    finalCsvList=[]
    for root, dirs, files in os.walk(path):
        files = [f for f in files if not f[0] == '.']
        for file in files:
            if file.endswith(".csv"):
                finalCsvList.append(os.path.join(root, file))
                #return os.path.join(root, file)
    #print(finalCsvList)
    return finalCsvList

def copy_file_to_dest(src):
    dst='/home/pi/storage/data.csv'
    print os.path.exists(str(src))
    print str(src)
    #os.makedirs(os.path.dirname(dst))
    copy(str(src), dst)#, ignore=ignore_patterns('*.pyc', 'tmp*'))    
    print "copied"
    #delete_directory(src)

def find_that_file_latest(path):
    #files_path = os.path.join(path, '*.csv')
    #list_of_files = glob.iglob(files_path) # * means all if need specific format then *.csv
    latest_file = max(find_that_file(path), key=os.path.getctime)
    return latest_file

def get_usb_devices():
    context = Context()
    monitor = Monitor.from_netlink(context)
    monitor.filter_by(subsystem='usb')
    observer = MonitorObserver(monitor)
    observer.connect('device-event', device_event)
    monitor.start()
    glib.MainLoop().run()

if __name__ == '__main__':
    usb = Usb()
    get_usb_devices()
