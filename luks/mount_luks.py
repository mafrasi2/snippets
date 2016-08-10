#!/usr/bin/env python3

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

print("Requesting free loop device...")
loop_dev = run(["losetup", "-f"], stdout=subprocess.PIPE).stdout
loop_dev = loop_dev.decode("utf-8").strip()

print("Mounting {} to loop device {}...".format(source_file, loop_dev))
if 0 != call(["losetup", loop_dev, sys.argv[1]]):
    error("Error: Failed to mount loop device")

print("Opening loop device with cryptsetup...")
if 0 != call(["cryptsetup", "--type", "luks", "open", loop_dev, container_name]):
    error("Error: Failed decrypt loop device")

print("Mounting container to {}...".format(mount_point))
if 0 != call(["mount", "/dev/mapper/{}".format(container_name), mount_point]):
    error("Error: Failed to mount container")


