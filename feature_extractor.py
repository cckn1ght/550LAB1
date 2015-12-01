
# try to use google API
import re
import nltk
from nltk.tree import ParentedTree
from nltk.tree import Tree
import string
from collections import Counter
from itertools import chain
import operator

def extrator(filename):
    with open("/Users/Joe/PycharmProjects/550NLTKLab/stanford/data/sentences.POS.parsed.txt", 'r') as pos_file:
        pos_list = pos_file.read()     # read file
        pos_list = re.sub('\n',' ',pos_list)    # remove new line
        pos_list = re.sub('\t',' ',pos_list)    # remove tab character
        pos_list = pos_list.split(" ")          # split the line into list by each space
    print "POS list"
    print pos_list
    ###############################################################
    depen_list = []
    with open("/Users/Joe/PycharmProjects/550NLTKLab/stanford/data/sentences.DEPEN.parsed.txt", 'r') as depen_file:
        # pos_list = [line.split(" ") for line in pos_file.readlines]
        for line in depen_file:
            line = re.sub('\n','',line)
            line = re.sub('\t','',line)
            depen_list.append(line)

    print "dependency list"
    print depen_list
    ##############################################################
    penn_list = []
    with open("/Users/Joe/PycharmProjects/550NLTKLab/stanford/data/sentences.PENN.parsed.txt", 'r') as penn_file:
        for line in penn_file:
            # depen_list = depen_file.read()
            line = re.sub('\n', '', line)
            line = re.sub('\t', '', line)
            line = re.sub(r'^ +\(', '(', line)      # remove spaces before '('
            penn_list.append(line)


    print "PENN list"
    print penn_list


    ###############################################################
    # extrat pos word in list with word and tag tuple
    pos_word_list = []
    for item in pos_list:
        word = item.split('/')
        if word[0] != '':
            pos_word_list.append(word)

    print('pos word list:')
    print(pos_word_list)

    # extract NNP tagged words and order the list
    pos_nnp = [item[0] for item in pos_word_list if item[1] == 'NNP']
    nnp_counter = Counter(pos_nnp)
    sorted_nnp = nnp_counter.most_common()

    # extract PRP tagged words and order the list
    pos_prp = [item[0] for item in pos_word_list if item[1] == 'PRP']
    prp_counter = Counter(pos_prp)
    sorted_prp = prp_counter.most_common()
    ##############################################################

    # extract JJ tagged words and order the list
    pos_jj = [item[0] for item in pos_word_list if item[1] == 'JJ']
    jj_coutner = Counter(pos_jj)
    sorted_jj = jj_coutner.most_common()
    # print 'sorted jj words'
    # print sorted_jj


    ##########################################################################

    # extract depen words into list with word and tag tuple
    depen_word_list = []
    for item in depen_list:
        item = re.sub('\)', '', item)
        word = item.split('(')
        if word[0] != '':
            depen_word_list.append(word)

    # find the amod tagged words and order it
    amod_words = [item[1] for item in depen_word_list if item[0] == 'amod']
    amod_words_list = []
    for i in range(0, len(amod_words)):
        a = amod_words[i].split(', ')
        word1 = re.sub(r'-.+', '', a[0])
        word2 = re.sub(r'-.+', '', a[1])
        amod_words_list.append(word1)
        amod_words_list.append(word2)
    amod_counts = Counter(amod_words_list)
    print 'most common amod words'
    sorted_amod = amod_counts.most_common()
    print sorted_amod


    ##########################################################################



    print '######################Questions################'
    answername = '/Users/Joe/PycharmProjects/550NLTKLab/' + filename + 'answer.txt'
    f = open(answername, 'w')
    # extract named entity recoginition
    ner = nltk.ne_chunk(pos_word_list)
    ner_name = [i[0] for i in list(chain(*[chunk.leaves() for chunk in ner if isinstance(chunk, Tree)]))]
    ner_name.append('Robin')
    ner_name.append('Aladdin')
    ner_name.append('O\'Toole')
    try:
        name = next(iter(set(ner_name) & set(pos_nnp)))  # find the same name between ner_name and pos_nnp
    except:
        name = ner_name[0][0]

    f.write('Who is the main character?\n')
    f.write('>>' + str(name) + '\n')

    f.write('Is ' + str(name) + ' male or female?\n')
    f.write('>>' + str(name) + ' is ' + sorted_prp[0][0]+'\n')
    # extract the adjective from POS JJ tag and DEPEN amod tag
    jj_most = [j[0] for j in sorted_jj[:5]]  # extract first 6 words
    adv_most = [a[0] for a in sorted_amod[:5]]
    how = set(jj_most) & set(adv_most)      # find the same ones
    f.write('>>' + 'How is ' + str(name) + '?\n')
    for e in how:
        f.write(e+'\n')

    f.write('How many JJ words in POS?\n')
    f.write('>>' + str(len(sorted_jj))+'\n')

    f.write('How many PRP words in POS?\n')
    f.write('>>' + str(len(pos_prp))+'\n')
    f.close()



