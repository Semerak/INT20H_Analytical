import pandas
import datetime as dt
import numpy as np
import sys

DaysTrial=7
DevProceeds=9.99
MaxPurches=6
AppleTax=0.3

def subscriber_actions(df,subscriber_id):
    return df[df['Subscriber ID']==subscriber_id]

def to_datetime(line):
    date_split=line.split('-')
    return dt.date(int(date_split[0]),int(date_split[1]),int(date_split[2]))


def cur_day(df):
    return to_datetime( df['Event Date'].max())


def add_vectors(a,b):
    a_size=a.size
    b_size=b.size
    if a_size == b_size:
        return a+b
    if a_size > b_size:
        return a+ np.pad(b,(0,a_size-b_size),'constant')
    return b+ np.pad(a,(0,b_size-a_size),'constant')

def count_purch_ends(df,sub_id):
    df_=subscriber_actions(df,sub_id)
    numb_of_purch=len(df_)
    numb_of_ends=numb_of_purch
    if cur_day(df) - to_datetime(df_['Event Date'].max()) < dt.timedelta(DaysTrial):  
        numb_of_ends-=1
    return numb_of_purch, numb_of_ends
        

def count_all_purch_ends(df):
    all_purch=np.zeros(MaxPurches)
    all_ends=np.zeros(MaxPurches)
    for sub_id in df['Subscriber ID'].unique():
        p,e=count_purch_ends(df,sub_id)
        all_purch=add_vectors(all_purch,np.ones(p))
        all_ends=add_vectors(all_ends,np.ones(e))
    return all_purch, all_ends

def LTV(df):
    all_purch,all_ends=count_all_purch_ends(df)
    ltv_=0
    x=DevProceeds*(1-AppleTax)
    for i in range(all_purch.size-1):
        x=x*(all_purch[i+1]/all_ends[i])
        ltv_+=x
    return ltv_

if __name__ == "__main__":
    file_name=sys.argv[1]
    df = pandas.read_csv(file_name)
    
    ltv=LTV(df)
    print(ltv)

