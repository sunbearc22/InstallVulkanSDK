#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

# A Python 3.6 script to install LunarG's Vulkan SDK in Ubuntu 18.04.
# Author      : sunbearc22
# Created on  : 2018-07-27
# Modified on : 2018-08-13 
# Modified on : 2020-06-19  Added SDK versions 1.1.121.1 to 1.2.141.2

import getpass
import textwrap
import sys
from pathlib import Path
import os
import os.path
import requests
import subprocess
import platform
import tarfile
import concurrent.futures as cf
import functools
import threading
import time

#=================
# Global Variables
#=================
SDKS_TAR_GZ = ( '1.2.141.2', '1.2.135.0', '1.2.131.2', '1.2.131.1',
                '1.1.130.0', '1.1.126.0', '1.1.121.1',
	        '1.1.114.0', '1.1.108.0', '1.1.106.0', '1.1.101.0', '1.1.97.0',
                 '1.1.92.1',  '1.1.85.0',  '1.1.82.1',  '1.1.82.0', '1.1.77.0', )
SDKS_RUN    = ( '1.1.73.0', '1.1.70.1', '1.1.70.0', '1.0.68.0', '1.0.65.0', 
                '1.0.61.1', '1.0.61.0', '1.0.57.0', '1.0.54.0', '1.0.51.0',
                '1.0.49.0', '1.0.46.0', '1.0.42.2', '1.0.39.1', '1.0.39.0',
                '1.0.33.0', '1.0.30.0', '1.0.26.0', '1.0.24.0', '1.0.21.1',
                '1.0.21.0', '1.0.17.0', '1.0.13.0', '1.0.11.0',  '1.0.8.0',
                 '1.0.5.0',  '1.0.3.1', )
SDKS = SDKS_TAR_GZ + SDKS_RUN
USERNAME = getpass.getuser() # Get OS username
VDIR = '~/Vulkan' # User's Vulkan directory ( default to ~/Vulkan )
# UBUNTU_VERSION  # version of Ubuntu
# VERSION         # LunarG SDK version
# IURL            # LunarG SDK Installer URL
# INAME           # LunarG SDK Installer Name
# IDIR            # LunarG SDK Installer Directory ( default to VDIR/Installers )
# IFULLNAME       # LunarG SDK Installer full path ( default to VDIR/Installers/INAME ) )
# PERMISSION      # Allow upgrading of system packages and installing of Vulkan prerequisite packages 

#==========
# Functions
#==========
def check_system_platform_and_Ubuntu_distribution():
    global UBUNTU_VERSION
    if not 'Linux' in platform.system():
        sys.exit( print( '    Quit: Non Linux System Platform detected.' ) )
    linux_distr = platform.linux_distribution()
    if not 'Ubuntu' in linux_distr:
        sys.exit( print( '    Quit: Non Ubuntu distribution detected.' ) )
    if '18.04' in linux_distr:
        UBUNTU_VERSION = '18.04'
    elif '16.04' in linux_distr:
        UBUNTU_VERSION = '16.04'
    else:
        sys.exit( print( f'    Quit: Ubuntu {UBUNTU_VERSION} is not supported.' ) )
        

def draw_program_header():
    user_border = '=' * len(USERNAME)
    border = f'================================{user_border}==================='
    print( border )
    print( f"Installing LunarG Vulkan SDK in {USERNAME}'s local directory." )
    print( border )


def get_global():
    global VERSION, VDIR, IDIR, IURL, INAME, IFULLNAME
    VERSION = get_sdk_version()
    VDIR, IDIR = get_vulkan_and_installer_dirs()
    IURL, INAME, IFULLNAME = get_installer_url_name_fullname()


def get_sdk_version():
    print( 'Available SDKs:' )
    sdks = " ".join( f'{x:>10s}' for x in SDKS )
    sdks = textwrap.fill( sdks, width=80, initial_indent='  ',
                          subsequent_indent='    ' )
    print(sdks)
    count = 0
    while True:
        count += 1
        version = input( f'Enter the SDK you want (e.g. 1.0.61.1): ').strip()
        if version in SDKS:
            return version
        if count == 3:
            sys.exit( print( 'Quit: >3 failed attempts' ) ) # Max. 3 attempts


def get_vulkan_and_installer_dirs():
    print()
    while True:
        try: 
            vdir = input( f'Enter your local Vulkan directory (defaults to ~/Vulkan): ').strip()
            if vdir == '':
                vdir = VDIR                   # use default directory if no entry is given
            vdir = Path( vdir ).expanduser()  # converts `~` to `/home/user` if `~` is present
        except PermissionError:
            print( "PermissionError. The directory must be inside your home directory (i.e. inside ~/ )." )
        else:
            make_dir( vdir )
            break
    idir = vdir / 'Installers'
    print( f'\nVulkan SDK Installer will be downloaded to {idir}.' )
    make_dir( idir )
    return vdir, idir
        

