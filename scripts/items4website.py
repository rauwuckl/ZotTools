from ZotTools import itemExport
import os.path


if __name__ == "__main__":

    tag = input("Tag to export:")
    default_filepath = f"Downloads/{tag}.txt"
    full_string = itemExport.export_items_by_tag_for_website(tag)
    
    output_filepath = input(f"Output filepath (or enter for {default_filepath}):")
    if output_filepath=="":
        print(f'using default: ~/{default_filepath}')
        output_filepath = os.path.join(os.path.expanduser('~'), default_filepath)



    with open(output_filepath, 'w') as file:
        file.write(full_string)
