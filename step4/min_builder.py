#!/usr/bin/python  
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.topolib import TreeTopo
import os
import sys
import time
import json
import ast 


"""Custom topology 

Building topology depending on edge-list

"""
class allH1Topo(Topo):
    def build(self,l):
        #dictionary for the names of the hosts&switches
        sh={}
        #switch = self.addSwitch('sVx00')    
        for e in l:
	    print e
	    #flag= 0 {same vm}, 1 {first node in other vm}, 2 {second node in other vm}
	    flag=0
            if e[2]==vm:
		if e[0] not in sh:
                    if e[0] in mH:
                            host=self.addHost('h_%s' % (e[0]),ip='10.0.%s.%s'%((e[0]&65280)>>8,e[0]&255))
                            #if dV[e[0]]==1:
                            s1=self.addSwitch('s_%s' % (e[0]))
                            self.addLink(s1,host)
                            sh[e[0]]='s_'+str(e[0])
                    else:
                        #creation of non-malicious host->switch
                        s1=self.addSwitch('s_%s' %(e[0]))
                        sh[e[0]]='s_'+str(e[0])
		
			
            else:
                flag=1
                #s1=self.addSwitch('s_%s' %(e[0]))
                sh[e[0]]='s_'+str(e[0])
                vm2=e[2]
                    
            if e[3]==vm:
                if e[1] not in sh:
                    if e[1] in mH:
			    #host=self.addHost('h_%s' % (e[1]))
                            host=self.addHost('h_%s' % (e[1]),ip='10.0.%s.%s'%((e[1]&65280)>>8,e[1]&255))
                            #if dV[e[0]]==1:
                            s2=self.addSwitch('s_%s' % (e[1]))
                            self.addLink(s2,host)
                            sh[e[1]]='s_'+ str(e[1])
		            #print str[e[1]]
			    #else:
                    else:
                        #creation of non-malicious host->switch
                        s2=self.addSwitch('s_%s' %(e[1]))
                        sh[e[1]]='s_'+ str(e[1])
            else:
                flag=2
                #s2=self.addSwitch('s_%s' %(e[1]))
                sh[e[1]]='s_'+ str(e[1])
                vm2=e[3]

            if flag==0:
                self.addLink(sh[e[0]],sh[e[1]])
	    elif flag==2:
                if sh[e[0]] not in vDict:
		    	#print '23456$#@!@#$*^&%#^$@%$!@#&$^$@%#!$@@#&$^@%#$!'
			#print sh[e[0]]
			vDict[sh[e[0]]]=[[vm2],[sh[e[0]]+sh[e[1]]],[e[4]],1]
                else:
                    vDict[sh[e[0]]][1].append(sh[e[0]]+sh[e[1]])
                    vDict[sh[e[0]]][3]+=1
		    #print vDict[sh[e[0]]]
		    vDict[sh[e[0]]][2].append(e[4])
                    vDict[sh[e[0]]][0].append(vm2)
		    #print '#####$$$$$$$#########'
		    #print vDict[sh[e[0]]]
		    #print '#####$$$$$$$#########'
	    
                #self.addLink(switch,sh[e[1]])
	    else:
                if sh[e[1]] not in vDict:
		    vDict[sh[e[1]]]=[[vm2],[sh[e[0]]+sh[e[1]]],[e[4]],1]
                else:
                    vDict[sh[e[1]]][1].append(sh[e[0]]+sh[e[1]])
                    vDict[sh[e[1]]][3]+=1
                    vDict[sh[e[1]]][2].append(e[4])
                    vDict[sh[e[1]]][0].append(vm2)
                #self.addLink(switch,sh[e[0]])

"""
-Creates the custom topology allH1Topo
-h1 runs SimpleHTTPServer
-All hosts run curl to h1 
-results on output_script.pcap, outputcurl.txt
"""

def Test(num):
    "Create and test a simple network"
    topo = allH1Topo(l=num)
    net = Mininet(topo)
    net.start()
    hosts=net.hosts
    switches=net.switches
    for switch in switches:
	if str(switch) in vDict:
		s=switch.name
		#print len(vDict[str(switch)][1])
		if vDict[str(switch)][3]==1:
                    switch.cmd('ovs-vsctl add-port %(switch)s vx%(number1)s -- set interface vx%(number1)s type=vxlan options:remote_ip=%(vm2)s options:key=%(number)s'% {"number":vDict[str(switch)][2][0],"number1":vDict[str(switch)][1][0], "vm2":vDict[str(switch)][0][0],"switch":s})
		else:		
                    for i in range(len(vDict[str(switch)][1])):
                    	#print '##########################'
		    	#print s
		        #print i
                    	#print '##########################'
                    	switch.cmd('ovs-vsctl add-port %(switch)s vx%(number1)s -- set interface vx%(number1)s type=vxlan options:remote_ip=%(vm2)s options:key=%(number)s'% {"number":vDict[str(switch)][2][i],"number1":vDict[str(switch)][1][i], "vm2":vDict[str(switch)][0][i],"switch":s})
			#print "olaaa"
                #"number":int(filter(str.isdigit,vDict[str(switch)][1]))%100
    
    for h in hosts:
        if h.name=='h_701':
            h.cmdPrint('iperf -s  >iperf_30_5Vms.txt -t 500 -i 120   &')
            #h.cmd('iperf -s  -i 2 -t 120  &')
            print "#################################################################################"
            print "#################################################################################"
            #h.cmd('tcpdump -U -i any -w output_100_120s.pcap &')
        else:   
            #h.cmd("ping 10.0.2.189 -c 3")
            h.cmdPrint('iperf -c 10.0.2.189 -t 120 -M 1400 &  ')
       
    #switch.cmdPrint('ovs-vsctl show')		

    CLI(net)
    #net.pingAll()
    net.stop()
   
if __name__=='__main__':
    l=[]
    #input1=this vm's ip
    #input2=edges/vms
    flag=0
    vDict={}
    #os.system("from_paths_to_vm.py ")
    vm=str(sys.argv[1])
    #print vm
    #edges=eval(open(sys.argv[2]))
    #mH=[12288,7473,702,701,9216,6147,8197,17409,9900,32778,24587,16397,10257,509]
    with open(sys.argv[3]) as f:                                               
        mH=f.read().splitlines()                                               
    mH.remove('None')                                                         
    mH=map(int,mH)
    with open(sys.argv[2]) as f:
    	edges = [ast.literal_eval(line) for line in f]    
    dV={}
    key={}
    count=0
    for e in edges:
        e= e + (count,)
        count+=1
        if vm in e:
            #print key
            l.append(e)
            if e[0] in dV:
                dV[e[0]]+=1
            else:
                dV[e[0]]=1
            if e[1] in dV:
                dV[e[1]]+=1
            else:
                dV[e[1]]=1
            #print e
    setLogLevel('info')
    #print l
    Test(l)
