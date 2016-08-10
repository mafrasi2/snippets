#!/usr/bin/env python3

import json
import os
import subprocess
import sys
from subprocess import call, run

def error(msg):
    if msg != None:
        print(msg)
    exit(1)

if len(sys.argv) != 4:
    print("Usage: {} <source_file> <mount_point> <container_name>".format(sys.argv[0]))
    exit(1)

source_file = sys.argv[1]
mount_point = sys.argv[2]
container_name = sys.argv[3]

print("Querying loop device for {}...".format(source_file))
loop_dev = run(["losetup", "--list", "--json", "-j", source_file], stdout=subprocess.PIPE).stdout
loop_dev = json.loads(loop_dev.decode("utf-8"))
if len(loop_dev["loopdevices"]) != 1:
    error("There are {} loop devices associated with {}".format(len(loop_dev["loopdevices"]), source_file))
loop_dev = loop_dev["loopdevices"][0]["name"]

print("Unmounting {}...".format(mount_point))
if 0 != call(["umount", "/dev/mapper/{}".format(container_name)]):
    error("Error: Failed to unmount container")

print("Closing LUKS container {}...".format(container_name))
if 0 != call(["cryptsetup", "close", container_name]):
    error("Error: Failed close container")

print("Closing loop device {}...".format(loop_dev))
if 0 != call(["losetup", "-d", loop_dev]):
    error("Error: Failed to close loop device")

