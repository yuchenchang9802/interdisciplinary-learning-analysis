import pandas as pd
import pymssql

# MSSQL database connection
def create_connection():
    return pymssql.connect(
        server='YOUR_SERVER',
        user='YOUR_USERNAME',
        password='YOUR_PASSWORD',
        database='YOUR_DATABASE'
    )

# Execute SQL query and convert results to DataFrame
def execute_query(query):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(query)

    data = cursor.fetchall()
    columns = [column[0] for column in cursor.description]

    df = pd.DataFrame(data, columns=columns)

    cursor.close()
    conn.close()

    return df

# MSSQL Queries
# Student basic information
std_basicinfo_query = """
SELECT *
FROM D_STDBASICINFO;
"""

# Filter master's students who previously completed their undergraduate studies at NCU
master_std_query = """
SELECT * 
FROM D_STDBASICINFO 
WHERE i_reason LIKE '6%' and school = '00081';
"""

# Undergraduate student records
college_std_query = """
SELECT * 
FROM D_STDBASICINFO 
WHERE i_reason = '01' or i_reason = '03' or i_reason LIKE '1%' or i_reason LIKE '2%' or i_reason LIKE '3%' or i_reason LIKE '4%' or i_reason LIKE '5%';
"""

# Filter interdisciplinary course enrollment records by excluding general education and home department courses
course_select_query = """
SELECT F_SEMESTER_CRS_SELECT.semester, F_SEMESTER_CRS_SELECT.s_id, D_STDBASICINFO.dept_now, D_STDBASICINFO.assis_degree_flag, 
       D_STDBASICINFO.double_degree_flag, D_STDBASICINFO.leave_school_name, D_STDBASICINFO.leave_dept_name, D_STDBASICINFO.leave_group_name, 
       F_SEMESTER_CRS_SELECT.crs_no, D_CRS.degree_kind_no, D_COURSE_DEPARTMENT.degree_kind_name AS course_degree_kind_name, D_CRS.crs_cname
FROM F_SEMESTER_CRS_SELECT
JOIN D_STDBASICINFO
ON F_SEMESTER_CRS_SELECT.s_id = D_STDBASICINFO.s_id
JOIN D_CRS
ON F_SEMESTER_CRS_SELECT.crs_no = D_CRS.crs_no
JOIN D_COURSE_DEPARTMENT
ON D_CRS.degree_kind_no = D_COURSE_DEPARTMENT.degree_kind_no AND D_CRS.degree_kind = D_COURSE_DEPARTMENT.degree_kind
WHERE D_CRS.degree_kind_no != N'0000' AND D_CRS.degree_kind_no != N'0001' AND D_CRS.degree_kind_no != N'0005'
AND D_CRS.degree_kind_no != N'0006' AND D_CRS.degree_kind_no != N'0008' AND D_CRS.degree_kind_no != N'0009'
AND D_CRS.degree_kind_no != N'0010' AND D_CRS.degree_kind_no != N'0011' AND D_CRS.degree_kind_no != N'1000'
AND D_STDBASICINFO.dept_now != D_CRS.degree_kind_no AND D_STDBASICINFO.leave_dept_name NOT LIKE N'%碩士%'
AND D_STDBASICINFO.leave_dept_name NOT LIKE N'%博士%' AND F_SEMESTER_CRS_SELECT.crs_type_no != 1
ORDER BY F_SEMESTER_CRS_SELECT.semester, F_SEMESTER_CRS_SELECT.s_id, D_CRS.degree_kind_no;
"""

# Query turn to DataFrame
std_basicinfo_df = execute_query(std_basicinfo_query)
master_std_df = execute_query(master_std_query)
college_std_df = execute_query(college_std_query)
course_select_df = execute_query(course_select_query)

# Save dataset
std_basicinfo_df.to_excel("std_basicinfo_df.xlsx", index=False)
master_std_df.to_excel("master_std_df.xlsx", index=False)
college_std_df.to_excel("college_std_df.xlsx", index=False)
course_select_df.to_parquet("course_select_df.parquet", index=False)