def make_dir( directory ):
    try:
        Path( directory ).mkdir( mode=0o777, parents=True, exist_ok=False )
    except FileExistsError:
        print( f'{directory} exist.' )
    else:
        print( f'{directory} was created.' )


def get_installer_url_name_fullname():
    if VERSION in SDKS_TAR_GZ:
        name = f'vulkansdk-linux-x86_64-{VERSION}.tar.gz'
    elif VERSION in SDKS_RUN:
        name = f'vulkansdk-linux-x86_64-{VERSION}.run'
    #url = f'https://sdk.lunarg.com/sdk/download/{VERSION}/linux/{name}?Human=true'
    url = f'https://sdk.lunarg.com/sdk/download/{VERSION}/linux/{name}'
    fullname = IDIR / name
    return url, name, fullname
                

def get_PERMISSION():
    global PERMISSION
    print( f'\nSee https://vulkan.lunarg.com/doc/view/latest/linux/getting_started.html#user-content-ubuntu-distributions-1804-and-1604' )
    while True:
        permission = input( f'Allow upgrading of system packages and installing of Vulkan prerequisite packages (y/n)? ' )
        if permission == 'y':
            PERMISSION = True
            break
        elif permission == 'n':
            PERMISSION = False
            break


def get_SDK():
    '''Download Vulkan SDK Installer to VDIR.'''
    if Path( IFULLNAME ).exists():
        print()
        count = 0
        while True:
            count += 1
            replace = input( f'SDK {VERSION} already exist in {VDIR}. Replace it (y/n)? ' )
            if replace == 'y':
                Path( IFULLNAME ).unlink() # delete old SDK
                break
            elif replace == 'n':
                return False
            else:
                if count == 3:
                    sys.exit( print( 'Quit: >3 failed attempts' ) ) # Max. 3 attempts
    return True #Whether IFULLNAME exist or not, return True to allow downloading of file.
    

def download_sdk( url, installerfullname ):
    print( f'\nProcess {os.getpid()} {threading.current_thread()} Downloading SDK...' )
    r = requests.get( url )
    #response less than 400 response, open in binary mode and write sdk to user defined vulkan directory
    if r.ok: 
        with open( installerfullname, "wb" ) as file:
            file.write( r.content )
    else:
        sys.exit( print( f'Quit: requests_status_code={r.status_code}' ) )
    print( f'\nProcess {os.getpid()} {threading.current_thread()} SDK {VERSION} Installer has been downloaded to {VDIR}.' )
    return True


def setup_system_and_prerequisite_packages():
    '''Update and upgrade Linux system packages and install Vulkan prerequisite_packages.'''
    print( '\nUpdating and Upgrading Linux System Packages and install Vulkan prerequisite_packages....' )
    future = 1
    a1 = apt_get_update()       #pkexec apt-get update
    a2 = apt_get_dist_upgrade() #pkexec apt-get dist-upgrade
    a3 = install_prerequisite_packages()
    if not a1 and not a2 and not a3:
        sys.exit( print( f'Quit: setup_system_and_prerequisite_packages() failed.' ) )
    return True


def call_subprocess_Popen( cmd, cwd=None ):
    with subprocess.Popen( cmd, bufsize=1, universal_newlines=True, cwd=cwd,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE ) \
                           as result:
        for line in result.stdout:
            print( line, end='' )
        for line in result.stderr:
            print( line, end='' )
    if result.returncode != 0:
        raise subprocess.CalledProcessError( result.returncode, result.args )
    else:
        return True


def apt_get_update():
    print( f'\nProcess {os.getpid()} {threading.current_thread()} sudo apt-get -y update' )
    cmd = [ 'apt-get', '-y', 'update' ]
    if UBUNTU_VERSION in '18.04':
        cmd.insert( 0, 'pkexec' )
    else:
        cmd.insert( 0, 'sudo' )
    if call_subprocess_Popen( cmd ):
        return True
    else:
        return False


def apt_get_dist_upgrade():
    print( f'\nProcess {os.getpid()} {threading.current_thread()} sudo apt-get -y dist-upgrade' )
    cmd = [ 'apt-get', '-y', 'dist-upgrade' ]
    if UBUNTU_VERSION in '18.04':
        cmd.insert( 0, 'pkexec' )
    else:
        cmd.insert( 0, 'sudo' )
    if call_subprocess_Popen( cmd ):
        return True
    else:
        return False


