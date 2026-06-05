import pandas as pd

# Undergraduate Student Filtering
# Remove records with missing semester information
filter_College_std_df = College_std_df[College_std_df['i_semester'].notna()].reset_index(drop=True)
filter_College_std_df.to_excel('filtered_undergraduate_students.xlsx', index=False)

# Master Student Matching
filter_Master_std_df = Master_std_df[Master_std_df['p_id'].isin(filter_College_std_df['p_id'])]
final_Master_std_df = filter_Master_std_df[filter_Master_std_df['p_id'].isin(duplicated_std_df['p_id'])].reset_index(drop=True)

# Course Enrollment Filtering
College_std_course_df = std_course_select_df[std_course_select_df['s_id'].isin(final_College_std_df['s_id']) ].reset_index(drop=True)

# Remove students with minor or double major programs
College_std_course_df = College_std_course_df[(College_std_course_df['assis_degree_flag'] != 1) & (College_std_course_df['double_degree_flag'] != 1)]
College_std_course_df = College_std_course_df.drop(columns=['assis_degree_flag', 'double_degree_flag']).reset_index(drop=True)

# Interdisciplinary Course Filtering
# Similar filtering logic was applied to other colleges and departments
department_course_patterns = {'地球科學學院學士班': 'GP|AP|EA', 
                              '工學院學士班': 'EG|CH|CI|ME', 
                              '理學院學士班': 'CM|JS|LS|MA|OS|PH|SH'}

# Remove department-owned courses
for dept, pattern in department_course_patterns.items():
  mask = ((College_std_course_df['leave_dept_name'] == dept) & (College_std_course_df['crs_no'].str.contains(pattern))) College_std_course_df = College_std_course_df[~mask]

# Additional department-specific filtering
science_extra_conditions = ((College_std_course_df['leave_dept_name'] == '理學院學士班') & 
                            (
                              (College_std_course_df['course_degree_kind_name'] == '大氣科學學系(大氣組)') | 
                              (College_std_course_df['course_degree_kind_name'] == '大氣科學學系(太空組)') | 
                              (College_std_course_df['course_degree_kind_name'] == '機械工程學系光機電工程組') | 
                              (College_std_course_df['course_degree_kind_name'] == '機械工程學系先進材料與精密製造') | 
                              (College_std_course_df['course_degree_kind_name'] == '機械工程學系設計與分析組') 
                            ))
College_std_course_df = College_std_course_df[~science_extra_conditions ].reset_index(drop=True)

College_std_course_df.to_parquet('processed_interdisciplinary_learning_dataset.parquet', index=False)
