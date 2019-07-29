import pandas as pd


m_ans = pd.read_excel("ACT_Report_3.xlsm", sheet_name="M_Ans").T
header = m_ans.iloc[0]
m_ans = m_ans[1:]
m_ans = m_ans.rename(columns=header)
m_ans.index = range(0, 50)


sd_ans=pd.read_csv("P01_Answers.csv").T
header=sd_ans.iloc[0]
sd_ans = sd_ans[1:51]
sd_ans = sd_ans.rename(columns=header)
sd_ans.index = range(0, 50)


def math_grader(math_ans,sd_ans):
    index = []
    for num in range(len(math_ans["Key"])):
        record = []
        # checking answers
        ans = math_ans.iloc[num,0]
        if sd_ans.iloc[num,0] == ans:
            record.append(True)
            index.append(record)
        else:
            record.append(False)
            index.append(record)
    result = pd.DataFrame(index, columns = ["Grade"])
    math_ans['Grade'] = result['Grade']
    grade = pd.DataFrame(math_ans['Grade'].value_counts())
    grade["Ans"] = ["Right", 'Wrong']
    return math_ans, grade

math_result, grade_result = math_grader(m_ans, sd_ans)



# Data ACT Score

df_sd = pd.read_excel("Prestige_ACT_TEST_REPORT.xlsm", sheet_name = "Sheet1")
df_sd = df_sd.loc[:,["Name","English", "Math", "Reading", "Science", "Composite Score"] ]
abc=df_sd.drop("Name", axis=1).T
abc.columns = df_sd["Name"]

print(df_sd.columns[1:])



