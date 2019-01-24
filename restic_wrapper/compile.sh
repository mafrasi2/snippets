#!/bin/sh
clang restic_wrapper.c -lcap-ng -o restic_wrapper
sudo setcap cap_dac_read_search=+ep /home/restic/restic_wrapper
