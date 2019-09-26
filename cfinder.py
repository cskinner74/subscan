#!/usr/bin/python3
#cfinder.py
#Developer: Cody Skinner
#ver 0.1.1

import subprocess
import sys
import getopt
import re

def main(argv):
    inputfile = ''
    outputfile = ''
    verbose = False
    try:
        opts, args = getopt.getopt(argv, 'hi:o:v',['ifile=','ofile=','verbose='])
    except getopt.GetoptError:
        print('usage: cfinder.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('cfinder.py')
            print('Tool for finding hanging CNAME entries')
            print('usage: cfinder.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ('-i', '--ifile'):
            inputfile = arg
        elif opt in ('-o','--ofile'):
            outputfile = arg
        elif opt in ('-v','--verbose'):
            verbose = True
    if not inputfile or not outputfile:
        print('usage: cfinder.py -i <inputfile> -o <outputfile>')
        sys.exit()
    print('Checking for CNAME entires in DNS results')
    print('Please be patient, this may take a while with long lists')
    with open(inputfile, 'r') as i:
        line = i.readline().rstrip()
        with open(outputfile, 'a') as out:
            while line:
                if verbose:
                    print('Checking ',str(line))
                cmd = ['dig', line]
                pull = ['grep','CNAME']
                p1 = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True)
                p2 = subprocess.Popen(pull, stdin=p1.stdout, stdout=subprocess.PIPE, text=True)
                p1.stdout.close()
                result = p2.communicate()[0]
                if result != '':
                    print(str(result))
                    out.write(str(result))
                line = i.readline().rstrip()
    print('Output saved to ', outputfile)

if __name__ == "__main__":
    main(sys.argv[1:])
