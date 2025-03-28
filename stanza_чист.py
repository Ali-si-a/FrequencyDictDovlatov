# -*- coding: utf-8 -*-
"""Stanza чист

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1QAJAlyvDZGYo8tMiYq-EolFAyhqpXFii
"""

with open("/content/drive/MyDrive/Курсовая/Все тексты.txt") as f:
  text = f.read ()

!pip install stanza
import stanza
stanza.download('ru')
ppln = stanza.Pipeline('ru', processors='tokenize,pos,lemma')

doc=ppln(text)

with open("/content/drive/MyDrive/Курсовая/swl_optimum.txt") as f:
  swl = f.read ()

word_list=[]
pos_list=[]
for sent in doc.sentences:
  for word in sent.words:
    if word.lemma not in swl:
      word_list.append(str(word.lemma))
      pos_list.append(str(word.upos))

import pandas as pd

df = pd.DataFrame(word_list, pos_list)

df['кол-во']=1

df1=df.reset_index()

df1.columns=['Часть речи', 'Лемма', 'Количество словоупотреблений']

df2=pd.pivot_table(df1, index=['Лемма', 'Часть речи'], values='Количество словоупотреблений', aggfunc='sum')

df3=df2.reset_index()

with open("/content/drive/MyDrive/Курсовая/Тексты Довлатов.txt") as f:
  text2 = f.read ()

import re
text2=text2.replace('\n',' ')
text2=text2.replace(' -',' ').replace('- ',' ').replace('—',' ')
text2= re.sub(r'[^\w\s\-]','',text2)
text2=text2.split(' ')

word_list1=[]
for token in text2:
  if token !='':
    word_list1.append(token)

num=len(word_list1)

df3.insert(1, 'Доля (%)', df3['Количество словоупотреблений'].apply(lambda z: z/num*100))
df3

df3.insert(2, 'Частота (ipm)', df3['Количество словоупотреблений'].apply(lambda t: t*1000000/num))
df3

df4 = df3.sort_values(by='Количество словоупотреблений', ascending = False)
df4

df5=df4.reindex(columns=['Лемма', 'Количество словоупотреблений',  'Доля(%)', 'Частота (ipm)', 'Часть речи'])
df5

rslt_df = df4.sort_values(by='Количество словоупотреблений', ascending = False)
rslt_df

rslt_df.to_excel('FREQ.xlsx', index=False)

del rslt_df['Лемма']
del rslt_df['Доля (%)']
del rslt_df['Частота (ipm)']

rslt_df

df_pos_f=pd.pivot_table(rslt_df, index=['Часть речи'], values=['Количество словоупотреблений'], aggfunc='sum')
df_pos_f

df_pos_f.insert(1, 'Доля', df_pos_f['Количество словоупотреблений'].apply(lambda r: r/num*100))
df_pos_f

res1 = df_pos_f.T

res1['VERB'] = res1['VERB']+res1['AUX']+res1['PART']
res1['REST'] = res1['ADV'] +res1['NUM']+res1['INTJ']+res1['ADP']+res1['CCONJ']+res1['DET']+res1['PRON']+res1['PUNCT']+res1['SCONJ']+res1['SYM']+res1['X']

res2=res1.drop(['ADV', 'NUM', 'INTJ', 'AUX', 'PART', 'ADP', 'CCONJ', 'DET', 'PRON', 'PUNCT', 'SCONJ', 'SYM', 'X'], axis=1)

res3 = res2.T

rslt_df2 = res3.sort_values(by='Доля', ascending = False)

res3_new = rslt_df2.reset_index()
res3_new

num=len(word_list1)
num

df_pos = pd.DataFrame({
    'Количество': rslt_df['Часть речи'].value_counts (),
}).fillna(0) #Что это fillna? (импутировать нулевые значения в столбце с помощью функции)

print(df_pos[["Количество"]].sort_values(["Количество"], ascending=False))

df_pos.insert(1, 'Доля', df_pos['Количество'].apply(lambda r: r/df_pos['Количество'].sum()*100))
df_pos

res1 = df_pos.T

res1['VERB'] = res1['PART'] +res1['VERB']+res1['AUX']
res1['REST'] = res1['ADV'] +res1['NUM']+res1['ADP']+res1['PRON']+res1['X']+res1['PUNCT']+res1['SCONJ']+res1['INTJ']

res2=res1.drop(['ADV', 'NUM', 'ADP', 'PRON', 'X', 'PUNCT', 'SCONJ', 'INTJ', 'PART', 'AUX'], axis=1)

res3 = res2.T

rslt_df2 = res3.sort_values(by='Доля', ascending = False)

res3_new = rslt_df2.reset_index()

res3_new.columns=['Часть речи', 'Количество', 'Доля']
res3_new

dataframe = pd.DataFrame({'Часть речи': res3_new['Часть речи'],
                          'Доля': res3_new['Доля']})

dataframe.groupby(['Часть речи']).sum().plot(kind='pie', autopct='%1.0f%%', y='Доля')