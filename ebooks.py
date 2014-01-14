# -*- coding: utf8 -*- 

__author__ = "A. Daouzli"
__copyright__ = "Copyright 2013, A. Daouzli"
__licence__ = "GPL3"
__version__ = "0.0.1"
__maintainer__ = "A. Daouzli"

# The application() function is the function that responses to the HTTP request.
# It is this function that you should link to your server.


import os
import sys
import epub

############ custom data

books_path = "/path/to/your/ebooks"
formats = ['epub','pdf']
ignored_chars = ['(', '[']
lang = 'en'
if lang == 'fr':
    ignored_words = ['le ', 'la ', 'les ', 'l\''] # must be lower case

    str_html_head_title = "Mes livres"
    str_html_body_title = "Voici la liste de bouquins"
    str_html_full_list = "Liste complète"
    str_html_no_letter = "Liste des bouquins ne commançant pas par une lettre"
    str_html_with_letter = "Liste des bouquins commançant par la lettre"
    str_html_containing = "Liste des bouquins contenant"
    str_html_select_page = "Sélectionner la page"
    str_html_author = "Auteur"
    str_html_summary = "Résumé"
    str_html_download = "Télécharger le bouquin"
    str_html_go_top = "Remonter"
    str_html_404 = '404 NOT FOUND'
    str_html_bad_page = "Page incorrecte"
    str_html_home = "Accueil"
    str_html_search = "Rechercher"
else:
    ignored_words = ['the ', 'a '] # must be lower case

    str_html_head_title = "My books"
    str_html_body_title = "Here is the books list"
    str_html_full_list = "Full list"
    str_html_no_letter = "List of books not starting with a letter"
    str_html_with_letter = "List of books starting with the letter"
    str_html_containing = "List of books containing"
    str_html_select_page = "Select a page"
    str_html_author = "Author"
    str_html_summary = "Summary"
    str_html_download = "Download the book"
    str_html_go_top = "Go back to the top of the page"
    str_html_404 = '404 NOT FOUND'
    str_html_bad_page = "Bad page"
    str_html_home = "Home"
    str_html_search = "Search"
############ end of custom data


def first_letter(name):
    '''Return the first letter ignoring non significant words or characters.

    @param name: the string which first letter should be retrieved
    @return: the first significant letter

    '''
    n = name.lower()
    l = n[0]
    for w in ignored_words:
        if n.startswith(w):
            l = n[len(w)]
    if n[0] in ignored_chars:
        l = n[1]
    return l

def get_epub_author(book):
    '''Retrieve the book's author from an Epub file.

    @param book: the book informations containing the file name, path,...
    @return: a string containing the author if found else an error message

    '''
    try:
        eb = epub.open_epub(books_path+'/'+book['file'])
        try:
            auth = eb.opf.metadata.creators[0][0].encode('utf-8')
        except:
            try:
                auth = eb.opf.metadata.creators[0][0].encode('ascii')
            except:
                auth = "error epub retrieve creator"
        eb.close()
    except:
        auth = "error epub open " + book['file']
    return auth

def get_epub_description(book):
    '''Retrieve the book's description from an Epub file.

    @param book: the book informations containing the file name, path,...
    @return: a string containing the description if found else an error message

    '''
    try:
        eb = epub.open_epub(books_path + '/' + book['file'])
        try:
            desc = eb.opf.metadata.description.encode('utf-8')
        except:
            try:
                desc = eb.opf.metadata.description.encode('ascii')
            except:
                desc = "error epub retrieve description"
        eb.close()
    except:
        desc = "error epub open "+books_path + '/' + book['file']
    return desc

def get_file_list(path):
    '''Retrieve the list of ebooks from a path.

    @param path: string containing the path where to search files.
    @return: a list of found ebooks. Each element of the list contains
    the path, the file name, the name (without the file extension), the
    first significant letter and an id.
    @rtype: list of dictionaries

    '''
    list_books = []
    path = os.path.abspath(path)
    i = 1
    for elem in os.listdir(path):
        if '.' in elem and elem[elem.rindex('.')+1:].strip() in formats:
            file_name = elem
            name = elem[:elem.rindex('.')]
            letter = first_letter(name)
            list_books.append( {'path': path, 'file': file_name, 'name': name,
                                'letter': letter, 'id': i} )
            i += 1
    return list_books

def all_letters():
    '''Get the list of all alphabetical letters.
    '''
    l = [chr(i) for i in xrange(ord('a'), ord('z')+1)]
    return l

def gen_page_list(book_list, letter="*"):
    '''Generates a filtered list of books.

    @param book_list: the initial list of books
    @type: list of dictionaries
    @param letter: the filter:
    - If it is an alphabetical letter then the returned list will contain
    all books starting with that letter.
    - If it is '*' no filter is done, thus all books are kept.
    - If it is an empty string '', then all books not starting with a letter
    will be kept (e.g.: starting with a number)
    @return: the list of books filtered
    @rtype: list of dictionaries

    '''
    letters = all_letters()
    page_list = []
    for book in book_list:
        if (letter == "" and book['letter'] not in letters) or \
            letter == book['letter'] or \
            letter == "*":
                page_list.append(book)
    return page_list

