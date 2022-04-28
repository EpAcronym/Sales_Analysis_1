# Import packages
import pandas as pd
import math
import datetime as dt
import seaborn as sns
import matplotlib.pyplot as plt
import xlsxwriter

#Requirement 1: import csv

#Function to read_csv
def read_csv():
    pd.read_csv(sales)
    return read_csv

#csv being read and info
sales = pd.read_csv('supermarket_sales.csv') # import csv
sales.info()

#Format title and date
sales_gross = sales.rename(columns = {'gross income': 'gross profit'}) #rename column
sales_gross['Date'] = pd.to_datetime(sales_gross['Date']) # convert to datetime data type
sales_gross['Date'] = pd.to_datetime(sales_gross['Date']).dt.strftime('%B %Y').str.lower().sort_values() #convert date to month and year format
print(sales_gross.head()) # check first 5 lines of table

#Requirement 2: create a list from sales MoM

#Create groups according to month and sum figures

sales_gross_group = sales_gross.groupby(['Date'], as_index = False).sum().round(2) #group rows of data based on date
new_order = ['january 2019', 'february 2019', 'march 2019'] #Next three rows of text are needed to ensure that data is sorted according to month and not alphabetically
sales_gross_group.index = pd.CategoricalIndex(sales_gross_group['Date'], categories=new_order, ordered = True)
sales_sort = sales_gross_group.sort_index().reset_index(drop = True) # gets the dataframe cols in the correct order
sales_sort.drop(['gross margin percentage', 'Rating'], axis=1, inplace=True) ## Delete these columns as they don't make sense cumulatively
pd.set_option("display.max_rows", None, "display.max_columns", None) ### full table displayed when run script

# create list of sales and profit summations and print
mom_breakdown_sales = sales_sort[['Date', 'Total']] # sales in a list by month
mom_breakdown_profit = sales_sort[['Date', 'gross profit']] # profit in a list by month

print(mom_breakdown_sales)
print(mom_breakdown_profit)

#Requirement 3: print total sales

mom_sales_total = sales_sort['Total'] # only numerical values cab be summed so a new numerically exclusive list is called
sales_total = sum(mom_sales_total)
print(f'Total sales were: £{sales_total:,} for Jan - Mar 2019')


#print(f'Total sales were: £{sales_total:,.2f} for Jan - Mar 2019') - Don't need 2f already rounded in groupby

#Extension

#% changes

sales_sort['gross profit margin'] = (sales_sort['gross profit']/sales_sort['Total'])*100
sales_sort['sales (total) - % change'] = (sales_sort['Total'].pct_change())*100
sales_sort['cogs - % change'] = (sales_sort['cogs'].pct_change())*100
sales_sort['quantity - % change'] = (sales_sort['Quantity'].pct_change())*100
sales_sort['gross profit - % change'] = (sales_sort['gross profit'].pct_change())*100

sales_sort_0 = sales_sort.fillna(0) # get rid of Nan at start of data for % change

print(sales_sort_0)

#Save cleaned data to excel sheet
#def create_sheet(writer, sales_sort, sheet_name): -what does sales_sort do here? was blanked out

#function to create sheet
def create_sheet(writer, sheet_name):
    return sales_sort_0.to_excel(writer, sheet_name = sheet_name)

writer = pd.ExcelWriter('Flash report.xlsx', engine='xlsxwriter')
sales_sort.to_excel(writer, sheet_name='flash')
writer.save()

#Graphs

#MOM (create and save as png)
sales_bar = sns.barplot(x = 'Date', y = 'Total', data = sales_gross_group, order= new_order)
plt.title('Sales MoM', size = 18)
plt.xlabel('Months', size = 12)
plt.ylabel('Sales (USD)', size = 12)
fig1 = plt.gcf()
plt.show()
#plt.draw() this isn't an urgent need to run the code
fig1.savefig('MOM.png')


#MOM descending (create and save as png)
sales_bar_hig_low = sns.barplot(x = 'Date', y = 'Total', data = sales_gross_group, order= sales_gross_group.sort_values('Total', ascending = False).Date)
plt.title('Sales in Descending Order', size = 18)
plt.xlabel('Months', size = 12)
plt.ylabel('Sales (USD)', size = 12)
fig2 = plt.gcf()
plt.show()
#plt.draw this isn't an urgent need to run the code
fig2.savefig('Descending.png')

