import json

import nmap
import pandas as pd
import webbrowser
import os
from pivottablejs import pivot_ui


class Network(object):
    def __init__(self):
        ip = ''
        self.ip=ip

    def network_scanner(self):
        if len(self.ip)<=0:
            self.ip =input ("please enter the default getway ip")
            if len (self.ip)==0:
                self.ip = '192.168.1.1'
            network=self.ip+"/24"
        else:
            network = self.ip + "/24"
        print("scanning ----------------------->")
        nm = nmap.PortScanner()
        nm.scan(hosts=network,arguments='-sn')
        allin = pd.DataFrame()
        for x in nm.all_hosts():
            try:
                name= nm[x]['hostnames'][0]['name']
                ip=x
                status=nm[x]['status']['state']
                tempin = pd.DataFrame({'name':[name],'ip':[ip],'status':[status]})
                allin = allin.append(tempin)
            except Exception as e:
                print(e)
                pass

        return allin
if __name__=="__main__":
    D=Network()
    df=D.network_scanner()
    print(df)
    fileout = "all_up_devices.html"
    df=df.reset_index(drop=True)
    outfile=fileout.replace("html",'csv')
    df.to_csv(outfile)
    pivot_ui(df, rows=list(df.index), cols=list(df.columns),outfile_path=fileout)
    webbrowser.open('file://' + os.path.realpath(fileout))