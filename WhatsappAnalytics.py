import collections
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import subplot, figure, subplots
#%matplotlib inline
fname = input('Enter the file name: ')
if fname == '':
    fname='Asses_Whatsapp.txt'
try:
    fhand = open(fname,encoding="utf8")
    fhand1 = open(fname,encoding="utf8")
    fhand2 = open(fname,encoding="utf8")
except:
    print('File cannot be opened:', fname)
    exit()

common_Word_list=['<Media','omitted>','this','that','there','Where']

print('1. How many times did this word occur?')
print('2. What was the most common word used in the group?')
print('3. Who sent the most number of messages?')
print('4. What is the most often used words by a person the most?')
print('5. Who spoke more about the word?')
choice=int(input('enter your choice of action:'))

counts = dict()
for line in fhand:
    #print(line)
    ind=line.find('-')
    line=line[ind+1:]
    ind=line.find(':')
    line=line[ind+1:]
    line = line.replace(".","")
    line = line.replace("?","")
    line = line.replace("Media","")
    line = line.replace("omitted","")
    words = line.split()

    for word in words:
        if len(word)<=4 or word in common_Word_list:
            continue
        if word not in counts:
            counts[word] = 1
        else:
            counts[word] += 1
#print(counts)
#print(word_counter)
most_msgs = dict()
x=1
for lin in fhand1:
    if len(lin) is None :
        continue
    ind=lin.find('-')
    lin=lin[ind+1:]
    if len(lin) is None :
        continue
    if ':' not in lin :continue
        #print(': is not there~ line number~~',x,'~~', lin)
        #x=x+1

        #print(lin)
    ind=lin.find(':')
    person=lin[:ind]
    #print(person)
    person_lst=person.split()
    person = person_lst[0]
    msg=lin[ind+1:]
    most_msgs[person]=most_msgs.get(person,0)+1
    #x=x+1
#print(most_msgs)

#print(most_msgs.get('Join Zoom Meeting',0))

#Code to get "How many times did this word occur"
if choice==1:
    search_Word=input('enter the word you want to search for: ')
    search_Word_upr=search_Word.upper()
    #occuring=counts.get(search_Word,0)
    #print(occuring)
    occuring=0
    for lin in fhand2:
        if len(lin) is None :
            continue
        ind=lin.find('-')
        lin=lin[ind+1:]
        if len(lin) is None :
            continue
        #if ':' not in lin :continue
        ind=lin.find(':')
        #person=lin[:ind]
        #print(person)
        #person_lst=person.split()
        #person = person_lst[0]
        msg=lin[ind+1:]
        msg=msg.upper()
        if search_Word_upr in msg:
            occuring=occuring+len(msg.split(search_Word_upr))-1
    print('{} word has occurred {} times in the group'.format(search_Word,occuring))

#Code to get the most used word in the group
if choice==2:
    word_counter = collections.Counter(counts)
    n_times=int(input('how many most common words:'))
    #most_used_word=''
    #most_used_times=0
    for wor,count in word_counter.most_common(n_times):
        #if count>most_used_times:
        #    most_used_times=count
        #    most_used_word=wor
        print('{} is used : {}'.format(wor,count))
    #print('the most used word is:', most_used_word, 'used ',most_used_times,' times')
    # Create a data frame of the most common words
    # Draw a bar chart
    lst = word_counter.most_common(n_times)
    print(lst)
    df = pd.DataFrame(lst, columns = ['Word', 'Count'])
    df.plot.bar(x='Word',y='Count')
    plt.show()

if choice==3:
    group_members=int(input('enter the number of members in group:'))
    msg_counter = collections.Counter(most_msgs)
    for per,count in msg_counter.most_common(group_members):
        print('{} messaged {} times'.format(per,count))

    most_msgs_lst=msg_counter.most_common(group_members)
    df = pd.DataFrame(most_msgs_lst, columns = ['person', 'Number of messages'])
    df.plot.bar(x='person',y='Number of messages')
    plt.show()

#4. What is the most often used words by a person?
if choice==4:
    most_msgs_per = dict()
    most_msgs_per_word_count=dict()
    person_list=list()
    fhand3=open(fname,encoding='utf8')
    x=1
    for lin in fhand3:
        if len(lin) is None:
            continue
        ind=lin.find('-')
        name_msg=lin[ind+1:]
        if ':' not in name_msg or ('AM -' not in lin and 'PM -' not in lin)  :continue
        ind=name_msg.find(':')
        person=name_msg[1:ind]
        msg=name_msg[ind+1:]
        person_lst=person.split()
        person = person_lst[0]
        if person_list.count(person)==0:
            person_list.append(person)

        if person not in most_msgs_per.keys():
            most_msgs_per[person]=list()
            msg_list=msg.split()
            for wor in msg_list:
                if len(wor)<=4 or wor in common_Word_list : continue
                most_msgs_per[person].append(wor)
        msg_list=msg.split()
        for wor in msg_list:
            if len(wor)<=4 or wor in common_Word_list : continue
            most_msgs_per[person].append(wor)

    for per in most_msgs_per.keys():
        most_msgs_per_word_count[per]=dict()
        for wor in most_msgs_per[per]:
            most_msgs_per_word_count[per][wor]=most_msgs_per_word_count.get(per).get(wor,0)+1
            #print(per,' ',wor)
    n_per_times=int(input('how many most common words:'))
    no_pers=len(most_msgs_per)
    x=0
    y=0
    nrow=int(no_pers/2)
    ncol=3
    fig,axes=plt.subplots(nrows=nrow, ncols=ncol)
    for per in most_msgs_per_word_count.keys():
        per_word_counter = collections.Counter(most_msgs_per_word_count[per])
        #print('below are the most common words for {}'.format(per),':')
        #for wor,count in per_word_counter.most_common(n_per_times):
        #    print('{} was used {} times'.format(wor,count))
        #plt.figure(1)

        #plt.title(per)
        per_word_counter_list=per_word_counter.most_common(n_per_times)
        #print(per_word_counter_list)
        #plt.bar()
        df = pd.DataFrame(per_word_counter_list, columns = ['Word', 'number of times used'])
        df = df.set_index('Word')
        myplot=df.plot(ax=axes[x],kind='bar')
        myplot.set_title(per)
        myplot.set_xlabel('')
        x=x+1
        #if y==nrow-1:
        #    x=x+1
        #y=y+1
    plt.show()
