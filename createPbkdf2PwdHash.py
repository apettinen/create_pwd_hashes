#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=C0301, C0103
"""Create PBKDF2 hashed passwords"""
# This creates PBKDF2 Hashed passwords to be used with e.g. Puppet or Chef
# when creating users for OS X 10.8 onwards
# Antti Pettinen
# TUT IT Services / TUTMac
import os
import argparse
#import sys
import binascii
import hashlib

def createHashes(password, stringLength, iterations, digest, derivedLength):
    """Main function: all the lifting happens here"""
    # check that input values are sane (switch to at least the default)
    if iterations < 25000:
        iterations = 25000

#    if
    #else if args.iterations is None:

    passwordSalt = os.urandom(stringLength)
    passwordHash = hashlib.pbkdf2_hmac(digest, password, passwordSalt, iterations, derivedLength)

    hexPasswordSalt = binascii.hexlify(passwordSalt)
    hexPasswordHash = binascii.hexlify(passwordHash)
    return hexPasswordHash, hexPasswordSalt

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Create PBKDF2 passwords for user creation with Puppet/Chef for OS X 10.8 and later. The created password will have a salt of a random string with defined length and will use defined digest, with a desired derived length.')
    parser.add_argument('-pwd', '--Password', help="Password to create the hash from", type=str)
    parser.add_argument('-sl', '--StringLength', help="Length of the random string (default 32)", type=int, default=32, nargs=1)
    parser.add_argument('-i', '--iterations', help="Number of iterations, min. 25000", type=int, default=25000)
    parser.add_argument('-d', '--digest', help="Digest to be used. Defaults to sha512", default='sha512', choices=['sha512', 'sha384', 'sha256'])
    parser.add_argument('-dl', '--DerivedLength', type=int, default=128, help="Desired derived key length, default 128")
    parser.add_argument('-v', '--verbose', action='count', help="Increase the verbosity")
    #parser.add_argument
    args = parser.parse_args()

    # stringLength, iterations, digest, derivedLength
    if args.Password is None:
        args.Password = raw_input('Please enter the desired password: ')

    #if args.

        # desiredPassword = raw_input('Please enter the desired password: ')
        # iterations = 0
        # while iterations < 25000:
        #     try:
        #         iterations = int(raw_input('Please provide the amount of iterations (min 25000): '))
        #     except ValueError:
        #         iterations = 25000
        # passwordSalt = os.urandom(32)
        # hexPasswordSalt = binascii.hexlify(passwordSalt)

    outPwdHash, outPwdSalt = createHashes(args.Password, args.StringLength, args.iterations, args.digest, args.DerivedLength)

    if args.verbose:
        print "PBKDF2 hash will be created with the following arguments"
        print 'Password:', args.Password
        print 'Salt string length:', args.StringLength
        print 'Number of iterations:', args.iterations
        print 'Defined digest:', args.digest
        print 'Derived length:', args.DerivedLength

    print 'Password hash: ', outPwdHash
    print 'Salt hash: ', outPwdSalt

if __name__ == "__main__":
    main()
