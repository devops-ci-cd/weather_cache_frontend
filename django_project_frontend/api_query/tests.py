from django.test import TestCase
from time import time
from os import getenv

# Create your tests here.

def stress(x):
    t = time() + 60*float(getenv('STRESS_MINS'))
    while time() < t:
        x*=x

