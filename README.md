ebooks
======

This is a very basic python WSGI web application to browse an ebook collection. 
Accepted formats are PDF and EPUB but you can easily add others.

It allows searching, filtering by letter, getting book's informations (author, description), and downloading.
The application is contained in a single python file. It is not really pythonist as it is made of basic functions and no class.
But my objective was to have a dirty basic program quickly working. And it does what it is supposed to.
I would like to enhance it when I will have time.


Before starting:
---------------

The python epub module is used so you must install it first:

    sudo pip install epub

You must set your ebooks directory to the variable books_path in the ebook.py code.
Then you need a python WSGI server to run the application.
I'm serving the application using gunicorn via nginx. You can easily use any other alternative (e.g.: apache2 + mod_python).



To run it with Nginx and gunicorn:
---------------------------------

First you should install Nginx and gunicorn:

    sudo apt-get install nginx gunicorn

- Then configure Nginx to enable a socket connection to gunicorn:
open file /etc/nginx/sites-enabled/default and add:


    server {
    ...
    
        location /ebooks/ {
                proxy_pass http://unix:/tmp/gunicorn.sock;
        }
        
    ...
    }


- Go to the path containing your script ebooks.py and run gunicorn:


    $ gunicorn -b unix:/tmp/gunicorn.sock --workers=2 ebooks:application

- Browse your ebooks collection with a web browser:

    e.g.:

    $ links2 http://127.0.0.1/ebooks

(of course you can use Epiphany, Firefox, Chromium or any other browser of your choice.)
