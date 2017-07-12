# -*- coding: utf-8 -*-
from __future__ import print_function
import sys

import urllib
import os
import re
import time


class alpha:
    choose = input("How would you like to see the procces?\n1 = by % \n2 = printing the text \n")
#   creating the path and the place the docs will be on your computer
    newpath = r'C:\WorkAlpha\babylonienTexts'
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    else:
        print ("you already got the files or files with the same name on your computer")
        helper = input("Are you sure you want to replace them?\n1 - yes I want to replace them\n2 - no I don't want to replace them\n")
        if helper != 1:
            exit()
    myPageUrl = []
    text_file = open(r"C:\WorkAlpha\babylonienTexts\textsUrls.txt", "w")
    print(r"urls download: (to C:\WorkAlpha\babylonienTexts\textsUrls.txt)")
    prhelp = 1.0
#   copy the urls and printing em to a txt file and to the screen
    names = ["archives-ebabbar","archives-eanna","archives-egibi","archives-nappahu","archives-murasu","autres-archives-privees"]
    for y in range(0,6):
        for x in range(1,8): # 8 because the are 8 pages in the site
            link = "http://www.achemenet.com/fr/tree/?/sources-textuelles/textes-par-langues-et-ecritures/babylonien/%s/%s/96/0#set" % (names[y], x)
            pagecode = urllib.urlopen(link)
            for x in range(0,10000): # 10000 because the page code will probably wont be longer then that
                myfile = pagecode.readline()
                if (myfile.find("Strassmaier") >= 0 or myfile.find("YOS") >= 0 or myfile.find("Wunsch") >= 0 or myfile.find("Murašu") >= 0 or myfile.find("Jursa") >= 0):
                    myPageUrl.append("http://www.achemenet.com/" + myfile.split('"')[3])
                    text_file.write("http://www.achemenet.com/" + myfile.split('"')[3] + "\n")
                    if choose == 1:
                        b = str(round((prhelp / 1834) * 100,3))
                        print('\r',end = "")
                        print(b + "%",end = "")
                        time.sleep(0.01)
                        prhelp = prhelp + 1
                    else:
                        print ("http://www.achemenet.com/" + myfile.split('"')[3])

    print ("\nfinised download the urls")
    text_file.close()


#   again creating 2 new txt files
    text_file = open(r"C:\WorkAlpha\babylonienTexts\texts.txt", "w")
    dict_text_file = open(r"C:\WorkAlpha\babylonienTexts\textsAfterTokenizatiom.txt", "w")

    prhelp = 0.0

#   the dictionary build up from the word it number and the number of times it appears in the text
    dict = {}
    counter = 0
    print(r"texts download: (to C:\WorkAlpha\babylonienTexts\texts.txt and C:\WorkAlpha\babylonienTexts\textsAfterTokenizatiom.txt)")


    for z in range(0,len(myPageUrl)): # passing over all the urls
        pagecode = urllib.urlopen(myPageUrl[z])
        if choose != 1:
            print (myPageUrl[z]) # printing the url of the text we are about to print
        text_file.write("\n" + myPageUrl[z] + "\n")
        dict_text_file.write("\n" + myPageUrl[z] + "\n")
        # helper flag
        flag = 0
        flag1 = 0
        for y in range(0, 10000): # reading all the lines in the page
            pageLine = pagecode.readline()

            if (pageLine.find("TRANSLITTERATION</div>") >= 0): flag = 1
            if (pageLine.find("BIBLIOGRAPHIE") >= 0): flag = 0
            if (flag > 0):
                if flag1 == 0:
                    pageLine = pagecode.readline()
                    pageLine = pagecode.readline()
                    flag1 = 1

                if pageLine.find("</table>") != -1:
                    break

                pageLine = pageLine.replace(',',"   ")


