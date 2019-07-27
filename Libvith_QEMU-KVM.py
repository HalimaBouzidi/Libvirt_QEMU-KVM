# ===========================================
# TP VCL: Bouzidi Halima & Djebrouni Yasmine - SIQ3 .
# 2018/2019.
# used libraries : libvirt, sys, os.
# ===========================================

from __future__ import print_function
import sys
import libvirt
import sys, os

# Main definition - constants
menu_actions  = {}  
connection = libvirt.open('qemu:///system')
lsNact=connection.listDefinedDomains()
lsAct=connection.listDomainsID()
# =======================
#     Libvirt FUNCTIONS
# =======================

def infoHost():

    print('Hostname : ' + connection.getHostname())
    vcpus = connection.getMaxVcpus(None)
    print('Maximum support virtual CPUs: '+str(vcpus))
    nodeinfo = connection.getInfo()
    print('Model: '+str(nodeinfo[0]))
    print('Memory size: '+str(nodeinfo[1])+'MB')
    print('Number of CPUs: '+str(nodeinfo[2]))
    print('MHz of CPUs: '+str(nodeinfo[3]))
    print('Number of NUMA nodes: '+str(nodeinfo[4]))
    print('Number of CPU sockets: '+str(nodeinfo[5]))
    print('Number of CPU cores per socket: '+str(nodeinfo[6]))
    print('Number of CPU threads per core: '+str(nodeinfo[7]))
    #Virtualization type
    print('Virtualization type: '+connection.getType())
    raw_input("Press Enter to continue...")

def vmInfo(domainName):
    #opening the connection
    dom = connection.lookupByName(domainName)
    if dom == None:
        print('Can''t get the domain object', file=sys.stderr)
        exit(1)
    print("Name : "+ domainName)
    id = dom.ID()
    if id == -1:
        print('No ID because it is not running.')
    else:
        print('The ID of the domain is ' + str(id))
    osType = dom.OSType()
    print("OS type = '" + osType + "'")
    state, maxmem, mem, cpus, cput = dom.info()
    print('Max Memory = ' + str(maxmem))
    print('Memory = ' + str(mem))
    print('CPU number = ' + str(cpus))
    print('CPU time (ns) =' + str(cput))
    flag = dom.isActive()
    if flag == True:
        print('VM is active.')
    else:
        print("VM is not active.")
    state, reason = dom.state()

    if state == libvirt.VIR_DOMAIN_NOSTATE:
        print("l'etat est VIR_DOMAIN_NOSTATE")
    elif state == libvirt.VIR_DOMAIN_RUNNING:
        print("l'etat est VIR_DOMAIN_RUNNING")
    elif state == libvirt.VIR_DOMAIN_BLOCKED:
        print("l'etat est VIR_DOMAIN_BLOCKED")
    elif state == libvirt.VIR_DOMAIN_PAUSED:
        print("l'etat est VIR_DOMAIN_PAUSED")
    elif state == libvirt.VIR_DOMAIN_SHUTDOWN:
        print("l'etat est VIR_DOMAIN_SHUTDOWN")
    elif state == libvirt.VIR_DOMAIN_SHUTOFF:
        print("l'etat est VIR_DOMAIN_SHUTOFF")
    elif state == libvirt.VIR_DOMAIN_CRASHED:
        print("l'etat est VIR_DOMAIN_CRASHED")
    elif state == libvirt.VIR_DOMAIN_PMSUSPENDED:
        print("l'etat est VIR_DOMAIN_PMSUSPENDED")
    else:
        print("l'etat est unknown.")
    raw_input("Press Enter to continue...")    

def domainList():
    i = 1
    #opening the connexion
    domainNames = []
    #getting the list of active and inactive domains
    domains = connection.listAllDomains(0)
    if len(domains) != 0:
        for domain in domains:
            print('%r.  %s'%(i,domain.name()))
            i=i+1
            domainNames.append(domain.name())
    else:
        print('  None')
    return domainNames

def domainStart(domainName):
    if connection == None:
        print('Can''t open connection to qemu:///system', file=sys.stderr)
        exit(1)
    dom = connection.lookupByName(domainName)
    if dom == None:
        print('Can''t get the domain object', file=sys.stderr)
        exit(1)
    dom.create()
    print("the VM is running")

def domainDestruction(domainName):
    dom = connection.lookupByName(domainName)
    dom.destroy()
    print("the VM is shutdown")

def getIP(domainName):
# The qemu-guest-agent must be installed on guest
            dom = connection.lookupByName(domainName)
            if dom == None:
               print("Can''t get the domain object")
            ifaces = dom.interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT, 0)
            print("The interface IP addresses:")
            for (name, val) in ifaces.iteritems():
               print("Interface  :"+name)
               if val['addrs']:
                  for ipaddr in val['addrs']:
                     if ipaddr['type'] == libvirt.VIR_IP_ADDR_TYPE_IPV4:
                        print(" IPV4_address : "+ipaddr['addr'])
                     elif ipaddr['type'] == libvirt.VIR_IP_ADDR_TYPE_IPV6:
                        print(" IPV6_address : " +ipaddr['addr'])

