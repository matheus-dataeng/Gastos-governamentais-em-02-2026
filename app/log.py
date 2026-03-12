import logging as log 

def logger_setup():
    log.basicConfig(
        level= log.INFO,
        format= "%(asctime)s / %(levelname)s / %(name)s / %(message)s"
        
    )