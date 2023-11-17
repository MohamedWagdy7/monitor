from subprocess import Popen

def monitor(domain, path):
    # enumerate subdomains
    proccess = Popen(
        f"amass enum -active -passive -brute -d {domain} -w /home/Kalawy/Pentest/SecLists/Discovery/DNS/subdomains-top1million-110000.txt >> {path}/newsubdomains", shell=True)
    proccess.wait()

    # delete outofscope
    with open(f"{path}/.config/outofscope", "r") as outofscope_file:
        with open(f"{path}/newsubdomains", "r") as newsubdomains_file:
            outofscope = outofscope_file.readlines()
            newsubdomains = newsubdomains_file.readlines()
            for subdomain in newsubdomains:
                if subdomain in outofscope:
                    newsubdomains.remove(subdomain)
            for i in newsubdomains:
                print(i)

with open("/home/Kalawy/.config/monitor/targets") as targets_file:
    targets = targets_file.readlines()
    for target in targets:
        target = target.split()
        monitor(target[0], target[1])
