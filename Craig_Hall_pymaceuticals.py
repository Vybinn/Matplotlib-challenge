#!/usr/bin/env python
# coding: utf-8

# ## Three summary observations from the data
# Instead of looking at three drugs and the placebo, I looked at four drugs plus the placebo. Based on an initial reading of the raw data, it looked like there might be multiple successful drugs.
# 1. Of the four observed drugs, one drug performed WORSE than the placebo (Ketapril).  The increase in tumor volume for mice that recieved this drug was larger than in mice receiving the placebo. 
# 2. Only two drugs were successful in decreasing the tumor volume.  Those two drugs also had the lowest mortality rate, and the lowest rate of metastic site spreading (Capomulin, Ramicane).
# 3. Ramicane was the most successful drug in the study.  It had the lowest mortality rate during the treatment period, it decreased the volume of tumors by the largest percentage, and resulted in the lowest rate of metastatic spread.  

# In[285]:


# Dependencies and Setup
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Hide warning messages in notebook
import warnings
warnings.filterwarnings('ignore')

# File to Load (Remember to Change These)
mouse_drug_data_to_load = "data/mouse_drug_data.csv"
clinical_trial_data_to_load = "data/clinicaltrial_data.csv"

# Read the Mouse and Drug Data and the Clinical Trial Data
mouse_drug_data = pd.read_csv(mouse_drug_data_to_load)
clinical_trial_data = pd.read_csv(clinical_trial_data_to_load)


# Combine the data into a single dataset
merge_table = pd.merge (mouse_drug_data, clinical_trial_data, on="Mouse ID", how = "outer")

# Display the data table for preview
merge_table.head()




# ## Tumor Response to Treatment

# In[286]:


# Store the Mean Tumor Volume Data Grouped by Drug and Timepoint 
by_drug = merge_table[["Drug", "Timepoint", "Tumor Volume (mm3)"]]
by_drug_df = by_drug.groupby(["Drug", "Timepoint"])
by_drug_df.mean()

# Convert to DataFrame
by_drug_pd_df = pd.DataFrame(by_drug_df.mean().reset_index())

# Preview DataFrame
by_drug_pd_df.head(20)


# In[287]:


# Store the Standard Error of Tumor Volumes Grouped by Drug and Timepoint
by_drug_sem_df = pd.DataFrame(by_drug_df.sem().reset_index())
tumor_sem_df = by_drug_sem_df.rename(columns={"Tumor Volume (mm3)" : "SEM/Tumor Volume"})

# Preview DataFrame
tumor_sem_df.head(20)


# In[288]:


# Minor Data Munging to Re-Format the Volume Data Frames
by_timepoint_pivot = by_drug_pd_df.pivot(index="Timepoint", columns = "Drug", values = "Tumor Volume (mm3)")

# Preview that Reformatting worked
by_timepoint_pivot.head(10)


# In[289]:


## Minor Data Munging to Re-Format the SEM Data Frames
by_timepoint_sem_pivot = tumor_sem_df.pivot(index = "Timepoint", columns = "Drug", values = "SEM/Tumor Volume")
by_timepoint_sem_pivot.head(10)


# In[290]:


#Obtain data for each drug for plotting y axis
capo_vol = by_timepoint_pivot["Capomulin"]
infu_vol = by_timepoint_pivot["Infubinol"]
keta_vol = by_timepoint_pivot["Ketapril"]
plac_vol = by_timepoint_pivot["Placebo"]
rami_vol = by_timepoint_pivot["Ramicane"]
capo_sem_vol = by_timepoint_sem_pivot["Capomulin"]
infu_sem_vol = by_timepoint_sem_pivot["Infubinol"]
keta_sem_vol = by_timepoint_sem_pivot["Ketapril"]
plac_sem_vol = by_timepoint_sem_pivot["Placebo"]
rami_sem_vol = by_timepoint_sem_pivot["Ramicane"]


# In[291]:


#Get keys for x axis
timepoint = list(by_timepoint_pivot.index.values) 


# In[292]:


# Generate the Plot (with Error Bars)
capo_plt, = plt.plot(timepoint, capo_vol, marker="*",color="blue", linewidth=1, label="Capomulin")
infu_plt, = plt.plot(timepoint, infu_vol, marker="s", color="red", linewidth=1, label="Infubinol")
keta_plt, = plt.plot(timepoint, keta_vol, marker="o", color = "purple", linewidth=1, label="Ketapril")
plac_plt, = plt.plot(timepoint, plac_vol, marker="x", color = "yellow", linewidth=1, label="Placebo") 
rami_plt, = plt.plot(timepoint, rami_vol, marker="^", color = "green", linewidth=1, label = "Ramicane")

