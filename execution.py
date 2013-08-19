import sys
import json
from math import sqrt
import random



# Load input JSON file containing Twitter friends entries.  
input = open(sys.argv[1])
lines = []
for line in input:
    data = json.loads(line)
    for x in data:
       if (x['following']):
           follow = 1
       else:
           follow = 0
       description = str(x['description']).split()          
       description_length = len(description)                #length of twitter bio
       apple = [x['name'], x['followers_count'], x['statuses_count'],x['friends_count'], x['favourites_count'], follow, description_length]
       lines.append(apple)


#Create friend-vectors and friend-vector-names
vecnames = []
vectors = []
for line in lines:
    vecnames.append(line[0])
    vectors.append(line[1:])
    



#Notion of distance, we'll user Pearson Correlation. Other more sophisticated methods are possible.
#Read Wikipedia entry on Pearson score for definition and more information. 
def pearson(v1,v2):
  sum1=sum(v1)
  sum2=sum(v2)
  
  # Sums of the squares
  sum1Sq=sum([pow(v,2) for v in v1])
  sum2Sq=sum([pow(v,2) for v in v2])	
  
  # Sum of the products
  pSum=sum([v1[i]*v2[i] for i in range(len(v1))])
  
  # Calculate r (Pearson correlation)
  n=pSum-(sum1*sum2/len(v1))
  d=sqrt((sum1Sq-pow(sum1,2)/len(v1))*(sum2Sq-pow(sum2,2)/len(v1)))
  if d==0: return 0

  return 1.0-n/d




#Clustering
#Read Wikidepia entry on clustering or k-means for more information

def clustering(vectors,distance=pearson,k):
    
  # Determine the minimum and maximum values for each point

  ranges=[(min([vector[i] for vector in vectors]),max([vector[i] for vector in vectors])) 
  for i in range(len(vectors[0]))]

  #Place k centroids randomly. 

  clusters=[[random.random()*(ranges[i][1]-ranges[i][0])+ranges[i][0] 
  for i in range(len(vectors[0]))] for j in range(k)]
  
  lastmatches=None
  for t in range(100):
    bestmatches=[[] for i in range(k)]
    
    # Find closest centroid for each vector

    for j in range(len(vectors)):
      vector=vectors[j]
      bestmatch=0
      for i in range(k):
        d=distance(clusters[i],vector)
        if d<distance(clusters[bestmatch],vector): bestmatch=i
      bestmatches[bestmatch].append(j)

    # If the results are the same as last time, this is complete

    if bestmatches==lastmatches: break
    lastmatches=bestmatches
    
    # Move the centroids to the average location of their members

    for i in range(k):
      avgs=[0.0]*len(vectors[0])
      if len(bestmatches[i])>0:
        for rowid in bestmatches[i]:
          for m in range(len(vectors[rowid])):
            avgs[m]+=vectors[rowid][m]
        for j in range(len(avgs)):
          avgs[j]/=len(bestmatches[i])
        clusters[i]=avgs
      
  return bestmatches


#Print 5 Clusters of my Twitter friends
clust = clustering(vectors, k=5)
for i in range(len(clust)):
    print [vecnames[t] for t in clust[i]]








