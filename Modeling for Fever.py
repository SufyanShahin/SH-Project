# In[1]:
# Needed imports
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

features = pd.read_csv('path\\First Dance.csv', low_memory=False).drop(columns=['Unnamed: 0'])
features.info()

# In[2]:
### Finding songs most closely associated with the feel and rhythm of 
### Fever by Michael Buble for my fiance

# Keeping features related to the feel and rhythm of a song
# danceability, energy, loudness, valence, tempo, key, mode, time_signature
attributes = ['danceability','energy','loudness','valence','tempo']

# Subsetting based on these attributes and standardizing the attributes
features_fv = features[attributes]
features_fv = StandardScaler().fit_transform(features_fv)

# In[3]:
# Running a DBSCAN to identify song clusters
# Reference: https://towardsdatascience.com/dbscan-algorithm-complete-guide-and-application-with-python-scikit-learn-d690cbae4c5d
# Manually adjusted eps to get 5-15 songs that cluster with target (last observation)
db = DBSCAN(eps=1.003, min_samples = 5).fit(features_fv)
labels = db.labels_
labels

# In[4]:
# Adding the group column based on these labels
features['group'] = labels

# Filtering down to just songs grouped with Fever
songs = features[features.group == int(features.group[features.name == features.name[len(features)-1]])]

# That also have the same time_signature
songs = songs[features.time_signature == int(features.time_signature[features.name == features.name[len(features)-1]])]

# In[5]:
# 14 songs are clustered with Fever
songs.info()
songs.reset_index(drop=True,inplace=True)

# Printing those songs
for song in range(0, len(songs)-1):
    print(songs.name[song] + ' by ' + songs.artist[song])


