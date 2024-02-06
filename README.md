# arXiv filter

As a scientist, it's crucial to stay updated on the latest developments in your field. Experts often use even small advancements to progress their own projects. The arXiv is a perfect platform for this exchange of information.

You can also subscribe to a daily newsletter that provides the newest submissions in your chosen genre, like high-energy physics - theory (hep-th). This newsletter includes titles, authors, abstracts, and more. Checking it regularly can offer valuable insights and open up new research directions.

However, the sheer volume of daily submissions, even in narrower subfields, can quickly become overwhelming. Additionally, subscribing to multiple subfields may result in duplicate articles appearing in both newsletters. This can lead to difficulties in keeping track of everything and may result in overlooking important papers. 

This is where the arXiv filter comes into play. It sorts through the received emails, eliminating duplicates and replacements. Additionally, users can set specific keywords to exclude from titles. 
This allows for openness to new ideas (since it's impossible to filter out ideas never encountered) while reducing daily information overload. Consequently, more time is available for actually reading papers.

## Usage

The operation of the arXiv filter is straightforward:

 1. Subscribe to the relevant arXiv newsletter [here](https://info.arxiv.org/help/subscribe.html).
 2. Download and save the email in a directory of your choice (e.g., Downloads).
 3. Install the arXiv filter (see below)
 4. Start the arXiv filter.

Titles are then presented sequentially to you. If a title catches your interest, you can open the abstract in the same screen to read it. If the abstract is intriguing, you can directly open the PDF in the browser, or proceed to the next title if not.

## Installation

```
git pull (this directory)
```

```
cd arXiv_filter/
```

in the same directory. Then, open the settings.config file in your editor and specify the browser, and the email directory. Save the file.

If you made sure that the follwing standard python packages are available:

1. pandas
2. webbrowser
3. os
4. datetime
 
run 

```
python main.py
```

Enjoy reading the papers and wait till the end :) 


## Notes

I'm currently developing an improved version of the arXiv filter, leveraging GPT-4 technology. In this version, articles and corresponding user actions are saved locally in a .csv file for each day. The goal is to enable training of the AI backend directly on personalized labeled data.

If storage is undesired, you have the option to disable this feature in the settings file.
