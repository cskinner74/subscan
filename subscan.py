#!/usr/bin/python3
#
#subscan.py
#Developer: Cody Skinner
#ver 0.0.1

import subprocess
import sys
import getopt


def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, 'hi:o:',['ifile=','ofile='])
    except getopt.GetoptError:
        print ('usage: subscan.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('subscan.py')
            print('Tool for checking host information for a list of domains')
            print('usage: subscan.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ('-i', '--ifile'):
            inputfile = arg
        elif opt in ('-o', '--ofile'):
            outputfile = arg
    if not inputfile or not outputfile:
        print('usage: subscan.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    with open(inputfile) as i:
        line = i.readline().rstrip()
        with open(outputfile, 'a') as out:
            while line:
                out.write('\n***' + line + '***\n')
                cmd = ['host', line]
                with subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True) as proc:
                    result = proc.stdout.read()
                    out.write(str(result) + '\n')
                line = i.readline().rstrip()

if __name__ == "__main__":
    main(sys.argv[1:])
