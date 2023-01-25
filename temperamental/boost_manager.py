"""Simple module to handle CPU Boost and helpers for button usage"""

def status():
    with open("/sys/devices/system/cpu/cpufreq/boost", "r", encoding='utf-8') as boost:
        boost_status = (int(boost.read()) == 1)
    return boost_status

def enable_boost():
    if status():
        return
    with open("/sys/devices/system/cpu/cpufreq/boost", "r+", encoding='utf-8') as boost:
        boost.write("1")

def disable_boost():
    if not status():
        return
    with open("/sys/devices/system/cpu/cpufreq/boost", "r+", encoding='utf-8') as boost:
        boost.write("0")


class EnableBoostHelper():

    def do_action(self):
        enable_boost()

class DisableBoostHelper():

    def do_action(self):
        disable_boost()
