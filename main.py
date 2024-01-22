
import os

#Function which loads the eml file and returns the body of the email
def load_articles(file_path):
    """Loads an eml file and returns the body of the email. """
    with open(file_path, 'r') as f:

        body = f.read().split('arXiv:')[1:]
        body = ['arXiv:' + i for i in body]

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

    article_cut = article.replace('\n', ' ')



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




if __name__ == '__main__':

    test = load_articles("test_mail.eml")
    #print(test[0].split('\n')[6:])
    test = extract_article_info(test[9])

    for i in test:
        print(i, test[i])

