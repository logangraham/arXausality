import urllib
import feedparser
import unicodecsv as csv
import datetime
import sys


def fetch_papers(start, max_results=10, only_recent=True):

    # Base api query url
    base_url = 'http://export.arxiv.org/api/query?'

    # Search parameters
    def list_to_OR_params(l, prefix, quotations=False):
        """
        This formats lists of strings to '(prefix:string1)+OR+(prefix:string2)...'
        quotations=True puts quotations: '(prefix:"string1")+OR+(prefix:"string2")...'
        """
        if quotations:
            l = map(lambda x: '"%s"' % x, l)
        l = map(lambda x: '({}:'.format(prefix) + '+'.join(x.split()) + ')', l)
        return "+OR+".join(l)

    general_terms = [
                     'causation',
                     'interven',
                     # 'cause',
                     'causal',
                     # 'causes'
                    ]
    general_abs = list_to_OR_params(general_terms, 'abs', quotations=False)
    general_ti = list_to_OR_params(general_terms, 'ti', quotations=False)

    specific_terms = ['do-calculus',
                      'do calculus',
                      'structural equation',
                      'instrumental variable',
                      'treatment effect',
                      'counterfactual',
                      'hidden variable',
                      'structure identif',
                      'faithfulness',
                      'conditional independenc'
                     ]
    specific_abs = list_to_OR_params(specific_terms, 'abs', quotations=True)
    specific_ti = list_to_OR_params(specific_terms, 'ti', quotations=True)

    category_list = ['cs.CV',
                     'cs.AI',
                     'cs.LG',
                     'cs.CL',
                     'cs.NE',
                     'stat.ML'
                    ]
    categories = list_to_OR_params(category_list, 'cat')

    search_query = '(%s)+AND+(%s+OR+%s+OR+%s+OR+%s)' % (categories,
                                                        general_abs,
                                                        general_ti,
                                                        specific_abs,
                                                        specific_ti)

    query = 'search_query=%s&start=%i&max_results=%i' % (search_query,
                                                         start,
                                                         max_results)

    if only_recent:
        suffix = "&sortBy=submittedDate&sortOrder=descending"
        query += suffix

    full_url = base_url + query
    print(full_url)

    feedparser._FeedParserMixin.namespaces['http://a9.com/-/spec/opensearch/1.1/'] = 'opensearch'
    feedparser._FeedParserMixin.namespaces['http://arxiv.org/schemas/atom'] = 'arxiv'

    response = urllib.urlopen(base_url+query).read()

    feed = feedparser.parse(response)

    print('Feed title: %s' % feed.feed.title)
    print('Feed last updated: %s' % feed.feed.updated)

    print('totalResults for this query: %s' % feed.feed.opensearch_totalresults)
    print('itemsPerPage for this query: %s' % feed.feed.opensearch_itemsperpage)
    print('startIndex for this query: %s'   % feed.feed.opensearch_startindex)

    rows = []
    for entry in feed.entries:  # extract information & add to list
        entry_id = entry.id.split('/abs/')[-1]
        date = datetime.datetime.strptime(str(entry.published)[:10], '%Y-%m-%d').date()
        title = entry.title
        first_author = entry.author
        all_categories = ", ".join([t['term'] for t in entry.tags])
        primary_category = entry.tags[0]['term']
        abstract = entry.summary
        for link in entry.links:
            if link.rel == 'alternate':
                abs_link = link.href
            elif link.title == 'pdf':
                pdf_link = link.href
        row = [entry_id,
               date,
               title,
               first_author,
               all_categories,
               primary_category,
               abstract,
               abs_link,
               pdf_link]
        rows.append(row)
    return feed.feed.opensearch_totalresults, rows

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

if __name__ == "__main__":
    arguments = sys.argv
    if len(arguments) == 1:
        get_paper_spreadsheet(7)  # default to past seven days
    else:
        get_paper_spreadsheet(int(arguments[1]))  # otherwise use custom flag