### Import library

import  pandas as pd
from nltk import word_tokenize
from nltk.corpus import stopwords
import string
import nltk
from fuzzywuzzy import process
import termcolor

'''

Class is used to create dictionary for further analysis and clean biography for further analysis


'''

class data_cleaning():
    
    def __init__(self,df=pd.DataFrame(), frame_dict={}):
        self.df=df
        self.cm_dict = frame_dict
        
        
    def create_dict(self):
        ''' create dictionary form dataframe '''
        for i in range(0,len(self.df)):
            self.cm_dict[self.df['cm_id'][i]]=self.df['short_bio'][i]
        return self.clean_up()
    
    def clean_up(self):
        '''
        Clean dictionary for the stop words and puntuation for further analysis
        
        '''
        stop = stopwords.words('english') + list(string.punctuation)
        for key, value in self.cm_dict.items():
#             print("initial value\n ", self.cm_dict[key])
            if value =='' or value is None:
                value='Unknown'
#             print("count :", cnt)
#             print("key :" , key)
            word_list= [i for i in word_tokenize(value.lower()) if i not in stop]
#             print(c)
            sentence=""
            for word in word_list:
                sentence=sentence+" "+word
            self.cm_dict[key]=sentence
#             print ("final value \n ",self.cm_dict[key])
        return self.cm_dict

'''  
This class combine multiple records of cm_id with employement details into 1 single dictionary item


'''

class refine():
    
    def __init__(self,frame):
        self.frame=frame
        self.cm_id=[]
        self.emp_dict={}
        
    def combine_emp_history(self):
        
        for i in range(0, len(self.frame)):
            self.cm_id.append(self.frame['cm_id'][i])
        self.cm_id=set(self.cm_id)
#         print(self.cm_id)

        for key in self.cm_id:
            value_df = self.frame.loc[self.frame['cm_id']==key]
            str_a=''        
            for j in value_df['employment']:
                if j is None:
                    j = 'Unknown'
                str_a=str_a+" "+j
            self.emp_dict[key]=str_a
        
        return self.emp_dict
   
