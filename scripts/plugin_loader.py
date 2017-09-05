#!/usr/bin/python

"""
Part of the Greenery.guru project
Monitor plugin directory, and if any new files have been added, load new 
plugins into the inventory db.

TODO:
Needs a lot more error checking and exception handling! Also, loggin would be
nice too.
"""

import os
import sys
import subprocess
import hashlib

def main():
    plugin_dir = os.path.join(os.environ['GREENERY_WEB'], 'plugins')
    secret_file = os.path.join(plugin_dir, '.checksum')
    old = read_checksum_file(secret_file)
    new = dir_checksum(plugin_dir)

    if old and old == new:
        sys.exit(0)
    
    load_plugins(plugin_dir)
    write_checksum_to_file(new, secret_file)
    

def read_checksum_file(fname):
    try:
        fh = open(fname, 'r')
        md5 = fh.readlines()[0]
        fh.close()
        return md5
    except:
        return None


def write_checksum_to_file(md5, fname):

    fh = open(fname, 'w')
    fh.write(md5)
    fh.close()


def dir_checksum(path):
    cmd = ['ls', '-ltr', path]
    child = subprocess.Popen(cmd,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE )
    out, err = child.communicate()
    m = hashlib.md5()
    m.update(out)
    return m.hexdigest()


def load_plugins(path):
    import django
    from yapsy.PluginManager import PluginManager
    sys.path.append(os.environ['GREENERY_WEB'])
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'greenery.settings')
    django.setup()
    from app.inventory.models import Plugin   

    manager = PluginManager()
    manager.setPluginPlaces([path])
    manager.collectPlugins()
    dbobjects = list(Plugin.objects.all())

    # skip plugin names we already have stored
    for plugin in manager.getAllPlugins():
        found = False
        for obj in dbobjects:
            if obj.name == plugin.name:
                found = True
                break

        if not found:
            try:
                newp = Plugin.objects.get_or_create(name=plugin.name)[0]
                notes = ""
                if plugin.description:
                    notes += "DESCRIPTION: %s\n" % plugin.description

                if plugin.version:
                    notes += "VERSION: %s\n" % str(plugin.version)

                if plugin.author:
                    notes += "AUTHOR: %s\n" % plugin.author

                if plugin.website:
                    notes += "WEBSITE: %s\n" % plugin.website
                

                newp.documentation = notes
                newp.save()
            except:
                raise

if __name__ == '__main__':
    main()
