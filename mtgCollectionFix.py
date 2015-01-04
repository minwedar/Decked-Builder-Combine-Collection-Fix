#!/usr/bin/env python

# Author: Todd Burke  (minwedar@gmail.com)
# Creation Date: Summer 2014
# Discription: This simply combines two Decked Builder collections into one.  The
#              current problem I was having was that you couldn't simply open the
#              two text files and append one to the other because there would 
#              sometimes be multiple and then conflicting number for the quantity
#              of a certain card.  This script combines duplicates so that when
#              opened in Decked Builder App it actually shows up correctly.
#
# Usage: This is a quick hack, so basically you start with simply appending any
#        number of collections to a single file.  Do this however you wish.  My
#        preference is to just keep `cat my.coll2 >> new.coll2` until you have
#        all the collections you want into the one big collection.  Then run the
#        script.  It will print out how many duplicate lines it fixed if any.
#        Please, please backup your collection before running this script.  
#
#        python mtgCollectionFix.py -i appended.coll2 -o new.coll2


#import os, sys, shutil, re, optparse, time
import optparse
import re

class mtgData():
    id = 0
    r = 0
    f = 0

    def _init_(self):
        self.id = 0
        self.r = 0
        self.f = 0

    def add_r(self, count):
        self.r = self.r + int(count)

    def add_f(self, count):
        self.f = self.f + int(count)


def main():
    
    #Set up some command line options
    p = optparse.OptionParser()
    p.add_option('--input', '-i', default="All.coll2", help="Input file.")
    p.add_option('--output', '-o', default="new.coll2", help="Output file.")
        
    global options  #options used in other functions below  
    options, arguments = p.parse_args()


    try:
        f = open(options.input, 'r')

        fileContents = f.read()
        f.close()

    except Exception, e:
        print 'ERROR: %s' % e

    lines = fileContents.split('\n')

    reID = re.compile('(^..-.-.id:.)(.*)')
    reR = re.compile('(^....-.r:.)(.*)')
    reF = re.compile('(^....-.f:.)(.*)')

    objList = []
    mtgDataList = []
    currentCard = None
    sourceIDCount = 0
    dupFound = False
    dupCounter = 0
    
    for i,line in enumerate(lines):
        #if i > len(lines):   # probably someday need to take care when there isn't blank lines at the end.
        #    break

        if reID.findall(line):
            # Create card object for each one found
            sourceIDCount += 1
            currentCard = mtgData()

            currentCard.id = reID.findall(line)[0][1]
            #print "ID: %s:%s" % (i, currentCard.id)
            objList.append(currentCard.id)  # Test to see what all ID have dups

            if reR.findall(lines[i+1]):
                currentCard.add_r(int(reR.findall(lines[i+1])[0][1]))
                #print "Regular Count: %s" % currentCard.r

            elif reF.findall(lines[i+1]):
                currentCard.add_f(int(reF.findall(lines[i+1])[0][1]))
                #print "Foil Count: %s" % currentCard.f

            if reF.findall(lines[i+2]):
                currentCard.add_f(int(reF.findall(lines[i+2])[0][1]))
                #print "Foil Count: %s" % currentCard.f

            # Search current entries for this ID
            dupFound = False
            for item in mtgDataList:
                if item.id == currentCard.id:
                    #print "Duplicate found"
                    dupFound = True
                    dupCounter += 1

                    #print "Before: %s: r:%s f:%s" %(item.id, item.r, item.f)

                    if (currentCard.r):
                        item.add_r(currentCard.r)

                    if (currentCard.f):
                        item.add_f(currentCard.f)

                    #print "After: %s: r:%s f:%s" %(item.id, item.r, item.f)

                    break

            if not dupFound:
                mtgDataList.append(currentCard)

    print "Sanity Check:"
    print "Total number of IDs picked up from source file: %s" % sourceIDCount
    print "Length of mtgDataList after processing: %s" % len(mtgDataList)
    print "Difference: %s" % (sourceIDCount - len(mtgDataList))
    dups = duplicatesInList(objList)
    print "Duplicate entry IDs that where found: %s" % dupCounter
    print "The difference between the two list and how many had duplicates should be equal.\n"

    # objList.sort()
    # print "Duplicates: %s\n" % len(dups)
    # print dups

    # Write list out to a file to create the collection
    try:
        f = open(options.output, 'w')

        f.writelines("doc:\n- version: 1\n- items:\n")

        for card in mtgDataList:
            f.writelines("  - - id: %s\n" % card.id)
            f.writelines("    - r: %s\n" % card.r)
            f.writelines("    - f: %s\n" % card.f)

        f.writelines("\n\n")    
        f.close()

    except Exception, e:
        print 'ERROR: %s' % e


def duplicatesInList(l):
    return list(set([x for x in l if l.count(x) > 1]))


if __name__ == "__main__":
   main()