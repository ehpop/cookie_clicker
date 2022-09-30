import sys
import subprocess
import gui_auto_clicker

# implement pip as a subprocess:
subprocess.check_call([sys.executable, '-m', 'pip', 'install',
'PySimpleGUI', 'pyautogui'])

# process output with an API in the subprocess module:
reqs = subprocess.check_output([sys.executable, '-m', 'pip',
'freeze'])
installed_packages = [r.decode().split('==')[0] for r in reqs.split()]

print(installed_packages)

def main():
    gui_auto_clicker.run()


if __name__ == '__main__':
    main()