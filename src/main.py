# module main

import os
import json
import math

from rich import box
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich import print as rprint
from rich.prompt import Prompt, Confirm

from book import Book
from library import Library
from export import json_to_csv

DEFAULT_FILE_PATH: str = '../data/library.json'

def clear_screen() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

def prompt_add(library: Library) -> None:
    status: str | None = None

    while True:
        print('Add mode. Press [q] to exit.')

        if status:
            print(f'STATUS: {status}')

        title: str = Prompt.ask('Title')

        if title.lower() == 'q':
            break

        author: str = Prompt.ask('Author')

        if author.lower() == 'q':
            break

        isbn: str = Prompt.ask('ISBN')

        if isbn.lower() == 'q':
            break

        status: str | None = library.add_book(Book(title, author, isbn))

        clear_screen()

def prompt_remove(library: Library) -> None:
    status: str | None = None

    while True:
        print('Remove mode. Press [q] to exit.')

        if status:
            print(f'STATUS: {status}')

        isbn: str = Prompt.ask('ISBN')

        if isbn.lower() == 'q':
            break

        status: str | None = library.remove_book(isbn)

        clear_screen()

def prompt_list(library: Library) -> None:
    books: list[Book] = library.books

    page:      int = 0
    page_size: int = 5
    max_page:  int = math.ceil(len(books) / page_size)

    while True:
        table: Table = create_table_large()

        start: int = page_size * page
        end:   int = start + page_size

        end = min(end, len(books))

        for i in range(start, end):
            table.add_row(books[i].title, books[i].author, books[i].isbn, books[i].publisher,
                          books[i].cover, books[i].category, str(books[i].edition),
                          str(books[i].year), str(books[i].pages))

        rprint(Align(Panel(table, title=f'Page {page + 1} of {max_page}'), align='center'))

        prompt: str = Prompt.ask(r'\[u]p, \[d]own, \[q]uit', choices=['u', 'd', 'q'])

        match prompt:
            case 'u':
                if page != 0:
                    page -= 1
            case 'd':
                if end != len(books):
                    page += 1
            case 'q':
                break

        clear_screen()

def prompt_search(library: Library) -> None:
    # TODO: add multiple pages to search table if necessary

    table: Table = create_table_small()
    query: str   = Prompt.ask('Search')

    books: list[Book] = library.search_fuzz(query)

    if books:
        for book in books:
            table.add_row(book.title, book.author, book.isbn)

        rprint(Align(Panel(table), align='center'))
    else:
        print('No books found.')

def prompt_export() -> None:
    # TODO: deal with file already existing

    do_export = Confirm.ask('Convert the saved JSON to CSV?')

    if do_export:
        csv_file_path = json_to_csv(DEFAULT_FILE_PATH)
        print(f'File {DEFAULT_FILE_PATH} exported to {csv_file_path}.')

def create_table_small() -> Table:
    table: Table = Table(box=box.HORIZONTALS, row_styles=['', 'dim'])

    table.add_column('Title', style='#94e2d5', header_style='#94e2d5')
    table.add_column('Author', style='#74c7ec', header_style='#74c7ec')
    table.add_column('ISBN', style='#b4befe', header_style='#b4befe')

    return table

def create_table_large() -> Table:
    table: Table = Table(box=box.HORIZONTALS, row_styles=['', 'dim'])

    table.add_column('Title', style='#94e2d5', header_style='#94e2d5')
    table.add_column('Author', style='#74c7ec', header_style='#74c7ec')
    table.add_column('ISBN', style='#b4befe', header_style='#b4befe')
    table.add_column('Publisher', style='#94e2d5', header_style='#94e2d5')
    table.add_column('Cover', style='#74c7ec', header_style='#74c7ec')
    table.add_column('Category', style='#b4befe', header_style='#b4befe')
    table.add_column('Edition', style='#94e2d5', header_style='#94e2d5')
    table.add_column('Year', style='#74c7ec', header_style='#74c7ec')
    table.add_column('Pages', style='#b4befe', header_style='#b4befe')

    return table

def run_app() -> None:
    library: Library = Library()

    try:
        library.load_file(DEFAULT_FILE_PATH)
    except FileNotFoundError:
        print(f'The {DEFAULT_FILE_PATH} file could not be located.')

        while True:
            choice: bool = Confirm.ask(f'Create a new {DEFAULT_FILE_PATH} file?')

            match choice:
                case True:
                    break
                case False:
                    return
    except json.JSONDecodeError as e:
        is_empty: bool = os.stat(DEFAULT_FILE_PATH).st_size == 0

        if is_empty:
            print(f'Empty file {DEFAULT_FILE_PATH}, continuing.')
        else:
            print(f'ERROR: Error decoding JSON from file {DEFAULT_FILE_PATH}: {e}')
            return

    while True:
        user_input: str = Prompt.ask(r'\[a]dd, \[r]emove, \[l]ist, \[s]earch, \[e]xport, \[q]uit',
                                     choices=['a', 'r', 'l', 's', 'e', 'q'])

        match user_input:
            case 'a':
                clear_screen()
                prompt_add(library)
                clear_screen()
            case 'r':
                clear_screen()
                prompt_remove(library)
                clear_screen()
            case 'l':
                clear_screen()
                prompt_list(library)
                clear_screen()
            case 's':
                clear_screen()
                prompt_search(library)
            case 'e':
                clear_screen()
                prompt_export()
            case 'q':
                library.update_file(DEFAULT_FILE_PATH)
                return

def main() -> None:
    run_app()

if __name__ == '__main__':
    main()