# =======================
#     MENUS FUNCTIONS
# =======================
 
# Main menu
# Main menu
def main_menu():
    os.system('clear')
    
    print("Welcome to the virtMaster,\n")
    print("Please select one of the below options: \n")
    print("1. Informations of the host")
    print("2. VMs list")
    print("3. Run a VM")
    print("4. Shutdown a VM")
    print("5. VM IP address")
    print("\n0. Quit")
    choice = input(" >>  ")
    exec_menu(choice)
 
    return

# Execute menu
def exec_menu(choice):
    os.system('clear')
    choice = str(choice)
    ch = choice.lower()
    if ch == '':
        menu_actions['main_menu']()
    else:
        try:
            menu_actions[ch]()
        except KeyError:
            print("Invalid selection, please try again.\n")
            menu_actions['main_menu']()
    return

# Menu 1
def menu1():
    infoHost()
    print("9. Back")
    print("0. Quit")
    choice = input(" >>  ")
    exec_menu(choice)
    return
 
 
# Menu 2
def menu2():
    domainList()
    print("9. Back")
    print("0. Quit") 
    choice = input(" >>  ")
    exec_menu(choice)
    return

# Menu 3
def menu3():
    vm_menu_start()
    print("9. Back")
    print("0. Quit") 
    choice = input(" >>  ")
    exec_menu(choice)
    return
 
# Menu 4
def menu4():
    vm_menu_destroy()
    print("9. Back")
    print("0. Quit") 
    choice = input(" >>  ")
    exec_menu(choice)
    return


# Menu 5
def menu5():

    vm_menu_ip()

    print("9. Back")
    print("0. Quit") 
    choice = input(" >>  ")
    exec_menu(choice)
    return

# Back to main menu
def back():
    menu_actions['main_menu']()
 
# Exit program
def exit():
    sys.exit()

# Info VM choice
def vm_menu_info():
    os.system('clear')
    print("Please choose the virtual machine:\n")
    domainList()
    print("\n0. Quit")
    choice = input(" >>  ")
    exec_menu_vm(choice)
    return 

# Start VM choice
def vm_menu_start():
    os.system('clear')
    print("Please choose the virtual machine:\n")
    domainList()
    print("\n0. Quit")
    choice = input(" >>  ")
    exec_menu_vm_start(choice)
    return 

# Destroy VM choice
def vm_menu_destroy():
    os.system('clear')
    print("Please choose the virtual machine:\n")
    domainList()
    print("\n0. Quit")
    choice = input(" >>  ")
    exec_menu_vm_destroy(choice)
    return 

# Destroy VM choice
def vm_menu_ip():
    os.system('clear')
    print("Please choose the virtual machine:\n")
    domainList()
    print("\n0. Quit")
    choice = input(" >>  ")
    exec_menu_vm_ip(choice)
    return 

# Execute menu VM
def exec_menu_vm(choice):
    os.system('clear')
    list = domainList()
    choice = str(choice)
    chi = int(choice)
    domainName = list[chi-1]
    ch = choice.lower()
    if ch == '':
        menu_actions['main_menu']()
    else:
        try:
            vmInfo(domainName)
        except KeyError:
            print("Invalid selection, please try again.\n")
            menu_actions['main_menu']()
    return

# Start VM
def exec_menu_vm_start(choice):
    os.system('clear')
    list = domainList()
    choice = str(choice)
    chi = int(choice)
    domainName = list[chi-1]
    ch = choice.lower()
    if ch == '':
        menu_actions['main_menu']()
    else:
        try:
            domainStart(domainName)
        except KeyError:
            print("Invalid selection, please try again.\n")
            menu_actions['main_menu']()
    return

# Destroy VM
def exec_menu_vm_destroy(choice):
    os.system('clear')
    list = domainList()
    choice = str(choice)
    chi = int(choice)
    domainName = list[chi-1]
    ch = choice.lower()
    if ch == '':
        menu_actions['main_menu']()
    else:
        try:
            domainDestruction(domainName)
        except KeyError:
            print("Invalid selection, please try again.\n")
            menu_actions['main_menu']()
    return

# ip VM
def exec_menu_vm_ip(choice):
    os.system('clear')
    list = domainList()
    choice = str(choice)
    chi = int(choice)
    domainName = list[chi-1]
    ch = choice.lower()
    if ch == '':
        menu_actions['main_menu']()
    else:
        try:
            getIP(domainName)
        except KeyError:
            print("Invalid selection, please try again.\n")
            menu_actions['main_menu']()
    return
# =======================
#    MENUS DEFINITIONS
# =======================
 
# Menu definition
menu_actions = {
    'main_menu': main_menu,
    '1': menu1,
    '2': menu2,
    '3': menu3,
    '4': menu4,
    '5': menu5,
    '9': back,
    '0': exit,
}
 
# =======================
#      MAIN PROGRAM
# =======================
 
# Main Program

if __name__ == "__main__":
    # Launch main menu
    main_menu()

    