#               handle sub
                while ((pageLine.find('<sub>') != -1) and pageLine[pageLine.find("<sub>") + 5].isdigit()):
                    if pageLine[pageLine.find('<sub>') + 5] == '0':
                        pageLine = pageLine[:(pageLine.find('<sub>') + 5)] + "A" + pageLine[(pageLine.find('<sub>') + 6):]
                    if pageLine[pageLine.find('<sub>') + 5] == '1':
                        pageLine = pageLine[:(pageLine.find('<sub>') + 5)] + "B" + pageLine[(pageLine.find('<sub>') + 6):]
                    if pageLine[pageLine.find('<sub>') + 5] == '2':
                        pageLine = pageLine[:(pageLine.find('<sub>') + 5)] + "C" + pageLine[(pageLine.find('<sub>') + 6):]
                    if pageLine[pageLine.find('<sub>') + 5] == '3':
                        pageLine = pageLine[:(pageLine.find('<sub>') + 5)] + "D" + pageLine[(pageLine.find('<sub>') + 6):]
                    if pageLine[pageLine.find('<sub>') + 5] == '4':
                        pageLine = pageLine[:(pageLine.find('<sub>') + 5)] + "E" + pageLine[(pageLine.find('<sub>') + 6):]
                    if pageLine[pageLine.find('<sub>') + 5] == '5':
                        pageLine = pageLine[:(pageLine.find('<sub>') + 5)] + "F" + pageLine[(pageLine.find('<sub>') + 6):]
                    if pageLine[pageLine.find('<sub>') + 5] == '6':
                        pageLine = pageLine[:(pageLine.find('<sub>') + 5)] + "G" + pageLine[(pageLine.find('<sub>') + 6):]
                    if pageLine[pageLine.find('<sub>') + 5] == '7':
                        pageLine = pageLine[:(pageLine.find('<sub>') + 5)] + "H" + pageLine[(pageLine.find('<sub>') + 6):]
                    if pageLine[pageLine.find('<sub>') + 5] == '8':
                        pageLine = pageLine[:(pageLine.find('<sub>') + 5)] + "I" + pageLine[(pageLine.find('<sub>') + 6):]
                    if pageLine[pageLine.find('<sub>') + 5] == '9':
                        pageLine = pageLine[:(pageLine.find('<sub>') + 5)] + "J" + pageLine[(pageLine.find('<sub>') + 6):]

                pageLine = pageLine.replace("!", "")
                pageLine = pageLine.replace("?", "")
                pageLine = pageLine.replace('-', '')
                pageLine = pageLine.replace("x", "")
                pageLine = pageLine.replace("o", "")
                pageLine = pageLine.replace("+", "")
                pageLine = pageLine.replace("[", "")
                pageLine = pageLine.replace("]", "")
                pageLine = pageLine.replace("(", "")
                pageLine = pageLine.replace(")", "")
                pageLine = pageLine.replace("*", "")
                pageLine = pageLine.replace("}","")
                pageLine = pageLine.replace("{","")


                pageLine = pageLine.replace("&lt;", "")
                pageLine = pageLine.replace("&gt;", "")
                pageLine = pageLine.replace("&nbsp;", "")
                pageLine = pageLine.replace("nsbp;", "")

                pageLine = pageLine.replace("<i>", "")
                pageLine = pageLine.replace("</i>", "")
                pageLine = pageLine.replace("<sub>","SUB")
                pageLine = pageLine.replace("</sub>", "ESUB")
                pageLine = pageLine.replace("<sup></sup>", "")
                pageLine = pageLine.replace("</em>","")
                pageLine = pageLine.replace("<em>","")
                pageLine = pageLine.replace("<td>","")
                pageLine = pageLine.replace("</td>","")
                pageLine = pageLine.replace("</tr>","")
                pageLine = pageLine.replace("<tr>","")

                pageLine = pageLine.replace("&iacute;", "")
                pageLine = pageLine.replace("</div>","")
                pageLine = pageLine.replace("</table>","")
                pageLine = pageLine.replace("<div>", "")
                pageLine = pageLine.replace("<table>", "")
                pageLine = pageLine.replace("</table", "")


                pageLine = pageLine.translate(None, '…⌉⌈—�')



                pageLine = re.sub(r'(\.?\/?\d+)+', 'NUM', pageLine)

                pageLine = pageLine.replace('<td style="width:NUMpx">', "")
                pageLine = pageLine.replace('<td style="width:NUM">', "")
                pageLine = pageLine.replace('.', " ")


#               handle super scripts
                while (pageLine.find('<sup>') != -1):
                    start = pageLine.find('<sup>')
                    end = pageLine.find(' ', start)
                    a = pageLine.find('>', start + 1)
                    b = pageLine.find('<', start + 1)
                    pointer = start
                    while (pointer > 0 and pageLine[pointer] != ' '):
                        pointer = pointer - 1
                    if (pageLine[a + 1:b] == 'ki'):
                        pageLine = pageLine[:pointer] + " KI " + pageLine[end:]
                    else:
                        pageLine = pageLine[:start] + pageLine[a + 1:b] + pageLine[end:]

                pageLine = pageLine.replace("<", "")
                pageLine = pageLine.replace(">", "")
                pageLine = pageLine.replace("&lceil;", "")
                pageLine = pageLine.replace("&rceil;", "")

                #               handle dictionary
                help = pageLine.split()
                for el in help:
                    if not dict.has_key(el):
                        dict[el] = [counter,1]
                        counter = counter + 1
                    else:
                        dict[el] = [dict[el][0],dict[el][1] + 1]
                    dict_text_file.write(str(dict[el][0]) + " ")

                #print (z)
                #print (len(myPageUrl))
                helperPage = pageLine.replace(" ","");
                if helperPage != "" and helperPage != "\n":
                    text_file.write(pageLine + "\n")
                    if choose != 1:
                        print(pageLine)

        if choose != 1:
            print (dict)
            print (len(dict))
        else:
            prhelp = prhelp + 1
            c = str(round((prhelp / 1834) * 100,3))
            print('\r', end="")
            print(c + "%", end="")
            time.sleep(0.01)
    dict_text_file.close()
    text_file.close()
    print ("\nfinised download the texts")

    print(r"dictionary download: (to C:\WorkAlpha\babylonienTexts\texts.txt and C:\WorkAlpha\babylonienTexts\dictionary.txt)")

    text_file = open(r"C:\WorkAlpha\babylonienTexts\dictionary.txt", "w")
    for i in dict:
        text_file.write("[" + str(i) +" [")
        if choose != 1:
            print("[" + str(i) +" [")
        for e in dict[i]:
            text_file.write(str(e) + ", ")
            if choose != 1:
                print (str(e) + ", ")
        text_file.write("]]")
    text_file.write("\n\nDictionary length: " + str(len(dict)))
    text_file.close()
    print ("100.0%")
    print (r"finished download texts dictionary")
    print ("\ndownload finished")
