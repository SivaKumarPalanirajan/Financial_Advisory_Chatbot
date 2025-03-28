from audioop import avg
import re
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os 
import pickle 

class FinBot:

    def __init__(self):
        global current_dir 
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, 'Data', 'transactions.xlsx')
        global df
        self.df = pd.read_excel(file_path)

    def greet(self):
        message = "Hi, I'm FINBOT, your personal financial advisor. Do you need any help?"
        return message
        
    def exit_pro(self):
        return "Okay, Thank you for using our service"
    
    def analyze_transaction_density(self,acc_no):
      filtered_based_on_accno_date=self.df.groupby(['Account No','VALUE DATE']).count()[['WITHDRAWAL AMT','DEPOSIT AMT']]
      transaction_density=filtered_based_on_accno_date['WITHDRAWAL AMT']+filtered_based_on_accno_date['DEPOSIT AMT']
      transaction_density=transaction_density[acc_no]
      avg_transaction_density = transaction_density.mean()
      max_transaction_density = transaction_density.max()
      min_transaction_density = transaction_density.min()
      return f"Average daily transaction density is {avg_transaction_density:.2f} <br> Maximum daily transaction density is {max_transaction_density} <br> Minimum daily transaction density is {min_transaction_density}"
      

    def predict_balance(self,acc_no,yr):
      file_path_regressor = os.path.join(current_dir, 'Models', 'regressor.sav')
      Regressor=pickle.load(open(file_path_regressor,"rb"))
      testing=[[acc_no,yr]]
      y_pred=Regressor.predict(testing)
      predicted=y_pred[0]
      return f"Predicted Balance for the account no {acc_no} by the {yr} is: {predicted:.2f}"
      


    def balance_evolution(self):
      self.df["DATE DAYS"] = self.date_to_float(self.df["VALUE DATE"])
      dates = pd.Series(self.df["DATE"])
      self.df["YEAR"] = dates.dt.year
      self.df["MONTH"] = dates.dt.month
      self.df["WEEK"] = dates.dt.isocalendar().week
      self.df["DAY"] = dates.dt.day
      self.df["DAYOFWEEK"] = dates.dt.dayofweek
        # Calculate statistics for account
      balance_mins = self.df["BALANCE AMT"].min()
      balance_maxs = self.df["BALANCE AMT"].max()
      balance_means = self.df["BALANCE AMT"].mean()
      balance_meds = self.df["BALANCE AMT"].median()   
      insights = []
        # Calculate insights for all accounts (no need to group by account)
      balance_data = self.df[["VALUE DATE", "BALANCE AMT"]].groupby("VALUE DATE").mean()
      max_drop = balance_data["BALANCE AMT"].diff().min()
      max_increase = balance_data["BALANCE AMT"].diff().max()
      if max_drop < -500000:
        insights.append(f"Experienced a significant drop in balance at some point.\n")
      elif max_increase > 500000:
        insights.append(f"Experienced a significant increase in balance at some point.\n")
        # Check if there is a trend in balance increase or decrease
      if max_increase > 0 and max_drop < 0:
        insights.append(f"Shows a trend of balance increase.\n")
      elif max_increase < 0 and max_drop > 0:
        insights.append(f"Shows a trend of balance decrease.\n")
        # Check if there are periods of high volatility
      balance_std = balance_data["BALANCE AMT"].std()
      if balance_std > 500000:
        insights.append(f"Experienced periods of high balance volatility.\n")
        # Print the generated insights
      insights_str = "\n".join(insights)

      result = f"Balance Evolution Insights:<br>"
      result += f"Minimum Balance: {balance_mins}<br>"
      result += f"Maximum Balance: {balance_maxs}<br>"
      result += f"Mean Balance: {balance_means:.2f}<br>"
      result += f"Median Balance: {balance_meds}<br><br>"
      if insights:
          result += "<br>".join(insights)
      else:
          result += "No significant insights found for this account."
      return result

    def no_match(self):
        responses = ("Can you rephrase your question again?","We can't seem to find a relevant answer for your question")
        return (random.choice(responses))

    def date_to_float(self, date_data):
        return (date_data - date_data.min()) / np.timedelta64(1, 'D')