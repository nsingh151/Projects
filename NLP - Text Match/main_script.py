''' Creating connection object and exceuting the script for fetching cm_id and short_biography'''

# Fetching short bio for cm paid in 2015 and above 

query1 = ''' 
with cte_cm as
(
select distinct council_member_id 
from mvs..fact_projects
where year(paid_date)=2018
and tpv_nm_ind = 1
)
Select cm.council_member_id as cm_id, cm.short_bio as short_bio
from  cte_cm cte

join glglive..council_member cm
on cte.council_member_id=cm.council_member_id
'''

test_run = Sql_connection(DATABASE)   # object initiation
frame=test_run.query(query1)         # returning dataframe cm_id & short_bio
print(frame.head(10))


''' Exceuting the script for fetching cm_id and Employmet details from vw_cm_job'''

# Fetching short bio for cm paid in 2015 and above 

query2 = ''' 
with cte_cm as
(
select distinct council_member_id 
from mvs..fact_projects
where year(paid_date)=2018
and tpv_nm_ind = 1
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
print(len(cm_bio))   


### for employment details combine records and removing stopwords

combine=refine(frame_job_history)
cm_work_details=combine.combine_emp_history()
print(len(cm_work_details))


clean_emp= data_cleaning(frame_dict=cm_work_details)
cm_work_details=clean_emp.clean_up()
print(len(cm_work_details))  

## Fuzzy logic comparison

f## Fuzzy logic comparison
from fuzzywuzzy import fuzz
fuzzy_dict={}
cntt=0

for key in cm_bio:
    print("key :", key)
    print("cnt :",cntt)
    cntt+=1
#     val=process.extractOne(cm_work_details[key],cm_bio[key])[1]
    bio=cm_bio[key].strip()
#     print(bio)

    work=cm_work_details[key].strip()
#     print("wor",work)
    work_len=len(work)+1
#     print(bio_len)
    cnt=0
    for word in work:
        if word in work:
            cnt+=1
        else:
            continue 
    val=(cnt*100)/work_len
    print("val :", val)
    fuzzy_dict[key]=val
    if val<50:
        print("=====")
        print("Biography :\n ", cm_bio[key])
        print("=================================================")
        print("Employment details :\n ", cm_work_details[key])
        print("=================================================")
print(len(fuzzy_dict))





