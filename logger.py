# 5th march 2017 sunday
# file=logger.py        lang=python3.5.2

'''
about the plugin
    for debugging
'''
def global_log():
    global log
    def log(str):
        print(str)
