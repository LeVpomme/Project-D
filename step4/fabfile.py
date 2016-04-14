from fabric.api import *
from fabric.tasks import execute
#cd,parallel,run,env,execute,task,sudo,open_shell
import networkx as nx
import sys
import os
from ast  import literal_eval
#env.hosts = ['snf-680603.vm.okeanos.grnet.gr']
#env.user = 'root'
#env.password = 'byslaf366'
#env.hosts=['mininet@192.168.56.102']
#env.user = 'mininet'
env.disable_known_hosts=True
env.warn_only=True
env.hosts=['mininet@192.168.56.101','mininet@192.168.56.102','mininet@192.168.56.103']
#env.hosts=['mininet@147.102.13.63','mininet@147.102.13.61','root@83.212.102.97']

#env.hosts = ["mininet@192.168.56.101","mininet@192.168.56.102"]

env.passwords = {'mininet@192.168.56.101:22': 'mininet', 'mininet@192.168.56.102:22': 'mininet','mininet@192.168.56.103:22' : 'mininet'}
#env.passwords = {'mininet@147.102.13.63:22': 'mininet', 'mininet@147.102.13.61:22': 'mininet','root@83.212.102.97:22' : 'byslaf366'}

ips=['192.168.56.101','192.168.56.102','192.168.56.103']
#ips=['147.102.13.63','147.102.13.61','83.212.102.97']


def showOvs():
        run('sudo ovs-vsctl show')

@parallel
def runOneLs():
    run('ls')


@parallel
def connection():
	#let's you interact with the remote VM from terminal
	#open_shell()
	#run('sudo mn')
	#with cd( '~/mininet/custom/'):
	#	run('ls')
	#put('adjToNetwork.py','~/')
	#put('exam.csv','~/')
	#put('~/USC-NSL-miniNExT-75c2781')
        # Simplest form:
        #environment = prompt('Please specify target environment: ')
        # With default, and storing as env.dish:
        #prompt('Specify favorite dish: ', 'dish', default='spam & eggs')
        #print("%s"%env.dish)
        #open_shell()
        #with hide('output'):
        #with
        #run('sudo mn -c')
        #put ('script.py','~/')
        #put ('list.txt','~/')
        #run('python script.py list.txt %s' %env.host)
	run('sudo dhclient eth1')
        run('sudo mn -c')
        run('mkdir -p testing')
        put('edges_mininet.txt','~/testing/')
        put('min_builder.py','~/testing/')
        put('allMh.txt','~/testing/')
        print '############################ %s ################'%env.host
        run('cd testing && sudo python min_builder.py %s edges_mininet.txt allMh.txt' %env.host , pty=False)
        #with settings(warn_only=True):
            #run('nohup sudo python  adjToNetwork.py exam.csv ')
            #run('disown')

if __name__=='__main__':
   
    f=str(sys.argv[1])
    num=int(sys.argv[2])
    os.system("python from_paths_to_vms.py %(file)s %(number)s" %{"file":f, "number":num})
    f1=open("new_edges.txt",'r')
    #f1=open(sys.argv[3])
    line=f1.readline()
    l=literal_eval(line)[:]
    print l
    e={}
    count=0
    for i in range(len(ips)):
        e[i]=ips[i]

    l=[(edge[0],edge[1],e[edge[2]],e[edge[3]]) for edge in l] 
    file = open("edges_mininet.txt",'w+')
    for item in l:
        print>>file, item
    file.close()
    f1.close()
    execute(connection)
    """
    print " "
    print '###############################'
    print l
    """
    """
    """
