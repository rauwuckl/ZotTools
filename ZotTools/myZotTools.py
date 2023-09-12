import os
import shutil
from pyzotero import zotero
import copy
from . import utils
import difflib


data = utils.get_credentials()
zot = zotero.Zotero(data['library_id'], data['library_type'], data['api_key'])


def get_items_by_tag(tag):
    all_tags = zot.tags()

    if tag not in all_tags:

        sorted_tags = sorted(all_tags, key=lambda x: difflib.SequenceMatcher(None, x, tag).ratio(), reverse=True)
        raise ValueError(f"Tag '{tag}' is not in the library, did you mean one of {sorted_tags[:8]}")
    
    items = zot.top(tag=tag)

    return items


def get_main_pdf_items_for_parentitem(item_key):
    children = zot.children(item_key)
    hit = None
    for c in children:
        item_type  = c['data']['itemType']
        if item_type == 'attachment':
            file_type = c['data']['contentType']
            if file_type == 'application/pdf' and c['data']['linkMode'] != "linked_file":
                if hit is None:
                    hit = c
                else:
                    raise ValueError('At least 2 attachements: {} and {}'.format(hit, c['key']))
    return hit

def get_items_by_title(item_title, return_more=False):
    items = zot.top(q=item_title) # todo whould probably uses zot.top() for toplevel items
    hits = list()
    for i in items:
        if not 'parentItem' in i['data']:
            hits.append(i)

    if len(hits)> 1:
        if return_more:
            return hits
        else:
            raise ValueError('Multiple hits: {}'.format(hits))
    else:
        return hits[0]

_rename_template = "ano_{}"
def download_pdf_item(pdf_item, folder_path):
    pdf_title = pdf_item['data']['title']
    new_pdf_title = _rename_template.format(pdf_title)
    pdf_key  = pdf_item['key']
    pdf_path_returned = zot.dump(pdf_key, new_pdf_title, folder_path)
    pdf_path = os.path.join(folder_path, new_pdf_title)
    return pdf_path



# optained by zot.item_template('attachment', 'linked_file')
linked_file_template = {'itemType': 'attachment', 
 'linkMode': 'linked_file', 
 'title': '', 'accessDate': '', 
 'note': '', 'tags': [], 'collections': [], 'relations': {}, 'contentType': 'application/pdf', 'charset': '', 'path': ''}


def attach_pdf_to_parent_as_link(parentKey, file_path):
    link_type = 'linked_file'
    item_type = 'attachment'

    template = copy.deepcopy(linked_file_template)

    template['path'] = file_path
    template['title'] = file_path.split("/")[-1]

    result = zot.check_items([template])

    result_of_create = zot.create_items(result, parentid=parentKey)
    return result


