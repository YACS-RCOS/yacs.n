import pandas as pd
#load 2011 and 2022 data
df_2021 = pd.read_csv("spring-2021.csv")
df_2022 = pd.read_csv("spring-2022.csv")
#loop for 2022 course data
for i in range(df_2022.shape[0]):
    # get course name
    course_name_2022 = df_2022.loc[i,"course_name"]
    # loop for other columns
    for column in df_2022.columns.to_list()[1:]:
        # if the column in this row is missing
        if pd.isna(df_2022.loc[i,column]) or df_2022.loc[i,column] =="[]":
            # if Corresponding infomation is not null, fill with the first value
            if df_2021[df_2021["course_name"]==course_name_2022][column].shape[0]!=0:
                df_2022.loc[i,column] = df_2021[df_2021["course_name"]==course_name_2022][column].values[0]
# store
df_2022.to_csv("spring-2023.csv",index=0)