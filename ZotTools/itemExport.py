from . import myZotTools 
import dateutil.parser
import re

def parse_date(date):
    return dateutil.parser.parse(date)


class ItemExporter:

    def __init__(self):
        pass

    def export(self, item_data):
        """

        Args:
            item_data (dictionary): item['data'] from pyzotero
        returns:
            string: exported_string
        """

        template = \
"""
<reference>
    <title>
        {all_authors} 
        "{title}," {year}.
    </title>
    <url>
        {url}
    </url>
</reference>
"""
        all_authors = self.format_all_authors(item_data['creators'])
        title = item_data['title']
        date =  parse_date( item_data['date'])
        year = date.year
        url = item_data['url']
        formated = template.format(all_authors=all_authors, title=title, year=year, url=url)
        return formated




    def format_individual_author(self, author):
        return "{}. {}".format(author['firstName'].upper()[0], author['lastName'])
        
    def format_all_authors(self, list_of_authors):
        formated_authors = list([self.format_individual_author(a) for a in list_of_authors])
        if len(formated_authors)==1:
            return formated_authors[0]
        else:
            first_half = formated_authors[:-1]
            last_one = formated_authors[1]

            return "{}, and {}".format(", ".join(first_half), last_one)



def export_items_for_website(list_of_items):
    exporter = ItemExporter()
    return "\n\n".join([exporter.export(item['data']) for item in list_of_items])


def get_number_forsorting(item):
    extra_info = item['data']['extra']

    pattern = r'q(\d{1,2})(?!\d)'

    match = re.search(pattern, extra_info)
    if match:
        extracted_number_str = match.group(1)
        extracted_number = int(extracted_number_str)
        return extracted_number
    else:
        return 999

def sort_items_by_qKey(items):
    return sorted(items, key=get_number_forsorting)

def export_items_by_tag_for_website(tag):
    """
    
    to sort the list we try to find patterns of the form q1, q33, q44 in the extra field, and sort by increasing number. if not such pattern is found it goes to the end of the list

    Args:
        tag (_type_): _description_

    Returns:
        _type_: _description_
    """
    items = myZotTools.get_items_by_tag(tag)

    sorted_items = sort_items_by_qKey(items)

    full_string = export_items_for_website(sorted_items)
    return full_string