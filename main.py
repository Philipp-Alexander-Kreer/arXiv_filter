from datetime import date
import webbrowser
import arXiv_filter
import pandas as pd


def arXiv_filter_main():
    # load the settings
    email_directory, browser, auto_open = arXiv_filter.load_settings()

    darticles = arXiv_filter.prepare_dataframe(email_directory)

    # loop over darticles with label 1
    for i in darticles[darticles['label'] == 0].index:
        # print the title
        print("\n\n", darticles.loc[i, 'title'])

        # ask the user if the abstract should be opened
        user_input = input("\nDo you want to open the abstract? (y/n) ")

        if user_input == 'y':
            print("\n")
            arXiv_filter.print_abstract(darticles.loc[i, 'abstract'])

            # ask the user if the link should be opened
            darticles.loc[i, 'label'] = arXiv_filter.open_link(darticles.loc[i, 'link'], browser, auto_open)

    # save the dataframe to a csv file with the current date

    today = date.today()
    darticles.to_csv("Data/articles_" + str(today) + ".csv", index=False)

    arXiv_filter.print_statistics(darticles)

    # delete the emails if the user wants to
    arXiv_filter.delete_emails(email_directory)
    print("Have a nice day and thank you for using the arXiv filter :-)")

if __name__ == '__main__':
    arXiv_filter_main()















    

