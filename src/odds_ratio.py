import pandas as pd
import numpy as np

cohort_df = pd.read_parquet('interdisciplinary_cohort_dataset.parquet')

# OR
def compute_odds_ratio(group, exposure_column, outcome_column):
    a = len(group[
        (group[exposure_column] == 1) &
        (group[outcome_column] == 1)
    ])

    b = len(group[
        (group[exposure_column] == 1) &
        (group[outcome_column] == 0)
    ])

    c = len(group[
        (group[exposure_column] == 0) &
        (group[outcome_column] == 1)
    ])

    d = len(group[
        (group[exposure_column] == 0) &
        (group[outcome_column] == 0)
    ])

    if b == 0 or c == 0:
        odds_ratio = None
    else:
        odds_ratio = round((a * d) / (b * c), 4)

    return {
        'a': a,
        'b': b,
        'c': c,
        'd': d,
        'odds_ratio': odds_ratio
    }

# Multilevel Odds Ratio Framework
def calculate_multilevel_odds_ratios(df, group_levels, outcome_column='cross_domain'):
    results = []
    grouped_df = df.groupby(group_levels)

    for group_name, group_data in grouped_df:
        # Cross-department course exposure
        cross_department_result = compute_odds_ratio(
            group_data,
            exposure_column='cross_department_course',
            outcome_column=outcome_column
        )

        # Cross-college course exposure
        cross_college_result = compute_odds_ratio(
            group_data,
            exposure_column='cross_college_course',
            outcome_column=outcome_column
        )

        result_row = {
            'group': group_name,
            'cross_department_odds_ratio': cross_department_result['odds_ratio'],
            'cross_college_odds_ratio': cross_college_result['odds_ratio']
        }

        results.append(result_row)

    return pd.DataFrame(results)

# College-Level Odds Ratio Analysis
college_level_or_df = calculate_multilevel_odds_ratios(cohort_df, ['leave_school_name'])

print('College-Level Odds Ratio Analysis')
print(college_level_or_df)

# Department-Level Odds Ratio Analysis
college_department_or_df = calculate_multilevel_odds_ratios(cohort_df, ['leave_school_name', 'degree_kind_name_x'])

print('\nDepartment-Level Odds Ratio Analysis')
print(college_department_or_df)


college_level_or_df.to_excel('college_level_odds_ratio_analysis.xlsx', index=False)

college_department_or_df.to_excel('department_level_odds_ratio_analysis.xlsx', index=False)
