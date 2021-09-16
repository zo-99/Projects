#!/usr/bin/env python
# coding: utf-8

# # Capstone 2: Biodiversity Project
# By: Zorawar Singh Dhanoa

# # Introduction
# I take the role of a biodiversity analyst working for the National Parks Service. I am going to help them analyze some data about species at various national parks.
# 
# Note: The data that you'll be working with for this project is *inspired* by real data, but is mostly fictional.

# In[2]:


from matplotlib import pyplot as plt 
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency


# In[3]:


species = pd.read_csv('species_info.csv')
species.head()


# # Step 1
# Let's start by learning a bit more about our data. Below are a set of questions that are important to understand going forward as they assist in understanding the data better

# How many different species are in the `species` DataFrame?

# In[4]:


unique_species = species.scientific_name.nunique()
unique_species


# What are the different values of `category` in `species`?

# In[5]:


diff_category = species.category.unique()
diff_category


# What are the different values of `conservation_status`?

# In[6]:


special_coserve_status = species.conservation_status.unique()
special_coserve_status


# # Step 2
# This section focuses on the analysis!
# 
# The column `conservation_status` has several possible values:
# - `Species of Concern`: declining or appear to be in need of conservation
# - `Threatened`: vulnerable to endangerment in the near future
# - `Endangered`: seriously at risk of extinction
# - `In Recovery`: formerly `Endangered`, but currnetly neither in danger of extinction throughout all or a significant portion of its range
# 
# We'd like to count up how many species meet each of these criteria.  Use `groupby` to count how many `scientific_name` meet each of these criteria.

# In[7]:


species.fillna('No Intervention', inplace=True)
grouped_conservation_status = species.groupby('conservation_status').scientific_name.nunique().reset_index()
grouped_conservation_status.head()


# In[8]:


#This segregates the data into the relevant sections, helping us understand the troubling nature of the species

protection_counts = species.groupby('conservation_status').scientific_name.nunique().reset_index().sort_values(by='scientific_name')
protection_counts


# In[9]:


plt.figure(figsize=(10,4))
ax = plt.subplot()
plt.bar(range(len(protection_counts)), protection_counts.scientific_name)
ax.set_xticks(range(len(protection_counts)))
ax.set_xticklabels(protection_counts.conservation_status)
plt.ylabel('Number of Species')
plt.title('Conservation Status by Species')
plt.show()


# # Step 3
# This section aims to find species that need immediate assitance

# The new column helps us visualise which species are protected and which species are not. This will be used to help us perform analysis and effective grouping of the data

# In[10]:


species['is_protected'] = species.conservation_status.apply(lambda x: True if x =='No Intervention' else False)
species.head(15)


# Let's group the `species` data frame by the `category` and `is_protected` columns and count the unique `scientific_name`s in each grouping.
# 

# In[11]:


category_counts = species.groupby(['category','is_protected']).scientific_name.nunique().reset_index()
category_counts


# A pivot Table helps us better understand the nature of the data, and to help is statistical anylysis. 

# In[12]:


category_pivot = category_counts.pivot(columns='is_protected', index='category', values='scientific_name').reset_index()
category_pivot.columns = ['category', 'protected', 'not_protected']
category_pivot['percent_protected'] = category_pivot.protected/(category_pivot.protected + category_pivot.not_protected)*100
category_pivot


# In[13]:


#This helps us compare the difference between the Mammal species and Bird species, however after the test we can conclude that the tests are not statistically significant
contingency = [[30,146], [75,413]]
sig_test = chi2_contingency(contingency)
sig_test


# In[14]:


#This is a similar test comparing the Reptile and Mammal species. However, here we can confidently conclude that there is a significant differnce between the two species
contingency1 = [[30,146], [5,73]]
sig_test1 = chi2_contingency(contingency1)
sig_test1


# # Step 4

# Conservationists have been recording sightings of different species at several national parks for the past 7 days.  the data is saved in a file called `observations.csv`.  

# In[15]:


observations = pd.read_csv('observations.csv')
observations.head()


# Some scientists are studying the number of sheep sightings at different national parks.  There are several different scientific names for different types of sheep.  This shows which rows of `species` are referring to sheep.  

# In[16]:


species['is_sheep'] = species.common_names.apply(lambda x: True if 'Sheep' in x else False)
sheep_species = species[(species.is_sheep == True) & (species.category == 'Mammal')]
sheep_species


# In[17]:


sheep_observations = observations.merge(sheep_species)
sheep_observations


# In[18]:


obs_by_park = sheep_observations.groupby('park_name').observations.sum().reset_index()
obs_by_park


# In[19]:


plt.figure(figsize=(16,4))
ax = plt.subplot()
plt.bar(range(len(obs_by_park.observations)), obs_by_park.observations.values)
ax.set_xticks(range(len(obs_by_park.observations)))
ax.set_xticklabels(obs_by_park.park_name)
plt.ylabel('Number of Observations')
plt.title('Observations of Sheep per Week')

plt.show()

