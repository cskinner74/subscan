#!/usr/bin/python3
#
#subscan.py
#Developer: Cody Skinner
#ver 0.0.1

import subprocess
import sys
import getopt
import re


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
            print('Includes option to extract NXDOMAIN results to a text file')
            print('usage: subscan.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ('-i', '--ifile'):
            inputfile = arg
        elif opt in ('-o', '--ofile'):
            outputfile = arg
    if not inputfile or not outputfile:
        print('usage: subscan.py -i <inputfile> -o <outputfile>')
        sys.exit()
    with open(inputfile, 'r') as i:
        line = i.readline().rstrip()
        with open(outputfile, 'a') as out:
            while line:
                out.write('\n***' + line + '***\n')
                cmd = ['host', line]
                with subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True) as proc:
                    result = proc.stdout.read()
                    out.write(str(result) + '\n')
                line = i.readline().rstrip()
    print('Output saved to ', outputfile)
    cont = input('Extract NXDOMAIN listings? (y/N): ')
    if cont == 'y' or cont == 'Y':
        nxdomain = 'nxdomain-' + outputfile
        pattern = re.compile("NXDOMAIN")
        strippat = re.compile(r'^(?:\S+\s){1}(\S+)')
        with open(outputfile, 'r') as results:
            nxdline = results.readline()
            with open(nxdomain, 'a') as o:
                while nxdline:
                    if pattern.search(nxdline) != None:
                        host = strippat.search(nxdline).group(1)
                        o.write(host + '\n')
                    nxdline = results.readline()
        print('NXDOMAIN list saved to: ', nxdomain)
    else:
        sys.exit()


if __name__ == "__main__":
    main(sys.argv[1:])
