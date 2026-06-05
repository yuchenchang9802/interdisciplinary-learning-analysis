import pandas as pd
import numpy as np

# Load Datasets
master_basicinfo_df = pd.read_excel('master_students_filtered.xlsx').sort_values('p_id')
college_basicinfo_df = pd.read_excel('college_students_filtered.xlsx').sort_values('p_id')
department_code_df = pd.read_excel('department_codes.xlsx')

department_code_df = department_code_df.drop_duplicates(subset=['degree_kind_no'])
department_code_df = department_code_df.rename(columns={'degree_kind_no': 'department_code'})

# Construct Student Information Tables
master_info_df = master_basicinfo_df[['p_id', 'dept_now']].rename(columns={'dept_now': 'master_department_code'})
college_info_df = college_basicinfo_df[['p_id', 's_id', 'dept_now', 'leave_school_name']].rename(columns={'dept_now': 'college_department_code'})

# Department Name Mapping
master_department_df = pd.merge( master_info_df, department_code_df, left_on='master_department_code', right_on='department_code', how='left')
college_department_df = pd.merge(college_info_df, department_code_df, left_on='college_department_code', right_on='department_code', how='left')
student_mixed_df = pd.merge(college_department_df, master_department_df, on='p_id', how='inner')

# ----------------------------------------
# Interdisciplinary Further Education Label
# Compare the first digit of department codes, if same category -> non-interdisciplinary; Different category -> interdisciplinary
student_mixed_df['cross_domain'] = np.where(student_mixed_df['college_department_code'].astype(str).str[0] != student_mixed_df['master_department_code'].astype(str).str[0], 1, 0)

# Cross-Department Course Enrollment Label
cross_department_students = allcourse_df['s_id'].unique()
student_mixed_df['cross_department_course'] = np.where(student_mixed_df['s_id'].isin(cross_department_students), 1, 0)

# Cross-College Course Enrollment Label
cross_college_students = academy_df['s_id'].unique()
student_mixed_df['cross_college_course'] = np.where(student_mixed_df['s_id'].isin(cross_college_students), 1, 0)

# Statistical Summary
cross_domain_summary = student_mixed_df.groupby('leave_school_name')['cross_domain'].sum()

student_mixed_df.to_parquet('interdisciplinary_cohort_dataset.parquet', index=False)
