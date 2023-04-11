import pandas as pd
import sys

# USUAGE python3 combine.py spring.csv fall.csv summer.csv

# load the three CSV files
spring_df = "spring-2022.csv"
fall_df = "fall-2022.csv"
summer_df = "summer-2022.csv"

# merge the dataframes and remove duplicates based on course_name and course_instructor columns
merged_df = pd.concat([spring_df, fall_df, summer_df]).reset_index(drop=True)
merged_df = merged_df.sort_values(by=['course_name', 'course_start_date'], ascending=False)
merged_df = merged_df.drop_duplicates(subset=['course_name', 'course_instructor'], keep='first')

# create the box column based on course_name presence in each of the three original dataframes
merged_df['box'] = ''
merged_df.loc[merged_df['course_name'].isin(spring_df['course_name']) &
              merged_df['course_name'].isin(fall_df['course_name']) &
              merged_df['course_name'].isin(summer_df['course_name']), 'box'] = 'S F U'
merged_df.loc[merged_df['course_name'].isin(spring_df['course_name']) &
              merged_df['course_name'].isin(summer_df['course_name']) &
              ~merged_df['course_name'].isin(fall_df['course_name']), 'box'] = 'S U'
merged_df.loc[merged_df['course_name'].isin(fall_df['course_name']) &
              merged_df['course_name'].isin(summer_df['course_name']) &
              ~merged_df['course_name'].isin(spring_df['course_name']), 'box'] = 'F U'
merged_df.loc[merged_df['course_name'].isin(spring_df['course_name']) &
              merged_df['course_name'].isin(fall_df['course_name']) &
              ~merged_df['course_name'].isin(summer_df['course_name']), 'box'] = 'S F'
merged_df.loc[~merged_df['course_name'].isin(spring_df['course_name']) &
              merged_df['course_name'].isin(fall_df['course_name']) &
              ~merged_df['course_name'].isin(summer_df['course_name']), 'box'] = 'F'
merged_df.loc[merged_df['course_name'].isin(spring_df['course_name']) &
              ~merged_df['course_name'].isin(fall_df['course_name']) &
              ~merged_df['course_name'].isin(summer_df['course_name']), 'box'] = 'S'
merged_df.loc[~merged_df['course_name'].isin(spring_df['course_name']) &
              ~merged_df['course_name'].isin(fall_df['course_name']) &
              merged_df['course_name'].isin(summer_df['course_name']), 'box'] = 'U'

# write the merged dataframe to a new CSV file
merged_df.to_csv('merged.csv', index=False)