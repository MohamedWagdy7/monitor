from subprocess import Popen,PIPE

def monitor(domain, path):
    # enumerate subdomains
    proccess = Popen(
        f"amass enum -active -passive -brute -d {domain} -w /home/Kalawy/Pentest/SecLists/Discovery/DNS/subdomains-top1million-110000.txt >> {path}/newsubdomains", shell=True,stdout=PIPE)
    proccesses.append(proccess)
    proccess.wait()
    
    proccesses.remove(proccess)
    
    # delete outofscope
    with open(f"{path}/.config/outofscope", "r") as outofscope_file:
        with open(f"{path}/newsubdomains", "r") as newsubdomains_file:
            outofscope = outofscope_file.readlines()
            newsubdomains = newsubdomains_file.readlines()
            for subdomain in newsubdomains:
                if subdomain in outofscope:
                    newsubdomains.remove(subdomain)
            anew = Popen(f"cat {path}/newsubdomains | anew {path}/subdomains >> {path}/new")
            proccesses.append(anew)
            anew.wait()
            proccesses.remove(anew)
            
proccesses = []
            
with open("/home/Kalawy/.config/monitor/targets") as targets_file:
    try:
        targets = targets_file.readlines()
        for target in targets:
            target = target.split()
            monitor(target[0], target[1])
    except KeyboardInterrupt:
        for pro in proccesses:
            pro.kill()