def install_prerequisite_packages():
    print( f'\nProcess {os.getpid()} {threading.current_thread()} Installing Prerequisite Packages....' )
    cmd = [
        'apt-get', '-y', 'install', 'libglm-dev', 'cmake', 'libxcb-dri3-0',
        'libxcb-present0', 'libpciaccess0','libpng-dev', 'libxcb-keysyms1-dev',
        'libxcb-dri3-dev', 'libx11-dev', 'g++', 'gcc', 'g++-multilib',
        'libmirclient-dev', 'libwayland-dev', 'libxrandr-dev', 'libxcb-ewmh-dev',
        'git', 'libpython3.6', 'bison' ]
    if UBUNTU_VERSION == '18.04':
        vkconfig_pkgs = ['qt5-default', 'qtwebengine5-dev' ]
        cmd.insert( 0, 'pkexec' )
    elif UBUNTU_VERSION == '16.04':
        vkconfig_pkgs = ['qt5-default' ]
        cmd.insert( 0, 'sudo' )
    cmd.extend( vkconfig_pkgs )
    if call_subprocess_Popen( cmd ):
        return True
    else:
        return False


def install_sdk():
    print( f'\nProcess {os.getpid()} Thread {threading.current_thread()} install_sdk()')
    install_dir = VDIR / 'VulkanSDK'
    if VERSION in SDKS_TAR_GZ:
        with tarfile.open( name=IFULLNAME, mode='r:gz' ) as f:
            print( f'Uncompressing LunarG Vulkan SDK...' )   
            f.extractall( path=install_dir )
    else:
        Path( IFULLNAME ).chmod( 33212 ) #Make SDK .run file executable by owner
        cmd = ['/bin/bash', IFULLNAME  ]
        if not call_subprocess_Popen( cmd, cwd=VDIR ):
            sys.exit( print( f'Quit: Failed to install LunarG Vulkan SDK' ) )
    print( f'SDK {VERSION} is installed in directory {install_dir}.' )
    return True


def show_end_notice():
    folder = VDIR / 'VulkanSDK' / VERSION # SDK Directory
    print()
    print( f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print( f"                   End of installVulkanSDK.py")
    print( f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print() 
    print( f" 1. To uninstall the SDK, simply remove your local installation\n"\
	   f"    directory. e.g.\n"\
           f"     rm -rf {folder}\n" )
    print( f" 2. Set up the runtime environment by issuing this command:\n"\
           f"     source {folder / 'setup-env.sh'}\n"\
           f"    This setting is temporary; only last in your current shell\n"\
           f"    session.\n" )
    print( f" 3. Build the Helper Scripts on examples, samples, and tools to.\n"\
           f"    learn more about Vulkan.\n")
    print( f" 4. Build SPIRV-Tools, SPIRV-Cross, and LunarG's\n"\
           f"    Vulkan Installation Analyzer (VIA).\n")
    print( f" 5. Learn to Trace and Replay.\n")
    print( f" 6. Enable Validation, Utility and Other Layers.\n")
    print( f" 7. Learn to debug an example application with gdb.\n")
    print( f"             Enjoy the power of VULKAN {VERSION}.")
    print( f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    

def main():
    print( f'Process {os.getpid()} Thread {threading.current_thread()}' )
    check_system_platform_and_Ubuntu_distribution()
    draw_program_header()
    get_global()
    get_PERMISSION()
    if PERMISSION:
        get_sdk = get_SDK()
        start = time.time()
        if get_sdk:
            #print( '### Get SDK and get and setup packages.' )
            with cf.ThreadPoolExecutor(max_workers=3) as executor:
            #with cf.ProcessPoolExecutor(max_workers=3) as executor:
                futures = [ executor.submit( functools.partial( download_sdk, IURL, IFULLNAME ) ),
                            executor.submit( setup_system_and_prerequisite_packages ) ]
                cf.wait( futures, return_when=cf.ALL_COMPLETED )
                f0r = futures[0].result()
                f1r = futures[1].result()                   
                print( f'\nSDK {VERSION} Downloaded = {f0r}   and   '\
                       F'System pkgs and Vulkan prerequisite pkgs setup = {f1r}' )
            end = time.time()
        else:
            #print( '### Get and setup packages.' )
            setup_system_and_prerequisite_packages()
            print( f'\nSystem pkgs and Vulkan prerequisite pkgs setup = True.' )
            end = time.time()
        print( f'\nSetup Time: {end-start:.2f} sec' )

    else:
        sys.exit( print( f'Quit: {USERNAME} disallowed.' ) )
        #pass
    start = time.time()
    install_sdk()
    end = time.time()
    print( f'\nInstall Time: {end-start:.2f} sec' )
    show_end_notice()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit( print( f'\nQuit: {USERNAME} terminated program.' ) )