#Set aesthetics, title and axis labels
plt.ylabel("Tumor Volume (mm3)")
plt.xlabel("Treatment Duration (Days)")
plt.title("Tumor Response to Treatment")
plt.grid(True)

#Plot legend
plt.legend(loc="best")

# Save the Figure
plt.savefig('Tumor_Response_to_Treatment.png') 


# ## Metastatic Response to Treatment

# In[293]:


#Create a new Data Frame for the Metastatic Response columns
meta_sites=merge_table[["Drug", "Timepoint", "Metastatic Sites"]]
meta_sites


# In[294]:


# Store the Mean Met. Site Data Grouped by Drug and Timepoint 
meta_sites_bydrug = meta_sites.groupby(["Drug", "Timepoint"])
meta_sites_bydrug.mean()


# Convert to DataFrame
meta_mean_df = pd.DataFrame(meta_sites_bydrug.mean().reset_index())

# Preview DataFrame
meta_mean_df


# In[295]:


# Store the Standard Error associated with Met. Sites Grouped by Drug and Timepoint 
meta_sites_sem = meta_sites.groupby(['Drug', 'Timepoint']).sem()


# Convert to DataFrame
meta_sites_sem_df = pd.DataFrame(meta_sites_sem.reset_index())

# Preview DataFrame
meta_sites_sem_df.head(15)
ms_sites_df = meta_sites_sem_df.rename(columns={"Metastatic Sites": "Meta Sites SEM"})
ms_sites_df


# In[296]:


# Minor Data Munging to Re-Format the Data Frames
meta_mean_org_df = meta_mean_df.pivot(index="Timepoint", columns = "Drug", values = "Metastatic Sites")
meta_mean_org_df.head(10)
meta_org_df = meta_mean_org_df[["Capomulin", "Infubinol", "Ketapril", "Placebo", "Ramicane"]]

# Preview that Reformatting worked
meta_org_df


# In[297]:


# Minor Data Munging to Re-Format the Data Frames
meta_sites_sem__org_df = ms_sites_df.pivot(index="Timepoint", columns = "Drug", values = "Meta Sites SEM")

# Preview that Reformatting worked
meta_sites_sem__org_df.head(15)
meta_sites_df = meta_sites_sem__org_df[["Capomulin", "Infubinol", "Ketapril", "Placebo", "Ramicane"]]
meta_sites_df


# In[298]:


# Generate the Plot (with Error Bars)

#Set the x-axis
timepoint = list(meta_org_df.index.values)

#Obtain data for each drug for plotting y axis
capo_metam = meta_org_df["Capomulin"]
infu_metam = meta_org_df["Infubinol"]
keta_metam = meta_org_df["Ketapril"]
plac_metam = meta_org_df["Placebo"]
rami_metam = meta_org_df["Ramicane"]
capo_metas = meta_sites_df["Capomulin"]
infu_metas = meta_sites_df["Infubinol"]
keta_metas = meta_sites_df["Ketapril"]
plac_metas = meta_sites_df["Placebo"]
rami_metas = meta_sites_df["Ramicane"]

#Set limits, create labels and grid
plt.grid(True)
plt.ylabel("# Of Met Sites")
plt.xlabel("Treatment Duration (Days)")
plt.title("Metastatic Spread During Treatment")

#Plot drugs
plt.errorbar(timepoint, capo_metam, capo_metas, marker = "*", ms = 10, label = "Capomulin")
plt.errorbar(timepoint, infu_metam, infu_metas, marker = "s", ms = 8, label = "Infubinol")
plt.errorbar(timepoint, keta_metam, keta_metas, marker = "o", ms = 8, label = "Ketapril")
plt.errorbar(timepoint, plac_metam, plac_metas, marker = "x", ms = 8, label = "Placebo")
plt.errorbar(timepoint, rami_metam, rami_metas, marker = "^", ms = 8, label = "Ramicane")

#Add a legend
plt.legend(loc="best")

# Save the Figure
plt.savefig('Metastatic_Site_Spread.png') 


# Show the Figure


# ![Metastatic Spread During Treatment](../Images/spread.png)

# ## Survival Rates

# In[299]:


# Store the Count of Mice Grouped by Drug and Timepoint (W can pass any metric)
survival = merge_table [["Mouse ID", "Drug", "Timepoint"]] 
survival_df = survival.groupby(["Drug", "Timepoint"])

# Convert to DataFrame
survival_stats = pd.DataFrame(survival_df.count().reset_index())
survival_stats_df = survival_stats.rename(columns={"Mouse ID": "Living Mice"})

# Preview DataFrame
survival_stats_df


# In[300]:


#Determine the survival rate as a percentage of living mice
survival_stats_df["% Survived"] = survival_stats_df["Living Mice"] / 25 * 100 
survival_stats_df


# In[301]:


