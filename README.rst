Reddit Account Deleter
======================

Delete all Submissions and Comments ever made by your account.

Authentication is done via OAuth 2.0. Interaction with Reddit is handled via
PRAW. The website itself is done with Django and the database is sqlite3.

Reading the codebase
--------------------

The project is built after standard Django conventions. General stuff such as
this README is located in the root folder. Additionally this is also where
`nuker.py` is located. This is a program that's run side-by-side with the
website and handles the deletion process.

The account_deleter project folder contains files for the entire project. Such
as the project wide settings and the main database.

The 'deleter' app is  located inside the deleter folder. It is the only app on
the website, so all views etc. are inside of it.

Finally the docs folder contain documentation.

Usage and dependencies
----------------------

If you want to try this library out yourself, then clone it with Git.

.. code-block:: bash

   $ git clone https://github.com/Damgaard/reddit-account-deleter.git

This project was developed with Python 2.7.3. It may, or may not, run with
other versions of Python. It requires a number of Python libraries to run.
These libraries and their versions are listed in the file `requirements.txt`.
Install them like this.

.. code-block:: bash

   $ pip install -r requirements.txt

Additionally sqlite3 must be installed on the system as well as a server. I
used Apache, but you can use whatever you want.

License
-------

Copyright (C) 2013 Andreas Damgaard Pedersen

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnuorg/licenses/>.
