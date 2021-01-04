# %%
import os
from email.parser import Parser
import pickle
import jieba
import re
import nltk
import pandas as pd

stemmer = nltk.stem.SnowballStemmer('english')

index_path = "../output/file_map.txt" # 映射文件到整型，方便存储
base_path = "../dataset/enron_mail_20150507/maildir/"
path = base_path
queries_semantic_file_path = '../query_semantic.txt'

pattern_subject = r'Subject: (.+?)Mime'  # 用于提取邮件标题
pattern_obj_subject = re.compile(pattern_subject, re.DOTALL)  # 有换行符，需要re.DOTALL来保证可以匹配
pattern_content = r'X-FileName: (.+?)$'  # 用于提取邮件内容
pattern_obj_cotent = re.compile(pattern_content, re.DOTALL)
stop = open('./stopword.txt', 'r+', encoding='utf-8')
stopword = stop.read().split("\n")  # 停用词表 <class 'list'>
fileIndex = 0  # 之前代码为0
indexList = []
# %%

def file_process(path, all_files, level):
    """
    递归处理文件，实现由原邮件到预处理后邮件到映射
    针对每一个文件进行编号，建立文件的索引
    :param
        path:
        all_files:
        level:
    :return:
    """
    global invertedIndex
    global fileIndex
    global afterPreProcessPath
    file_list = os.listdir(path)
    #print(file_list)
    if level == 1:
        print(path)
    for file in file_list:  # 按深度递归遍历所有文件夹下的邮件
        cur_path = os.path.join(path, file)
        if os.path.isdir(cur_path):
            file_process(cur_path, all_files, level+1)
        else:
            try:
                fileIndex = save_results(cur_path,fileIndex,'../output/pre_process/')
                if(fileIndex % 5000 == 0):
                    print(fileIndex)
            except UnicodeError:
                continue

    #save_results(queries_semantic_file_path,-1,'../output/query_semantic_list.txt')
    indexFile = open(index_path,"w+")
    indexFile.write(str(indexList))
    indexFile.close()

def save_results(cur_path,fileIndex,save_path):
    data_subject = extract_info(cur_path)
    data_subject = jieba.cut(data_subject, cut_all=False)
    line = "/".join(data_subject).lower()  # 转成字符串 + 小写
    wordlist = stopwords(line)  # 对从一篇文档中提取出的词去停用词
    pathlist = cur_path.replace(base_path, '')
    indexList.append(pathlist)
    # wordlist.append(pathlist)
    # dir_name = pathlist[-2]
    # print(fileIndex, wordlist)
    if fileIndex != -1:
        save_path = save_path + str(fileIndex)  # 把处理好的数据按原邮件名保存在新文件中
    fileIndex += 1
    file = open(save_path, 'w+')
    file.write(str(wordlist))
    file.close()
    return fileIndex

def remove_digits(input_str):
    """
    去除字符串中的数字
    :param input_str: 输入的字符串
    :return:
    """
    punc = u'0123456789.'
    output_str = re.sub(r'[{}]+'.format(punc), '', input_str)
    return output_str


def stopwords(line):
    """
    去停用词,词根化
    :return: 去停用词后的列表
    """
    wordlist = []
    for key in line.split('/'):
        if not (key.strip() in stopword) and (len(key.strip()) > 1) and not (key.strip() in wordlist):
            if not remove_digits(key):
                continue
            else:
                key = stemmer.stem(key)  # 词根化
                wordlist.append(key)
                # print(key)
    return wordlist


def extract_info(path):
    """
    从邮件中提取有用信息，使用os 模块 + 正则表达式
    :param path: 邮件路径
    :return:
    """
    Rawdata = open(path, 'r+', encoding='utf-8')
    text = Rawdata.read()  # <class 'str'>

    email_subject = pattern_obj_subject.findall(text)  # 利用正则表达式，将所需内容提取到data_list中
    data_subject = "".join(email_subject)  # 列表转字符串并换行显示
    email_content = pattern_obj_cotent.findall(text)
    email_content = email_content[0][email_content[0].find('\n'):]  # 去掉X-FileName:前的信息，保留邮件内容
    data_subject = data_subject + email_content  # 把标题内容 + 邮件内容组合起来
    return data_subject

# %%
file_process(path, [], 0)

