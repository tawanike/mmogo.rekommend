import json
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer


class ContentBasedEngine:
    def __init__(self, content):
        self.df = pd.DataFrame(content)
        self.df['soup'] = self.df.apply(self.create_soup, axis=1)
        self.count = CountVectorizer(stop_words='english')
        self.count_matrix = self.count.fit_transform(self.df['soup'])

    def get_recommendations(self, item, sort_order):
        cosine_sim = cosine_similarity(self.count_matrix)
        indices = pd.Series(self.df.index, index=self.df['id'])

        idx = indices.get(item)
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=sort_order)
        sim_scores = sim_scores[1:20]
    
        item_indices = [i[0] for i in sim_scores]
        items = json.loads(pd.Series.to_json(self.df['id'].iloc[item_indices]))
         
        recommendations = [i for i in list(dict(items).values())]
        return recommendations


    def get_title(self, id):
        title = self.df[id]
        return title

    def create_soup(self, x):
        return str(x['price_range']) + ' ' + str(x['designer']) + ' ' + str(x['category']) + ' ' + str(x['silhouette']) + ' ' + str(x['style'])+ ' ' + str(x['dress_type']) + ' ' + str(x['fabric']) + ' ' + str(x['neckline']) + ' ' + str(x['tags']) + ' ' + str(x['colour'])
   
