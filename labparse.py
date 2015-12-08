import re
import os
import shutil
import commands
import random
import time
import sys
import copy
import datetime
import glob
import math
import subprocess
import sets
from feature_extractor import extrator
from subprocess import call, Popen, PIPE, STDOUT
import nltk

def run_cmd(cmd):
    arglist = cmd.split()
    p = Popen(arglist, stdout=PIPE, stderr=STDOUT)
    output = p.communicate()[0]
    return (p.returncode, output)


############################################################################################################

def mycommandsfunction(sentence):

    path = "/Users/Joe/PycharmProjects/550NLTKLab/stanford/parser/"
    os.chdir(path)

    g_add_sentence = "/Users/Joe/PycharmProjects/550NLTKLab/stanford/data/sentences.txt"
    f_add_sentence = open(g_add_sentence,'w')
    # go to the start of this file
    f_add_sentence.seek(0)
    f_add_sentence.write(sentence)
    f_add_sentence.write('\n')
    f_add_sentence.close()

    stanfordcommandPOS = 'java -cp stanford-parser.jar -mx1024m edu.stanford.nlp.parser.lexparser.LexicalizedParser -outputFormat "wordsAndTags" englishPCFG.ser.gz "/Users/Joe/PycharmProjects/550NLTKLab/stanford/data/sentences.txt" > "/Users/Joe/PycharmProjects/550NLTKLab/stanford/data/sentences.POS.parsed.txt"'
    stanfordcommandPENN = 'java -cp stanford-parser.jar -mx1024m edu.stanford.nlp.parser.lexparser.LexicalizedParser -outputFormat "penn" englishPCFG.ser.gz "/Users/Joe/PycharmProjects/550NLTKLab/stanford/data/sentences.txt" > "/Users/Joe/PycharmProjects/550NLTKLab/stanford/data/sentences.PENN.parsed.txt"'
    stanfordcommandDEPEN = 'java -cp stanford-parser.jar -mx1024m edu.stanford.nlp.parser.lexparser.LexicalizedParser -outputFormat "typedDependencies" englishPCFG.ser.gz "/Users/Joe/PycharmProjects/550NLTKLab/stanford/data/sentences.txt" > "/Users/Joe/PycharmProjects/550NLTKLab/stanford/data/sentences.DEPEN.parsed.txt"'
    os.system(stanfordcommandPOS)
    os.system(stanfordcommandPENN)
    os.system(stanfordcommandDEPEN)


##########################################################################################################

def GetSyntacticParseStanfordParser(sentence):
    g_add_sentence = "/Users/Joe/PycharmProjects/550NLTKLab/stanford/data/sentences.txt"
    f_add_sentence = open(g_add_sentence,'w')
    # go to the start of this file
    f_add_sentence.seek(0)
    f_add_sentence.write(sentence)
    f_add_sentence.write('\n')
    f_add_sentence.close()

    path = '/Users/Joe/PycharmProjects/550NLTKLab/stanford/parser/'
    os.chdir(path)

    stanfordcommandPENN = 'java -cp stanford-parser.jar -mx1024m edu.stanford.nlp.parser.lexparser.LexicalizedParser -outputFormat "penn" englishPCFG.ser.gz "/Users/Joe/PycharmProjects/550NLTKLab/stanford/data/sentences.txt" > "/Users/Joe/PycharmProjects/550NLTKLab/stanford/data/sentences.PENN.parsed.txt"'
    os.system(stanfordcommandPENN)

    g_stanford_parse_PENN = '/Users/Joe/PycharmProjects/550NLTKLab/stanford/data/sentences.PENN.parsed.txt'
    f_stanford_parse_PENN = open(g_stanford_parse_PENN,'r')

    s_penn = ''
    for line in f_stanford_parse_PENN.readlines():
        s_penn = s_penn + line

    f_stanford_parse_PENN.close()

    temp = re.sub('\n','',s_penn)
    temp = re.sub('\t','',temp)

    return temp

##########################################################################################################

def GetDependencyParseStanfordParser(sentence):
    g_add_sentence = '/Users/Joe/PycharmProjects/550NLTKLab/stanford/data/sentences.txt'
    f_add_sentence = open(g_add_sentence,'w')
    f_add_sentence.seek(0)
    f_add_sentence.write(sentence)
    f_add_sentence.write('\n')
    f_add_sentence.close()

    path = '/Users/Joe/PycharmProjects/550NLTKLab/stanford/parser/'
    os.chdir(path)

    stanfordcommandDEPEN = 'java -cp stanford-parser.jar -mx1024m edu.stanford.nlp.parser.lexparser.LexicalizedParser -outputFormat "typedDependencies" englishPCFG.ser.gz "/Users/Joe/PycharmProjects/550NLTKLab/stanford/data/sentences.txt" > "/Users/Joe/PycharmProjects/550NLTKLab/stanford/data/sentences.DEPEN.parsed.txt"'
    os.system(stanfordcommandDEPEN)

    g_stanford_parse_DEPEN = '/Users/Joe/PycharmProjects/550NLTKLab/stanford/data/sentences.DEPEN.parsed.txt'
    f_stanford_parse_DEPEN = open(g_stanford_parse_DEPEN,'r')

    s_penn_DEPEN = []
    for line in f_stanford_parse_DEPEN.readlines():
        temp3 = re.sub('\n','',line)
        s_penn_DEPEN.append(temp3)

    f_stanford_parse_DEPEN.close()

    #temp = re.sub('\n','',s_penn)
    #temp = re.sub('\t','',temp)

    return s_penn_DEPEN

###########################################################################################################

## Main()

#sent = 'Yesterday Joe went to visit Dr. Gerald M. Knapp at the hospital, where his sister, was very sick not two months ago.'
# the_parse = GetSyntacticParseStanfordParser(sent)
# my_dependencies_list = GetDependencyParseStanfordParser(sent)
for i in range(1, 6):
    filename = 'story' + str(i)
    with open('/Users/Joe/PycharmProjects/550NLTKLab/' + filename+'.txt', 'r') as news:
        sent = news.read()
# sent = "".join(c for c in sent if c not in ('!', '.', ',', ':', ';'))
    mycommandsfunction(sent)

    extrator(filename)
# GetSyntacticParseStanfordParser(str(sent))
# GetDependencyParseStanfordParser(str(sent))


# print the_parse
#treeRC = nltk.Tree(the_parse)
#myleaves = treeRC.leaves()
#print myleaves
#treeRC.draw()

print ''
# print my_dependencies_list

print '<<<<<<<<<<<<DONE>>>>>>>>>>>>'


####END
############################################################################################################

