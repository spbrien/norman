# -*- coding: utf-8 -*-

import click
from quick import *

@click.command()
@click.argument('filename')
def main(filename):
    """Utility script for working with emails"""
    soup = get_soup(filename)
    styled = insert_styles(soup)
    centered = center_email(styled)
    no_cols = remove_colspans(centered)
    no_heights = strip_heights(no_cols)
    fix_images = image_styles(no_heights)
    inline_email(filename, fix_images)


if __name__ == "__main__":
    main()
