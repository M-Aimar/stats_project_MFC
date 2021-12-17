import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

sns.set()

raw_data = pd.read_csv('Billionaire.csv.xls')

raw_data['NetWorth'] = raw_data['NetWorth'].str.strip('$')

raw_data['NetWorth'] = raw_data['NetWorth'].str.strip(' B')

raw_data['NetWorth'] = pd.to_numeric(raw_data['NetWorth'], downcast='integer')

raw_data['Industry'].replace({'Media & Entertainment': 'Media', 'Construction & Engineering': 'Construction', 'Gambling & Casinos': 'Casinos'}, inplace=True)


clean_df = raw_data.drop(['Source', 'Rank'], axis=1)
clean_df['Industry_dummies'] = clean_df['Industry'].map({'Technology':0, 'Automotive':1, 'Fashion & Retail': 2, 'Finance & Investments':3, 'Diversified':4, 'Food & Beverage':5, 'Telecom':6, 'Media':7, 'Service':10, 'Casinos':11, 'Manufacturing':12, 'Real Estate':13, 'Metals & Manufacturing':14, 'Energy':15, 'Logistics':16, 'Healthcare':17, 'Construction':18, 'Sports':19 })
clean_df.dropna(axis=0, inplace=True)



while True:
    plot = input('''Hi what plot would you like to see?
    If you would like to see the how many billionaires there are per industry press 1
    If you would like a scatter plot of billionaires and their ages press 2
    ''')
    if plot == '1':
        plt.pie(pd.value_counts(clean_df['Industry']), labels=clean_df['Industry'].unique(), rotatelabels=True,
                labeldistance=1)
        plt.show()
    elif plot == '2':
        plt.scatter(clean_df['Age'], clean_df['NetWorth'])
        plt.xlabel('Age')
        plt.ylabel('Net Worth in billions')
        plt.title('Relationship between age and net worth')
        plt.show()

    new_pass = input('Would you like to see another plot? Yes or No')

    if new_pass.lower().startswith('n'):
        break


# Understanding the dataset
explore = clean_df.describe(include='all')

# Investigating the relationship between Age and net worth
y = clean_df['NetWorth']
x1 = clean_df['Age']
x = sm.add_constant(x1)

relationship = sm.OLS(y, x).fit()
netWorth_age = relationship.summary()

# Investigating the relationship between Industry and net worth
y = clean_df['NetWorth']
x1 = clean_df['Industry_dummies']
x = sm.add_constant(x1)

relationship = sm.OLS(y, x).fit()
industry_netWorth = relationship.summary()

# Investigating the relationship between both Industry and Age with net worth
y = clean_df['NetWorth']
x1 = clean_df[['Industry_dummies', 'Age']]
x = sm.add_constant(x1)

relationship = sm.OLS(y, x).fit()
industry_age_netWorth = relationship.summary()
