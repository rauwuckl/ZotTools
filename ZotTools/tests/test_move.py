import unittest

import ZotTools.myZotTools as myZotTools

class TestZoteroTools(unittest.TestCase):

    def stest_download_pdf(self):
        folder_path = "."
        item_title = 'Convergence of Redundancy-Free Spiking Neural Networks to Rate Networks'
        pdf_path = myZotTools.download_pdf_item(item_title, folder_path)


    def skiped_test_get_main_pdf_key_for_item(self):
        item_key = '9Z8AQK6V'
        pdfItem = myZotTools.get_main_pdf_items_for_parentitem(item_key)
        ano_path = myZotTools.download_pdf_item(pdfItem, '.')

        result = myZotTools.attach_pdf_to_parent_as_link(item_key, ano_path)

        print(pdfItem)


    def test_pdfKey_with_linked(self):
        name = 'The Tensor Product of Frames'
        item = myZotTools.get_items_by_title(name)

        pdfItem = myZotTools.get_main_pdf_items_for_parentitem(item['key'])


    def test_get_items_by_tag(self):
        items = myZotTools.get_items_by_tag('transformer2big')

        print(items)

    def test_utils(self):
        pass