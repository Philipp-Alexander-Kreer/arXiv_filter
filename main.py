import pandas as pd
import os
from datetime import date
import webbrowser


#Function which loads the eml file and returns the body of the email
def load_articles(file_path):
    """Loads an eml file and returns the body of the email. """
    with open(file_path, 'r') as f:


        # cut end of the email
        body = f.read().split('%%--%%--%%')[0] + "----\n\\\\"

        #cut header of the email
        body = body.split('\\\\\narXiv:')[1:]
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


def filter_title(title, remove_words):
    """Filters the title of the article and returns a label. """

    #Check if title contains remove_words
    if any(word in title.lower() for word in remove_words):
        return -1
    else:
        return 0




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

    #set the email directory and the browser
    email_directory = "/home/philipp/Downloads/"
    browser = webbrowser.get('firefox')
    #set auto_open to False if you want to open the new tab in the background
    auto_open = False

    # get email filenames and load them
    email_filenames = [email_directory + f for f in os.listdir(email_directory) if f.endswith(".eml")]
    print("The following emails will be loaded: ", email_filenames)

    articles = [[Article(article) for article in load_articles(email)] for email in email_filenames]
    #flatten articles
    articles = [item for sublist in articles for item in sublist]


    #convert articles into a pandas dataframe
    darticles = pd.DataFrame([vars(i) for i in articles])

    #filter duplicates based on arxiv id
    darticles = darticles.drop_duplicates(subset=['arxiv'])

    #filter replaced articles (indicated by replaced in the arxiv id)
    darticles = darticles[~darticles.arxiv.str.contains("replaced")]


    #load remove_words.txt
    with open("remove_words.txt", "r") as f:
        remove_words = [line.split(', ') for line in f.read().splitlines()]
        #flatten the list and lower the words

        remove_words = [word.lower() for sublist in remove_words for word in sublist]

    #filter articles based on title
    darticles.loc[darticles['label'] == 'NA', 'label'] = darticles[darticles['label'] == 'NA'].title.apply(lambda x: filter_title(x, remove_words))

    # loop over darticles with label 1
    for i in darticles[darticles['label'] == 0].index:
        #print the title
        print("\n\n",darticles.loc[i, 'title'])
        #print("\n\n", darticles.loc[i, ['arxiv','link']])

        # ask the user if the abstract should be opened
        user_input = input("\nDo you want to open the abstract? (y/n) ")

        if user_input == 'y':
            print("\n")
            darticles.loc[i, 'label'] = 1

            #print the abstract
            #print(darticles.loc[i, 'abstract'])
            long_string = darticles.loc[i, 'abstract']

            #Find postions of empty spaces in the string

            chunk_size = 15  # Adjust as needed
            empty_space_positions = [i for i, ltr in enumerate(long_string) if ltr == ' '][0::chunk_size]


            for line_break in range(len(empty_space_positions)):
                if line_break == len(empty_space_positions)-1:
                    print(long_string[empty_space_positions[line_break]:])
                else:
                    print(long_string[empty_space_positions[line_break]:empty_space_positions[line_break+1]])



            #ask the user if the link should be opened
            user_input = input("\nDo you want to open the article? (y/n) ")
            if user_input == 'y':

                darticles.loc[i, 'label'] = 2
                link = darticles.loc[i, 'link']
                # open the link new=2 opens the link in a new tab
                browser.open(link, new=2, autoraise=auto_open)



    #save the dataframe to a csv file with the current date

    today = date.today()
    darticles.to_csv("Data/articles_"+str(today)+".csv", index=False)

    #print statistics
    print("\n\n\n\n Statistics: \n\n")
    print("You filtered ", len(darticles[darticles['label'] == -1]), "of", len(darticles), "articles.")
    print("You opened ", len(darticles[darticles['label'] == 1]), "of", len(darticles), "abstracts.")
    print("You opened ", len(darticles[darticles['label'] == 2]), "of", len(darticles), "articles.")

    #delete the emails if the user wants to
    user_input = input("Do you want to delete the emails? (y/n) ")
    if user_input == 'y':
        for email in email_filenames:
            os.remove(email)
        print("Emails deleted.")
    print("Have a nice day and thank you for using the arXiv filter :-)")













    

