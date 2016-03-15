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

parser = argparse.ArgumentParser(description='Create PBKDF2 passwords for user creation with Puppet/Chef for OS X 10.8 and later. The created password will have a salt of a random string with defined length and will use defined digest, with a desired derived length.')
parser.add_argument('Password', help="Password to create the hash from")
parser.add_argument('-sl','--StringLength', help="Length of the random string (default 32)", type=int, default=32, nargs=1)
parser.add_argument('-i','--iterations', help="Number of iterations, min. 25000", type=int, default=25000)
parser.add_argument('-d', '--digest', help="Digest to be used. Defaults to sha512", default='sha512', choices=['sha512', 'sha384', 'sha256'])
parser.add_argument('-dl', '--DerivedLength', type=int, default=128, help="Desired derived key lenght, default 128")
parser.add_argument('-v','--verbose', action='count', help="Increase the verbosity")
#parser.add_argument
args = parser.parse_args()

if args.iterations < 25000:
    args.iterations = 25000

if args.verbose:
    print "PBKDF2 hash will be created with the following arguments"
    print 'Password:', args.Password
    print 'Salt string length:', args.StringLength
    print 'Number of iterations:', args.iterations
    print 'Defined digest:', args.digest
    print 'Derived Lenght:', args.DerivedLength

passwordSalt = os.urandom(args.StringLength)
passwordHash = hashlib.pbkdf2_hmac(args.digest, args.Password, passwordSalt, args.iterations, args.DerivedLength)

hexPasswordSalt = binascii.hexlify(passwordSalt)
hexPasswordHash = binascii.hexlify(passwordHash)

print 'Password hash: ', hexPasswordHash
print 'Salt hash: ', hexPasswordSalt
