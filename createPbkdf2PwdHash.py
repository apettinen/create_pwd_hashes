#!/usr/bin/python
# -*- coding: utf-8 -*-
# This creates PBKDF2 Hashed passwords to be used with Puppet/Chef
# when creating users for OS X 10.8 onwards
# Antti Pettinen
# TUT IT Services / TUTMac
import os
import argparse
#import sys
import binascii
import hashlib

parser = argparse.ArgumentParser(description='Interactively create PBKDF2 passwords for user creation with Puppet/Chef for OS X 10.8 onwards. The created password will have a salt of 32-bit random string and will use SHA-512 digest, with a derived length of 128.')
args = parser.parse_args()

desiredPassword = raw_input('Please enter the desired password: ')
iterations = 0
while iterations < 25000:
    try:
        iterations = int(raw_input('Please provide the amount of iterations (min 25000): '))
    except ValueError:
        iterations = 25000
passwordSalt = os.urandom(32)
hexPasswordSalt = binascii.hexlify(passwordSalt)
passwordHash = hashlib.pbkdf2_hmac('sha512', desiredPassword, passwordSalt, iterations, 128)
hexPasswordHash = binascii.hexlify(passwordHash)
print 'Password hash: ', hexPasswordHash
print 'Salt hash: ', hexPasswordSalt
