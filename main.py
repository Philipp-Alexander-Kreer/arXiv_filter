import pandas as pd
import os

#Function which loads the eml file and returns the body of the email
def load_articles(file_path):
    """Loads an eml file and returns the body of the email. """
    with open(file_path, 'r') as f:

        body = f.read().split('arXiv:')[1:]
        body = ['arXiv:' + i for i in body]

        #remove the last part of the body which is not an article and add the end of the article
        body[-1] = body[-1].split('%%%---%%%')[0] + "----\n\\\\"

        return body

def extract_article_info(article):
    """Extracts the article info  and returns a dictionary with the info. """

    article_info = {}

    #categories to extract (possible categories) + in order
    categories = ['arXiv:','Date:','Title:','Authors:','Categories:','Comments:','Report-no:','Journal-ref:','DOI:','\\\\']

    #keep only categories which are in article
    filtered_categories = [category for category in categories if category in article]

    #Put NA for categories which are not in article
    complement_categories = [category.replace(':','').lower() for category in categories if category not in article]

    for i in complement_categories:
        article_info[i] = 'NA'

    # the labels are : -1 = filtered, 0 = ignored, 1 = opened abstract, 2 = opened link
    article_info['label'] = 'NA'

    article_cut = article.replace('\n', ' ').replace('(*cross-listing*)', '')



    #split categories in article and put them in a dictionary
    for i in range(len(filtered_categories)-1):

        article_cut = article_cut.split(filtered_categories[i+1])
        idname = filtered_categories[i].replace(':','').lower()
        article_info[idname] = article_cut[0].replace('  ',' ')

        #if last category, add abstract and link
        if i == len(filtered_categories)-2:
            article_info['abstract'] = article_cut[1]
            article_info['link'] = article_cut[2].split(',')[0].replace('(', "").replace(' ', "")

        article_cut = article_cut[1]


    return article_info


class Article:
    def __init__(self, article):

        # if article is a string, extract the info
        article_info = extract_article_info(article)

        self.arxiv = article_info['arxiv']
        self.date = article_info['date']
        self.title = article_info['title']
        self.authors = article_info['authors']
        self.categories = article_info['categories']
        self.comments = article_info['comments']
        self.report_no = article_info['report-no']
        self.journal_ref = article_info['journal-ref']
        self.doi = article_info['doi']
        self.abstract = article_info['abstract']
        self.link = article_info['link']
        self.label = article_info['label']


if __name__ == '__main__':

    articles = [Article(i) for i in load_articles("test_mail.eml")]

    #convert articles into a pandas dataframe
    darticles = pd.DataFrame([vars(i) for i in articles])

    #filter duplicates based on arxiv id
    darticles = darticles.drop_duplicates(subset=['arxiv'])

    #filter replaced articles (indicated by replaced in the arxiv id)
    darticles = darticles[~darticles.arxiv.str.contains("replaced")]

    #print darticles date
    print(darticles.arxiv)








    

