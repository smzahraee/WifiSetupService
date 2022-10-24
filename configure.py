
import logging
import subprocess
import threading
from time import sleep
import httpserver

def run_cmd(cmd):
    try:
        subprocess.run(cmd, shell=True, check=True)
    except FileNotFoundError as exc:
        logging.critical(f"Failed to run create_ap\n{exc}")
    except subprocess.CalledProcessError as exc:
        logging.critical(
            f"Process failed because did not return a successful return code. "
            f"Returned {exc.returncode}\n{exc}"
        )


def set_wifi_enable(status=True):
    if status == True:
        run_cmd("nmcli radio wifi on")
    else:
        run_cmd("nmcli radio wifi off")


def run_access_point():
    set_wifi_enable(False)
    sleep(2)
    run_cmd("rfkill unblock all")    
    run_cmd("./create_ap/create_ap -n ap_name AP1 password")


def set_wifi_apn_password(apn=None, password=None):
    set_wifi_enable(False)
    sleep(2)
    set_wifi_enable(True)
    sleep(2)
    run_cmd("nmcli d wifi list --rescan yes")
    run_cmd("nmcli d wifi connect "+apn+" password "+password)


def wait_for_net_wifi_settings(ap_daemon):
    logging.debug("getting wifif settings\n\r")
    while True:
        logging.debug("wait for settings...\n\r")
        sleep(10)
        # ap_daemon.stop()
        set_wifi_apn_password("AndroidAP6", "123456789")


# Main starting point of daemon
format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.DEBUG,
                    datefmt="%H:%M:%S")
threading.Thread(target=httpserver.run_redirect_server, daemon=True).start()
threading.Thread(target=httpserver.run_web_api, daemon=True).start()

ap_daemon = threading.Thread(target=run_access_point, daemon=True).start()

wait_for_net_wifi_settings(ap_daemon)
