from django.shortcuts import render
from robot.daka.consumer import consume
from robot.daka.producer import producer
import threading
# Create your views here.


threading.Thread(target=producer).start()
threading.Thread(target=consume).start()
