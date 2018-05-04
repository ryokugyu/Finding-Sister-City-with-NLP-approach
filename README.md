Sister City project with NLP approach

Sister Cities Policy defines sister city as a form of legal or social agreement between towns, cities, counties,prefectures, provinces, regions, states and even countries on geographically and politically distinct areas to promote cultural and commercial ties.To quantitatively compare two cities, we define sister cities as cities are similar in user-specifed criteria. There are two ways to define criteria. The criteria could be the categories usually used to describe a city, such as demographics and economy. Input keywords could also be used to compare cities, such as "best coffee",to have broader criteria.To limit scope, we only involve cities in US. I found the intersection of city lists from various source to have the complete data for each city. The final list contains 15718 cities.To decrease the complexity of the unstructured analytics phase, for each input city, we return top 5 sister cities the most similar. We choose 5 categories as default putting in the database. Each category has multiple variables to measure the similarity. For example, we measure the median and mean income in economy, population and marital status in demographics. However, user could input arbitrary keywords to the system for ranking, which increases the complexity.The default five categories are climate, demographics, economy, political views and proximity. Each category is a dimension used to compare similarities. A user could assign weight to each category to evaluate sister cities according to the user's preference. And then we rank sister cities according to the relevance to the input keywords.


Structured approach

The first step of the analysis is the comparison of the structured data for each city. Given an input city, we wanted to find the city with the most similar metrics to that city.Because we had so many distinct criteria, and we were trying to find a similar solution rather than an optimal one,we elected to use KNN rather than TOPSIS or some other multi-criteria decision making algorithm. KNN allows us to compare the similarity of cities across each input dimension rather than projecting the data onto a lower dimensionality before making the comparison. Thus, it is easier to determine how our decisions are made in this phase of the analysis because each field in the output cities can be manually inspected.To prepare our data for KNN, we had to normalize each dimension so that it could be compared on the same scale without unintentional weight differences. Normalization was performed with a simple min-max formula which rescales the data to the range [0,1], where 0 is the value once held by the minimum in that column and 1 is the value once held by the maximum of the column


Unstructured Approach

First step was getting news articles for unstructured text analysis. So for a provided query input and list of cities determined in previous step, our script searched Google news for those querywords and after scraping those URLs from Google news page, crawled those URLs to get five relevant news articles for every city. Now after getting those articles we did need to analyze those news articles and determine its relevance to the query words. So we performed Ranking and scoring news articles using Dual Embedding Space-Model So i followed the algorithm proposed in the paper as follows:
 We trained a Word2Vec embedding model on a corpus
of 1,50,000 news articles while retaining both the input
and the output projections,allowing us to leverage both
the embedding spaces to derive richer distributional
relationships.
 During ranking we mapped the query words into the
input space and the document words into the output
space,and computed a query-document relevance score
by aggregating the cosine similarities across all the
query-document word pairs.
 A novel Dual Embedding Space Model, with one em-
bedding for query words and a separate embedding for
document words.
 Document ranking feature based on comparing all the
query words with all the document words, which is
equivalent to comparing each query word to a centroid
of the document word embeddings.
Embeddings-based approach is prone to false positives,
retrieving documents that are only loosely related to
the query. But we had solved this problem effectively
by ranking based on a linear mixture of the DESM(Dual
embedding space model) and the word counting fea-
tures
