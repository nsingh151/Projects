from extract_connection import Sql_connection
from transform import data_cleaning, refine
from connect_string import DATABASE


''' Creating connection object and exceuting the script for fetching cm_id and short_biography'''

# Fetching short bio for cm created in 2018 who are not paid yet 

query1 = ''' 
select  cm.council_member_id as cm_id,short_bio --, cm.*
 from glglive..council_member cm

left join mvs..fact_projects fp
on fp.council_member_id= cm.council_member_id

where fp.council_member_id is null                   --- eliminating TPV done CMs
and cm.lead_ind=0                                    --- should not be a lead 
and cm.short_bio is not null and cm.short_bio <>''   --- should have a bio
 and year(cm.create_date)=2018                       --- 2018 created CMs
 and cm.dnc_ind=0                                    --- should not be DNCed
'''

test_run = Sql_connection(DATABASE)   # object initiation
frame=test_run.query(query1)         # returning dataframe cm_id & short_bio
print(frame.head(10))


''' Exceuting the script for fetching cm_id and Employmet details from vw_cm_job'''

# Fetching Comapny details for cm created in 2018 who are not paid yet 

query2 = ''' 
with cte_cm as
(
select  cm.council_member_id
 from glglive..council_member cm

left join mvs..fact_projects fp
on fp.council_member_id= cm.council_member_id

where fp.council_member_id is null   -- eliminating TPV done CMs
and cm.lead_ind=0                --- should not be a lead 
and cm.short_bio is not null and cm.short_bio <>''  -- should have a bio
 and year(cm.create_date)=2018                      --- 2018 created CMs
 and cm.dnc_ind=0                                ----- Should not be DNCed
)

select cte.Council_member_id as cm_id,
isnull(cm.company+' '+ cm.title,'Unknown') as employment
 from cte_cm cte
 
 left join mvs..vw_dim_cm_job cm
 on cm.council_member_id=cte.council_member_id
 '''

# test_run = Sql_connection(DATABASE)   # object initiation
frame_job_history=test_run.query(query2)         # returning dataframe  cm_id and Emp_details
print(frame_job_history.head(10))


### for biography clean_up

clean= data_cleaning(frame)
cm_bio=clean.create_dict()
print("Length of Bio CM dictionary :",len(cm_bio))   


### for employment details combine records and removing stopwords

combine=refine(frame_job_history)
cm_work_details=combine.combine_emp_history()
print("Length of Work details dictionary before combining :",len(cm_work_details))


clean_emp= data_cleaning(frame_dict=cm_work_details)
cm_work_details=clean_emp.clean_up()
print("Length of Work details dictionary after combining :",len(cm_work_details))  

 

## Fuzzy logic comparison
from fuzzywuzzy import fuzz
fuzzy_dict={}
cntt=0

for key in cm_bio:
    print("key :", key)
    print("cnt :",cntt)
    cntt+=1
#     val=process.extractOne(cm_work_details[key],cm_bio[key])[1]
    bio=cm_bio[key].split()
#     print(bio)

    work=cm_work_details[key].split()
#     print("wor",work)
    work_len=len(work)+1
#     print(bio_len)
    cnt=0
    for word in work:
        if word in bio:
            cnt+=1  
        else:
            continue 
    val=(cnt*100)/work_len
    print("val :", val)
#     fuzzy_dict[key]=val
    if val<50:
        print("=====")
        print("Biography :\n ", cm_bio[key])
        print("=================================================")
        print("Employment details :\n ", cm_work_details[key])
        print("=================================================")
        fuzzy_dict[key]=val
print("Number of Poor Bios :",len(fuzzy_dict))







