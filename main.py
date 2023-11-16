from subprocess import Popen
from re import sub

def monitor(domain, path):
    # enumerate subdomains
    proccess = Popen(
        f"amass enum -active -passive -brute -d {domain} -w /home/Kalawy/Pentest/SecLists/Discovery/DNS/subdomains-top1million-110000.txt >> {path}/newsubdomains", shell=True)

    # delete outofscope
    with open(f"{path}/.config/outofscope", "r") as outofscope_file:
        with open(f"{path}/newsubdomains", "r+") as newsubdomains_file:
            outofscope = outofscope_file.readlines()
            newsubdomains = newsubdomains_file.read()
            for subdomain in outofscope:
                updated_content = sub(subdomain, '', newsubdomains)
            newsubdomains_file.write(newsubdomains)
    proccess = Popen(
        f"cat {path}/newsubdomains | anew {path}/subdomains | notify -p discord -d 3", shell=True)


with open("/home/Kalawy/.config/monitor/targets") as targets_file:
    targets = targets_file.readlines()
    for target in targets:
        target = target.split()
        monitor(target[0], target[1])
