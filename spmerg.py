#!/usr/bin/env python
# -*- coding = utf-8 -*-

import os
import re
import sys
reload(sys)
from lxml import etree as ET

line_feed = '\n'     #replace '\n' with '\r\n' when in windows
file_encode = 'utf-8'   #source file encode
save_file_encode ='utf-8'  #saved file encode
sys.setdefaultencoding(save_file_encode) 

def split(route):
    tree = ET.parse(route)
    gpoints = tree.getroot()

    for gpoint in gpoints:
        if re.match('D[0-9]{4}', gpoint.attrib['id']):
            for gpoint_PRB in gpoint:

                if re.match('P?(R|B)', gpoint_PRB.tag):
                    elem_Rgmap = ET.Element('Rgmap')
                    for gpoint_sRB in gpoint_PRB:
                        elem_RB = ET.SubElement(elem_Rgmap, 'Note', {'No': '{0}'.format(gpoint_sRB.attrib['id'])})
                        elem_RB.text = gpoint_sRB.text.replace('\n', line_feed)
                    with open('{0}_{1}.xml'.format(gpoint.attrib['id'],gpoint_PRB.tag), mode = 'w') as f:
                        f.write(ET.tostring(elem_Rgmap, xml_declaration = True, \
                        encoding = save_file_encode, pretty_print = True).decode(save_file_encode))

                elif re.match('P{1,2}', gpoint_PRB.tag):
                    with open('{0}_{1}.TXT'.format(gpoint.attrib['id'], gpoint_PRB.tag), mode='w') as f:
                        f.write(gpoint_PRB.text.replace('\n',line_feed))

                else:
                    print "Gpoint {0}'s tag <{1}> is incorrect.".format(gpoint.attrib['id'], gpoint_PRB.tag)

        elif re.match('L[0-9]{4}', gpoint.attrib['id']):
            with open('{0}.TXT'.format(gpoint.attrib['id']),mode='w') as f:
                f.write(gpoint.text.replace('\n',line_feed))

        else:
            print "{1}: <{0}>'s Gpoint Number is not agree with the pattern('id=D1234').".format(gpoint.attrib['id'], route)


def merger(folder):

    children = ' '.join(os.listdir(folder))
    Gpoints = re.findall('D\d{4}_P.TXT', children)
    Gpoints.sort()

    elem_root = ET.Element('body')

    for Gpoint in Gpoints: 
        #elem_hr = ET.SubElement(elem_root, 'hr')
        elem_div = ET.SubElement(elem_root, 'div', {'id':'{0}'.format(Gpoint[0:5])})
        with open('{0}_P.TXT'.format(Gpoint[0:5]), encoding = file_encode) as f:
            elem_P = ET.SubElement(elem_div, 'P')
            elem_P.text = str(f.read()).rstrip()

        #find R&B of a each Gpoint and sort it in the R-B order.
        RB = re.findall('({0}_(R|B).xml)'.format(Gpoint[0:5]),children)
        if RB:
            RB.sort(reverse=True)
        for ss in RB:
            with open(ss[0], encoding=file_encode) as f:
                entries = ET.fromstring(''.join(f.readlines()[1:]))
                data = []
                for entry in entries:
                    key = entry.attrib['No']
                    data.append((key, entry))
                    data.sort()

            elem_RB = ET.SubElement(elem_div, '{0}'.format(ss[1]))
            for item in data:
                elem_SRB = ET.SubElement(elem_RB, 'S{0}'.format(ss[1]), {'No' : item[0]})
                elem_SRB.text = str(item[-1].text).rstrip()

    with open('L{0}.html'.format(Gpoints[0][1:5]), 'w') as f:
        f.write((ET.tostring(elem_root, xml_declaration = True, pretty_print = True, \
            encoding = file_encode)).decode(file_encode))

def loopfolder(folder):
    entries = os.listdir(folder)
    for entry in entries:
        if os.path.isdir(entry):
            loopfolder(folder)
        else:
            return entry

if __name__ == '__main__':

    if sys.argv[1] == 's':
        if not os.path.exists('note'):
            os.mkdir('note')
        os.chdir('./note')
        for route in sys.argv[2:]:
            os.mkdir(os.path.splitext(route)[0])
            os.chdir(os.path.splitext(route)[0])
            split('../../{0}'.format(route))
            os.chdir('../../note')
            

    elif sys.argv[1] == 'm':
        merger(sys.argv[2:])

    else:
        print('Usuage: ./spmerg.py s|m xmlfiles|folders')
