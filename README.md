# 10th Circuit Court Capstone
## Description
This project focuses on developing a model that can quickly identify related court cases. In many court cases, each side constructs an argument citing previous cases as precedent to support their claim. However, there are a huge number of cases just in the 10th circuit alone. The goal of this project is to go beyond a standard key word search using Natural Language Processing and Non-negative matrix factorizations to find similar cases.

### Database
* All cases from 2000 and 2001 in the 10th Circuit U.S. Court of Appeals
* Case data is retrieved from http://law.justia.com/
* __MongoDB__ database stores data pulled from each case

### Model
#### Data manipulation
* Each case in the database is cleaned to remove punctuation, standard stop words and words commonly used in court cases. (e.g. court, defendant, jury, trial, etc.)
* __spaCy__ is used to process the cleaned case text
* Split the data
    * Use the cases from 2000 as the training set
    * Use the cases from 2001 as the testing set
* Cases were then saved in a _pickle file_ to form the corpus

![Alt text](/images/casedata1.png)

#### Cosine Similarities and tf-idf
* __Tf-idf__ is used to vectorize each case in the corpus according to the terms present in the entire corpus
* With each case having an associated vector, the angle between two cases is found
* Related cases can then be determined using cosine similarities

#### NMF
![Alt text](/images/nmf1.png)

* __NMF__ allowed for the data to be clustered without explicitly labeling each case topic
* A set of top words within each topic is generated to allow for a subset of the data to be searched
![Alt text](/images/casetopwords1.png)

* With the size of the database too many topics resulted in only a handful of cases per topic (Similarities between topics and test case were extremely small)
* While with too few the topics became _catch all topics_ (very broad, same terms appeared in the majority of documents)
* The number of allowed topics is set to 15, which allows for a reasonable number of topics while still keeping the topics unique from one another

#### Model Testing
* The model randomly selects a case from 2001 to test
* The model searches for similar cases in the corpus in two steps
* First it finds the cosine similarity between the test case and the set of top words for each topic
![Alt text](/images/casecorpus1.png)

* Second it finds the cosine similarity between the test case and all cases within the topic it was most similar to
![Alt text](/images/casetopic1.png)

* This is to prevent the model from calculating a similarity between the test case and all cases in the corpus
