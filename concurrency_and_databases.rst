Concurrency and databases
=========================

This is a short design document over concurrency and it's effect on the chosen
database for this project. It has been written before the implementation was
created to follow README Driven Development.

The need for concurrency
------------------------

Each API Request to reddit costs 2 seconds. So waiting until the account has
been deleted to return a ``HTTPResponse`` is not a possibility. Instead initial
error testing must be run and then a page saying the deletion process has begun
returned. Ideally some solution, potentially involving AJAX, would continually
update the returned page with information about how the process was going,
however such knowledge is currently beyond me and will be postponed to a later
project when I have stronger knowledge of Django fundamentals.

The process of deleting the Redditor will therefore be spun of from the process
of returning a webpage. Since it will involve many API calls it may take
several minutes to execute. While the process is running, another user may
decide to use the website to delete their content. Which would start another
redditor deletion process.

Using Celery as first intended introduced unnecessary complexity. All that's
really needed is to create a line in a database with the data necessary to
delete the redditor. A second continually script will then periodically poll
the database and see if there is any unprocessed jobs. This is a simple
solution that does not involve any concurrency libraries and race situation
will be handled by the database. Additionally since there's only a single PRAW
instance running, following reddit's API rules become very simple.

Schema
------

The database has the following fields, here shown populated with example data.

.. code-block:: text

  Id PRIMARY KEY INT | Username TEXT | Access_token TEXT | Gained_at INT
  ----------------------------------------------------------------------
  1                  | _Daimon_      | 12asf7asjn12as7   | 1382646830
  2                  | circlejerk    | asd67iasfdku8af   | 1382642199

The Id is auto incremented. This makes it possible to see how many accounts
have been nuked, while at at the same time not keeping any information about
the redditor.
