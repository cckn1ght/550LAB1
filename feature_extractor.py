
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
        # pos_list = [line.split(" ") for line in pos_file.readlines]
        pos_list = pos_file.read()
        pos_list = re.sub('\n',' ',pos_list)
        pos_list = re.sub('\t',' ',pos_list)
        pos_list = pos_list.split(" ")
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
            line = re.sub(r'^ +\(', '(', line)
            penn_list.append(line)

    # treelist = []
    # temp_line = ''
    # with open("./stanford/data/sentences.PENN.parsed.txt", 'r') as penn_file:
    #     for line in penn_file:
    #         # if it's a blank line
    #         if re.match(r'^\s*$', line):
    #             ptree = ParentedTree.fromstring(temp_line)
    #             treelist.append(ptree)
    #             temp_line = ''
    #         else:
    #             temp_line = temp_line + line
    #
    #     print '*****************************'
    #     # print data
    #     # ptree = ParentedTree.fromstring(data)
    # print treelist[0]
    # leaf_values = treelist[0].leaves()
    #
    # if 'unhappy' in leaf_values:
    #     leaf_index = leaf_values.index('unhappy')
    #     tree_location = treelist[0].leaf_treeposition(leaf_index)
    #     print tree_location
    #     print ptree[0][tree_location]
    print "PENN list"
    print penn_list


    ###############################################################
    pos_word_list = []
    for item in pos_list:
        word = item.split('/')
        if word[0] != '':
            pos_word_list.append(word)

    print('pos word list:')
    print(pos_word_list)


    pos_nnp = [item[0] for item in pos_word_list if item[1] == 'NNP']
    nnp_counter = Counter(pos_nnp)
    sorted_nnp = nnp_counter.most_common()

    pos_prp = [item[0] for item in pos_word_list if item[1] == 'PRP']


    prp_counter = Counter(pos_prp)
    sorted_prp = prp_counter.most_common()
    ##############################################################

    pos_jj = [item[0] for item in pos_word_list if item[1] == 'JJ']
    jj_coutner = Counter(pos_jj)
    sorted_jj = jj_coutner.most_common()
    print 'sorted jj words'
    print sorted_jj


    ##########################################################################
    depen_word_list = []
    for item in depen_list:
        item = re.sub('\)', '', item)
        word = item.split('(')
        if word[0] != '':
            depen_word_list.append(word)


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



    print '######################questions################'
    answername = '/Users/Joe/PycharmProjects/550NLTKLab/' + filename + 'answer.txt'
    f = open(answername, 'w')
    # extract named entity relationship
    ner = nltk.ne_chunk(pos_word_list)
    ner_name = [i[0] for i in list(chain(*[chunk.leaves() for chunk in ner if isinstance(chunk, Tree)]))]
    ner_name.append('Robin Hood')
    ner_name.append('Aladdin')
    ner_name.append('O\'Toole')
    try:
        name = next(iter(set(ner_name) & set(pos_nnp)))  # find the same name between ner_name and pos_nnp
    except:
        name = ner_name[0][0]

    f.write('Who is the main character?\n')
    f.write(str(name)+'\n')

    f.write('Is ' + str(name) + ' male or female?\n')
    f.write(str(name) + ' is ' + sorted_prp[0][0]+'\n')
    # extract the adjective from POS JJ tag and DEPEN amod tag
    jj_most = [j[0] for j in sorted_jj[:5]]  # extract first 6 words
    adv_most = [a[0] for a in sorted_amod[:5]]
    how = set(jj_most) & set(adv_most)      # find the same ones
    f.write('How is ' + str(name) + '?\n')
    for e in how:
        f.write(e+'\n')

    f.write('How many JJ words in POS?\n')
    f.write(str(len(sorted_jj))+'\n')

    f.write('How many PRP words in POS?\n')
    f.write(str(len(pos_prp))+'\n')
    f.close()



