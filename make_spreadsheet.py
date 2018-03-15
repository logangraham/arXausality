import datetime
import unicodecsv as csv
from pull_update import fetch_papers


def get_paper_spreadsheet(past_n_days):
    num_papers = 100  # start by fetching 100 at a time, due to API constraints

    # set date filename & date constraints
    current_date = datetime.date.today()
    ymd = "_".join(map(str, [current_date.year,
                             current_date.month,
                             current_date.day]))
    filename = ymd + '_fetch.csv'

    # search, and construct entries
    print("Searching...\n\n")  # fetch results
    all_data = [["ID",
                "DATE",
                "TITLE",
                "AUTHOR",
                "CATEGORIES",
                "FIRST_CATEGORY ",
                "ABSTRACT",
                "ABS_LINK",
                "PDF_LINK"]]

    num_results, _ = fetch_papers(0, 5)  # find total number of papers
    for i in range(0, int(num_results) + 1, num_papers):  # iterate searches
        _, r = fetch_papers(i, num_papers)
        rows = filter(lambda x: (current_date - x[1]).days <= past_n_days, r)
        all_data += rows
        if len(rows) < len(r):
            break  # break if there are entries older than past_n_days
    print "Num papers: ", len(all_data)

    # write to a spreadsheet
    filename = '../weekly_pulls/' + filename
    with open(filename, "wb") as f:
        writer = csv.writer(f, dialect='excel', encoding='utf-8')
        writer.writerows(all_data)