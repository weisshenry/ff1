#!/bin/bash
nmap -sP 192.168.1.* | grep IPCAM > out1.txt
echo "end"