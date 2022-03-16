from operator import index
from telnetlib import theNULL
import pandas as pd
import numpy as np
from pyparsing import col


def orderList(s):
    elements = s.split(',')
    elements.sort()      
    return ("".join(elements))
    

df_original = pd.read_json('grades_original.json')

#remove parent courses, only keeps courses with subcourse
df = df_original[df_original['ordering'] != 'null']

#df['idParentCourseConverted'] = [row[row.rindex('-')+1:len(row)-1] if row!='null' else 'null' for row in df['parentIdCourse']] 

#df['idCourseConverted'] = [row[row.rindex('-')+1:len(row)-1] if row!='null' else 'null' for row in df['idCourse']] 



#subselect only columns for grouping
df_select = df[['parentIdCourse','labelGroup','idCourse']]

#delete duplicates
df_unique = df_select.drop_duplicates()

#obtain labelGroup by parentIdCourse --union of same labelgroup
df_group_concat = df_unique.groupby(['parentIdCourse' ])[['labelGroup']].agg(lambda x: ','.join(x))

#order by subcourse
df_group_concat['labelGroup'] =  df_group_concat['labelGroup'].apply(orderList) 

df_group_concat = df_group_concat.reset_index()

#group by unique labelGroups
df_unique_ids = df_group_concat.groupby(['labelGroup'])[['parentIdCourse']].agg(lambda x: ','.join(x))

df_unique_ids = df_unique_ids.reset_index()

#we obtain every group of courses having the same labelGroup (complete set of subcourses sharing the same number and type of labelgroup)
for i in range(len(df_unique_ids)):
    parents = df_unique_ids.loc[i,"parentIdCourse"].split(',')
    boolean_series = df_original.parentIdCourse.isin(parents)    
    filtered_df = df_original[boolean_series]
    #print("filtered_df")
    #print(filtered_df)

    print("groupby final")
    #this block pivots table by subcourse, mark,...,extra3 and term
    group_course = pd.pivot_table(filtered_df,index=["idPerson","personName","parentIdCourse","parentCourseName","position"],values=["mark"],columns=["labelGroup","idTerm"],aggfunc="first")
    group_course = group_course.sort_values(["parentIdCourse", "personName"], ascending = (True, True))
    print(group_course)  
    



    
    


#this block pivots table per mark,absence..., extra3 and term
tr = pd.pivot_table(df_original,index=["idPerson","personName","idCourse","courseName","position","ordering"],values=["mark","absence","behaviour","note","extra1","extra2","extra3"],columns=["idTerm"],aggfunc="first")
tr = tr.sort_values(["personName", "position","ordering"], ascending = (True, True,False))
print("MATERIA GENERAL")
print(tr)


"""

group_course = pd.pivot_table(df,index=["idPerson","personName","parentIdCourse"],values=["mark"],columns=["idCourse","idTerm"],aggfunc="first")
print(group_course)
print(group_course.info())
group_course.to_csv("result.csv")
"""

