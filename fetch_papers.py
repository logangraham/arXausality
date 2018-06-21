import urllib
import feedparser
import datetime


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
    print full_url

    feedparser._FeedParserMixin.namespaces['http://a9.com/-/spec/opensearch/1.1/'] = 'opensearch'
    feedparser._FeedParserMixin.namespaces['http://arxiv.org/schemas/atom'] = 'arxiv'

    response = urllib.urlopen(base_url+query).read()

    feed = feedparser.parse(response)

    print 'Feed title: %s' % feed.feed.title
    print 'Feed last updated: %s' % feed.feed.updated

    print 'totalResults for this query: %s' % feed.feed.opensearch_totalresults
    print 'itemsPerPage for this query: %s' % feed.feed.opensearch_itemsperpage
    print 'startIndex for this query: %s'   % feed.feed.opensearch_startindex

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