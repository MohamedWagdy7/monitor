#!/usr/bin/env python

from subprocess import Popen,DEVNULL


def monitor(domain, path):
    # enumerate subdomains
    proccess = Popen(
        f"amass enum -active -passive -brute -d {domain} -w /home/Kalawy/Pentest/SecLists/Discovery/DNS/subdomains-top1million-110000.txt > {path}/newsubdomains 2>/dev/null", shell=True,stdout=DEVNULL,stderr=DEVNULL)
    proccess.wait()
    
    # delete outofscope
    with open(f"{path}/.config/outofscope", "r") as outofscope_file:
        with open(f"{path}/newsubdomains", "r") as newsubdomains_file:
            outofscope = outofscope_file.readlines()
            newsubdomains = newsubdomains_file.readlines()
            for subdomain in newsubdomains:
                if subdomain in outofscope:
                    newsubdomains.remove(subdomain)
            anew = Popen(f"cat {path}/newsubdomains | anew {path}/subdomains | notify -p discord 2>/dev/null && rm {path}/newsubdomains",shell=True,stdout=DEVNULL,stderr=DEVNULL)
            anew.wait()

with open("/home/Kalawy/.config/monitor/targets") as targets_file:
    targets = targets_file.readlines()
    for target in targets:
        target = target.split()
        monitor(target[0], target[1])