def gen_page_list_search(book_list, search):
    '''Retrieve a list of books that title contains a particular item.

    @param book_list: the list of books where searching
    @type: list of dictionaries
    @param search: the item to search. The search is not case sensitive.
    @return: the list of books containing the searched item
    @rtype: list of dictionaries

    '''
    page_list = []
    for book in book_list:
        if search.lower() in book['file'].lower():
                page_list.append(book)
    return page_list

def get_html_page(books, letter, selected_book=None):
    '''Generate the HTML page with the list of books

    @param books: the list of books to show
    @type: list of dictionaries
    @param letter: the applied filter ("", "*" or a letter) or the searched item
    @param selected_book: the selected book if any
    @type: dictionary

    '''
    letter = letter.lower()
    head = '''<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <title>''' + str_html_head_title + '''</title>
    </head>

    <body>
        <h1>''' + str_html_body_title + '''</h1>
    '''
    if letter == '*':
        content = '<h2>' + str_html_full_list + '</h2>'
    elif letter == '':
        content = '<h2>' + str_html_no_letter + '</h2>'
    elif len(letter) > 1:
        content = '<h2>' + str_html_containing + ' "' + letter + '"</h2>'
    else:
        content = '<h2>' + str_html_with_letter + ' <b>' + letter.upper() + '</b>.</h2>'
    content += '\n' + str_html_select_page + ':<br/>\n'
    content += '<a href="/ebooks/"> -nop- </a>'
    for l in all_letters():
        content += '<a href="/ebooks/' + l + '"> -' + l.upper() + '- </a> '
    content += '<a href="/ebooks/*"> -all- </a>'
    content += '\n<br/>' + str_html_search + '<br/>\n'
    content += '<form method="post" action="/ebooks/search">\n'
    content += '  <input type="search" name="search" /><br/>\n'
    content += '</form>'
    content += '<br/>\n<ul>\n'
    for book in books:
        content += '<li id="idx_' + str(book['id']) + '"> <a href="/ebooks/books/' + book['file'] + '#idx_' + str(book['id']) + '">' + book['file'] + '</a> </li>\n'
        if selected_book and book['file'] == selected_book['file']:
            if selected_book['file'].endswith('.epub'):
                content += '<b>' + str_html_author + '</b>: ' + get_epub_author(selected_book) + '<br/>\n'
                content += '<b>' + str_html_summary + '</b>: ' + get_epub_description(selected_book) + '<br/>\n'
            content += '<a href="/ebooks/dl/' + book['file'] + '">' + str_html_download + '</a><br/><br/>\n'
            content += '<a href="/ebooks/books/' + book['file'] + '">' + str_html_go_top + '</a><br/><br/>\n'
    content += '</ul>\n'
    foot = '''
        </body>
    </html>
    '''
    output = head + content + foot
    return output

def has_valid_extension(path):
    '''Checks if file has a valid extension

    @param path: the path to check
    @return: True if succeeded else False

    '''
    result = False
    for ext in formats:
        if path.endswith(ext):
            result = True
            break
    return result

def application(environ, start_response):
    '''Serve the client HTTP request.

    @param environ: the request informations.
    @param start_response: the WSGI callable to send 
    the headers response and the status
    @return: a list with the data to send to the client
    (web page or book data)

    '''
    status = '200 OK'
    path = environ['PATH_INFO']
    content_type = 'text/html'
    path = path.replace('/ebooks','')
    file_name = books_path + path.replace('/books','').replace('/dl','')

    # The request is not valid
    if len(path) > 2 and not path.endswith('.epub') and path != '/search':
        status = str_html_404 
        output = '<html>' + str_html_bad_page + '.'+str(path)+' <a href="/ebooks/*">' + str_html_home + '</a></html>'

    # A download was requested
    elif '/dl/' in path and has_valid_extension(path) and os.path.exists(file_name):
        output = open(file_name).read()
        content_type = 'application/octet-stream'

    # A book was selected
    elif path.endswith('.epub'):
        book = None
        letter = '*'
        full_book_list = get_file_list(books_path)
        book_list = gen_page_list(full_book_list, "*")
        for b in book_list:
            if os.path.basename(b['file']) == os.path.basename(path):
                book = b
                break
        output = get_html_page(book_list, letter, book)

    # A list of book is to be shown
    else:
        liste = get_file_list(books_path)
        path = path.replace("/", "")
        letter = ""
        if len(path) > 0:
            letter = path[0]
        full_book_list = get_file_list(books_path)
        if environ['REQUEST_METHOD'].upper() == 'POST':
            input = environ['wsgi.input'].read().split('=')
            search = input[1]
            if input[0].strip() == 'search':
                letter = search 
                book_list = gen_page_list_search(full_book_list, search)
            else:
                letter = "*"
                book_list = gen_page_list(full_book_list, "*")
        else:
            book_list = gen_page_list(full_book_list, letter)
        output = get_html_page(book_list, letter)

    response_headers = [('Content-type', content_type), ('charset', 'utf-8'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)

    return [output]
