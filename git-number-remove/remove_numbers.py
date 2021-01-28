#!/usr/bin/env python3 
# This program will eliminate all odd numbers from a specific file
# one at a time, creating a commit for each removal.

import sys
import subprocess
import argparse

parser = argparse.ArgumentParser(description='eliminate odd numbers from a file and use git')
parser.add_argument('filename', metavar='filename', help='The file path to process')
parser.add_argument('--use_branches', dest='use_branches', action='store_true', 
    help='use branches to eliminate numbers')
parser.add_argument('--default_branch', default='master', help='default branch')


args = parser.parse_args()

def eliminate_first_odd(fn, already_eliminated):
    lines = open(fn, 'r').readlines()
    for lineno, line in enumerate(lines):
        int_value = int(line)
        is_odd = ((int_value % 2) == 1)
        if is_odd and (int_value not in already_eliminated):
            lines = lines[:lineno] + lines[lineno+1:]
            already_eliminated.add(int_value)
            open (fn, 'w').write(''.join(lines))
            return int_value
    return None

def commit_change(fn, num):
    message = ('commit change for removal of %d' % num)
    subprocess.run(['git', 'commit', '-m', message, fn])

def create_branch(num):
    subprocess.run(['git', 'checkout', '-b', 'eliminate_%d' % num])

def switch_branch(branch_name):
    subprocess.run(['git', 'checkout', branch_name])

if __name__ == '__main__':
    fn = args.filename
    already_eliminated = set()
    while True:
        # 1. remove the first odd number in the file
        eliminated_number = eliminate_first_odd(fn, already_eliminated)

        # if None is returned, there are no odd numbers in the file
        if eliminated_number is None:
            break
        
        if not args.use_branches:
            # 2. commit, into the current branch, the change removing one odd number        
            commit_change(fn, eliminated_number)
        else:
            create_branch(eliminated_number)
            commit_change(fn, eliminated_number)
            switch_branch(args.default_branch)


