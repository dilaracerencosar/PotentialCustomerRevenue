#The Calculation of Potential Customer Revenue with Rule-Based Classification


# "Gezinomi" wants to create level-based new sales definitions using certain features of the sales
# they have made and then create segments based on these new sales definitions.
# The goal is to estimate how much potential new customers might bring in on average for the company according to these segments.
# For example, they want to determine the average revenue a customer who wants to go to an all-inclusive hotel in Antalya during a peak season might generate.


#Read the file miuul_gezinomi.xlsx and show general information about the data set.
import pandas as pd
pd.set_option("display.max_columns", None)

#I encountered an error while loading the dataset; it was caused by the backslashes (\) in the Windows file path being used as escape characters in Python.
#There are several ways to solve this issue, one of which is to define the file path as a raw string by prefixing it with the letter 'r'.
df = pd.read_excel(r"C:\Users\Dilara Ceren Coşar\OneDrive\Masaüstü\datasets\miuul_gezinomi.xlsx")

pd.set_option('display.float_format', lambda x: '%.2f' % x)
print(df.head())
print(df.shape)
print(df.info())


#How many unique cities are there? What are their frequencies?
print(df["SaleCityName"].nunique())
print(df["SaleCityName"].value_counts())


#How many unique Concept are there?
df["ConceptName"].nunique()


#How many sales were made from which Concept?
df["ConceptName"].value_counts()


#How much was earned from sales in total by city?
df.groupby("SaleCityName").agg({"Price": "sum"})


#How much was earned according to Concept types?
df.groupby("ConceptName").agg({"Price": "sum"})


#What are the PRICE averages by city?
df.groupby("SaleCityName").agg({"Price": "mean"})


#What are the PRICE averages according to concepts?
df.groupby("ConceptName").agg({"Price": "mean"})


#What are the PRICE averages in the City-Concept breakdown?
df.groupby(by=["SaleCityName", "ConceptName"]).agg({"Price": "mean"})



#####
# Convert the SaleCheckInDayDiff variable into a new categorical variable named EB_Score.
#####
bins = [-1, 7, 30, 90, df["SaleCheckInDayDiff"].max()]
labels = ["Last Minuters", "Potential Planners", "Planners", "Early Bookers"]

df["EB_Score"] = pd.cut(df["SaleCheckInDayDiff"], bins, labels=labels)
df.head(50).to_excel("eb_score.xlsx", index=False)


#####
# See wage averages and frequencies by City, Concept, [EB_Score, Season, CInday]
#####

#Wage averages in City-Concept-EB_Score breakdown
df.groupby(by=["SaleCityName", "ConceptName", "EB_Score"], observed=True).agg({"Price": ["mean", "count"]})
# !!! The warning you receive indicates a future change to the observed parameter used in Pandas' groupby function.
# This warning tells you that the behavior, which defaults to observed=False,
# will change to observed=True in the future, and that you must explicitly specify the observed parameter if you do not want to receive a silent warning about this change.
#Ignoring the warning and using observed=True to consider existing combinations results in faster processing and saves memory.


#Wage averages in City-Concept-Season breakdown
df.groupby(by=["SaleCityName", "ConceptName", "Seasons"]).agg({"Price":["mean", "count"]})

#Wage averages in City-Concept-CInDay breakdown
df.groupby(by=["SaleCityName", "ConceptName", "CInDay"]).agg({"Price":["mean", "count"]})


#####
# Sort the output of City-Concept-Season breakdown according to PRICE.
#####
# To better see the output in the previous question, apply the sort_values method to PRICE in decreasing order.
# Save the output as agg_df.

agg_df = df.groupby(["SaleCityName", "ConceptName", "Seasons"]).agg({"Price": "mean"}).sort_values("Price", ascending=False)
agg_df.head(20)


#####
# Convert the names in the index to variable names.
#####
# All variables except PRICE in the output of the third question are index names.
# Convert these names to variable names.
# hint: reset_index()
agg_df.reset_index(inplace=True) #The "inplace=True" parameter enables the operation to be applied directly on agg_df, i.e. it updates the existing DataFrame without creating a new DataFrame.
agg_df.head()


#####
# Define new level based sales and add them to the data set as a variable.
#####
# Define a variable called sales_level_based and add this variable to the dataset.
agg_df['sales_level_based'] = agg_df[["SaleCityName", "ConceptName", "Seasons"]].agg(lambda x: '_'.join(x).upper(), axis=1)


#####
# Divide personas into segments.
#####
# Segment by PRICE, add the segments to agg_df with the name "SEGMENT"
# describe the segments
agg_df["SEGMENT"] = pd.qcut(agg_df["Price"], 4, labels=["D", "C", "B", "A"])
agg_df.head(30)
agg_df.groupby("SEGMENT").agg({"Price": ["mean", "max", "sum"]})

#####
# Sort the final df according to the price variable.
# In which segment is "ANTALYA_HERŞEY DAHIL_HIGH" and how much is expected?
#####
agg_df.sort_values(by="Price")
new_user = "ANTALYA_HERŞEY DAHIL_HIGH"
agg_df[agg_df["sales_level_based"] == new_user]