# Minor Data Munging to Re-Format the Data Frames

perc_survived_df = survival_stats_df.pivot(index="Timepoint", columns = "Drug", values = "% Survived")
perc_survived_df = perc_survived_df[["Capomulin", "Infubinol", "Ketapril", "Placebo", "Ramicane"]]
num_survived_df = survival_stats_df.pivot(index="Timepoint", columns = "Drug", values = "Living Mice")
num_survived_df = num_survived_df[["Capomulin", "Infubinol", "Ketapril", "Placebo", "Ramicane"]]


# Preview the Data Frame
perc_survived_df


# In[302]:


# Generate the Plot (Accounting for percentages)

#Set the x-axis
timepoint = list(perc_survived_df.index.values)

#Grab data for each drug for plotting y axis
capo_perc = perc_survived_df["Capomulin"]
infu_perc = perc_survived_df["Infubinol"]
keta_perc = perc_survived_df["Ketapril"]
plac_perc = perc_survived_df["Placebo"]
rami_perc = perc_survived_df["Ramicane"]


#Set limits, create labels and grid
plt.grid(True)
plt.ylabel("Survival Rate (%)")
plt.xlabel("Treatment Duration (Days)")
plt.title("Survival During Treatment")

#Plot drugs
plt.plot(timepoint, capo_perc, marker = "*", ms = 10, label = "Capomulin")
plt.plot(timepoint, infu_perc, marker = "s", ms = 8, label = "Infubinol")
plt.plot(timepoint, keta_perc, marker = "o", ms = 8, label = "Ketapril")
plt.plot(timepoint, plac_perc, marker = "x", ms = 8, label = "Placebo")
plt.plot(timepoint, rami_perc, marker = "^", ms = 8, label = "Ramicane")


#Add a legend, save the plot as a png file and then show the plot
plt.legend(loc="best")

# Save the Figure
plt.savefig('Survival_Rate.png') 

# Show the Figure
plt.show()


# ## Summary Bar Graph

# In[303]:


#Determine the amount and percent growth from beginning to end
by_timepoint_pivot


# In[304]:


capo_growth = round((by_timepoint_pivot.iloc[9,0] - by_timepoint_pivot.iloc[0,0]) *100 /  by_timepoint_pivot.iloc[0,0], 2)
infu_growth = round((by_timepoint_pivot.iloc[9,2] - by_timepoint_pivot.iloc[0,2]) *100 /  by_timepoint_pivot.iloc[0,2], 2)
keta_growth = round((by_timepoint_pivot.iloc[9,3] - by_timepoint_pivot.iloc[0,3]) *100 /  by_timepoint_pivot.iloc[0,3], 2)
plac_growth = round((by_timepoint_pivot.iloc[9,5] - by_timepoint_pivot.iloc[0,5]) *100 /  by_timepoint_pivot.iloc[0,5], 2)
rami_growth = round((by_timepoint_pivot.iloc[9,7] - by_timepoint_pivot.iloc[0,7]) *100 /  by_timepoint_pivot.iloc[0,7], 2)
tumor_changes = [capo_growth, infu_growth, keta_growth, plac_growth, rami_growth]
tumor_changes


# In[305]:


#Set horizontal axis for bar chart using drugs as x axis
horizontal_axis = ["Capomulin", "Infubinol", "Ketapril", "Placebo", "Ramicane"]
x_axis = np.arange(len(horizontal_axis))


# In[306]:


# Create a bar chart based upon the above data
fig, ax = plt.subplots() 
zero=0
above_zero = np.maximum(tumor_changes, zero)
below_zero = np.minimum(tumor_changes, zero)
ax.bar(x_axis, below_zero, 0.5, color="g", zorder=3)
ax.bar(x_axis, above_zero, 0.5, color="r", zorder=3)
    
plt.bar(x_axis, tumor_changes, color="b", align="center")
tick_locations = [value for value in x_axis]
plt.xticks(tick_locations, horizontal_axis)

      
#create title and labels
ax.set_title("Tumor Growth Over 45-Day Treatment Period")
ax.set_ylabel("% Tumor Volume Change")

#Label the value of each bar
labels = [str(capo_growth) + "%", str(infu_growth) + "%", str(keta_growth) + "%", 
                  str(plac_growth) + "%", str(rami_growth) + "%"]

# Set the limits of the y axis
plt.ylim(-25, max(tumor_changes)+ 10)

for rect, label in zip(rects, labels):
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width() / 2, height + .5, label,
            ha='center', va='bottom')

#create a horizontal line to designate "0"
ax.axhline(0, color='black')

#add grid
ax.grid(zorder=0)

# Save the Figure
plt.savefig('Tumor_Growth_bar_chart.png') 

# Show the Figure
plt.show()


# In[ ]:





# In[ ]:




