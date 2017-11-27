import pandas as pd
import glob
import os
import io
import pytablewriter
from datetime import date


def add_to_markdown_README(paper_table_filepath):
    df = pd.read_csv(paper_table_filepath)
    df = df[['DATE', 'TITLE', 'AUTHOR', 'ABS_LINK', 'PDF_LINK']]
    df.ABS_LINK = df.ABS_LINK.apply(lambda x: '[Abstract]({})'.format(x))
    df.PDF_LINK = df.PDF_LINK.apply(lambda x: '[PDF]({})'.format(x))
    df['Links'] = df.ABS_LINK + ' | ' + df.PDF_LINK
    df = df.drop(['ABS_LINK', 'PDF_LINK'], axis=1)
    df.columns = ['Date', 'Title', 'First Author', 'Links']
    writer = pytablewriter.MarkdownTableWriter()
    writer.stream = io.StringIO()
    writer.header_list = list(df.columns)
    writer.value_matrix = df.values
    writer.write_table()
    writer.stream.seek(0)
    markdown = "".join(writer.stream.readlines()).encode('utf8')

    current_date = date.today()
    ymd = " / ".join(map(str, [current_date.year,
                               current_date.month,
                               current_date.day]))

    final_string = "## {}\n\n".format(ymd) + markdown

    with open("README.md", 'r+') as f:
        content = f.read()
        if ymd not in content[:20]:
            f.seek(0, 0)
            f.write(final_string + '\n\n' + content)
        else:
            print "Already put table from this week."

if __name__ == '__main__':
    list_of_files = glob.glob('../weekly_pulls/*') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    filepath = '../weekly_pulls/{}'.format(latest_file)
    add_to_markdown_README(filepath)