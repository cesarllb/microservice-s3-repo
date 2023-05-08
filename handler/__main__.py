from bus_publisher.builder import buss
from bus_publisher.inyect import config

if __name__ =='__main__':
    config()
    db = buss()
    db.start_consumer()