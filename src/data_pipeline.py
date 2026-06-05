import pandas as pd

# Load datasets
college_std_df = pd.read_excel('college_std_df.xlsx')
master_std_df = pd.read_excel('master_std_df.xlsx')
duplicated_std_df = pd.read_excel('duplicated_std_df.xlsx')
course_select_df = pd.read_parquet('course_select_df.parquet')

# Undergraduate Student Filtering
# Remove records with missing semester information
filter_college_std_df = college_std_df[college_std_df['i_semester'].notna()].reset_index(drop=True)
filter_college_std_df.to_excel('filtered_undergraduate_students.xlsx', index=False)

# Master Student Matching
filter_master_std_df = master_std_df[master_std_df['p_id'].isin(filter_college_std_df['p_id'])]
final_master_std_df = filter_master_std_df[filter_master_std_df['p_id'].isin(duplicated_std_df['p_id'])].reset_index(drop=True)

# Course Enrollment Filtering
course_select_df = std_course_select_df[std_course_select_df['s_id'].isin(final_college_std_df['s_id']) ].reset_index(drop=True)

# Remove students with minor or double major programs
course_select_df = course_select_df[(course_select_df['assis_degree_flag'] != 1) & (course_select_df['double_degree_flag'] != 1)]
course_select_df = course_select_df.drop(columns=['assis_degree_flag', 'double_degree_flag']).reset_index(drop=True)

# Interdisciplinary Course Filtering
# Similar filtering logic was applied to other colleges and departments
department_course_patterns = {'地球科學學院學士班': 'GP|AP|EA', 
                              '工學院學士班': 'EG|CH|CI|ME', 
                              '理學院學士班': 'CM|JS|LS|MA|OS|PH|SH'}

# Remove department-owned courses
for dept, pattern in department_course_patterns.items():
    mask = (
        (course_select_df['leave_dept_name'] == dept) &
        (course_select_df['crs_no'].str.contains(pattern))
    )
    course_select_df = course_select_df[~mask]

# Additional department-specific filtering
science_extra_conditions = ((course_select_df['leave_dept_name'] == '理學院學士班') & 
                            (
                              (course_select_df['course_degree_kind_name'] == '大氣科學學系(大氣組)') | 
                              (course_select_df['course_degree_kind_name'] == '大氣科學學系(太空組)') | 
                              (course_select_df['course_degree_kind_name'] == '機械工程學系光機電工程組') | 
                              (course_select_df['course_degree_kind_name'] == '機械工程學系先進材料與精密製造') | 
                              (course_select_df['course_degree_kind_name'] == '機械工程學系設計與分析組') 
                            ))
course_select_df = course_select_df[~science_extra_conditions ].reset_index(drop=True)

course_select_df.to_parquet('processed_interdisciplinary_learning_dataset.parquet', index=False)
