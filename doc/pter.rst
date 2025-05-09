
Synopsis
========

::

  pter [-h] [-v] [-u] [-n task] [-s search] [-c configuration] filename [filename ...]
  qpter [-h] [-v] [-u] [-a] [-n task] [-c configuration] filename [filename ...]


Description
===========

pter is a tool to manage your tasks when they are stored in the todo.txt
file format. pter is targeted at users applying the `Getting Things Done`_
method, but can be used by anyone that uses todo.txt files.

pter offers these features:

 - Fully compatible to the todo.txt standard
 - Support for `due:`, `h:`, `t:`
 - Save search queries for quick access (see `Searching`_ and `Named Searches`_)
 - Sort tasks through search queries (see `Sorting`_)
 - Convenient entering of dates (see `Relative Dates`_)
 - Configurable behaviour, shortcuts, and colors (see `Files`_)
 - Task sequencing (see `Task Sequences`_)
 - Automatic identifiers (see `Unique Task Identifiers`_)
 - `Time Tracking`_
 - `Recurring Tasks`_

qpter is the Qt version of pter (ie. pter with a graphical user interface)
and supports mostly the same features but sometimes looks for other
sections in the configuration.


Options
=======

  ``-c configuration``
    Path to the configuration file you wish to use. The default is
    ``$XDG_CONFIG_HOME/pter/pter.conf`` (usually
    ``~/.config/pter/pter.conf``).

  ``-h``
    Show the help.

  ``-v``
    Show the version of pter/qpter.

  ``-u``
    Check whether a new version of pter is available on pypi (requires an
    internet connection).

  ``-n task``
    Add ``task`` to the todo.txt file. The advantage of using this over
    just ``echo "task" >> todo.txt`` is that relative dates are properly
    expanded (see `Relative Dates`_).
    If you provide ``-`` instead of a task, the task will be read from
    stdin. Multiple tasks can be added, one per line.

  ``-s search``
    Only available for pter: load this named search upon startup. If a
    named search by that name does not exist, use this as a search term
    from the start.

  ``-a``
    Only available for qpter: either start qpter, immediately open the New
    Task panel. Or, if qpter is running already, bring it to the foreground
    and open the New Task panel.

  ``-l``
    Log level. Can be one of ``DEBUG``, ``INFO``, ``WARNING``, ``ERROR``,
    or ``FATAL``. Defaults to ``ERROR``.

  ``--log-file``
    In what file to log the messages. This is also the file where you can
    find information about crashes, if you encounter any.

  ``filename``
    Path to your todo.txt file. The first file that you provide is the one
    where new tasks will be created in.


Files
=====

Aside from the data files in the todo.txt format (see `Conforming to`_),
pter's behaviour can be configured through a configuration file.

The configuration file's default location is at ``~/.config/pter/pter.conf``.

There should have been an example configuration file, ``example.conf``
distributed with your copy of pter that can give you an idea on how that
works. In this documentation you will find the full explanation.

Note that the configuration file content is case-sensitive!

The configuration file is entirely optional and each option has a default
value. That allows you to run pter just fine without ever configuring
anything.

The configuration file has these four sections:

 - `General`_, for general behaviour,
 - `Symbols`_, for icons used in the (task) display,
 - `Keys`_, to override default keyboard controls in lists,
 - Editor:Keys, to override the default keyboard controls in edit fields (detailed in `Keys`_),
 - `Colors`_, for coloring the TUI,
 - `GUI:Colors`_, for coloring the tasks in the GUI,
 - `Highlight`_, for coloring specific tags of tasks,
 - GUI:Highlight, for coloring specific tags of tasks (GUI version, see `Highlight`_).
 - `GUI`_, for other GUI specific options
 - `Include`_, to include another configuration file

General
-------

  ``use-colors``
    Whether or not to use colors. Defaults to 'yes'.

  ``scroll-margin``
    How many lines to show at the lower and upper margin of lists. Defaults
    to '5'.

  ``safe-save``
    Safe save means that changes are written to a temporary file and that
    file is moved over the actual file after writing was completed.
    Defaults to 'yes'.

    This can be problematic if your files are in folders synchronised with
    cloud services.

  ``search-case-sensitive``
    Whether or not to search case-sensitive. Defaults to 'yes'.

  ``human-friendly-dates``
    Here you can define what fields of a task, that are known to contain a
    date, should be displayed in a more human-friendly way. By default no
    dates are translated.

    Human-friendly means that instead of a 'YYYY-MM-DD' format it might
    show 'next wednesday', 'tomorrow', or 'in 2 weeks'. It means that
    dates, that are further away (in the future or the past) will be less
    precise.

    Possible values are ``due`` (for due dates), ``t`` (for the
    threshold/tickler dates), ``completed`` (for completion dates),
    ``created`` (for creation dates), or ``all`` (for all of the above).
    You can also combine these values by comma separating them like this::

      [General]
      human-friendly-dates = due, t

  ``task-format``
    The format string to use for displaying tasks. Defaults to "``{selection: >} {nr: >} {done} {tracking }{due }{(pri) }{description}``".

    See `Task Format`_ below for more details.

  ``clear-contexts``
    A list of comma separated contexts (without the leading ``@``) to remove from a task
    when it is being marked as done.

    For example, you might want to remove the ``@in`` context or any
    ``@today`` tags when marking a task as done. In that case
    ``clear-contexts`` should be set to ``in, today``.

  ``default-threshold``
    The default ``t:`` search value to use, even when no other search has
    been defined. Defaults to 'today'.

    This option supports `Relative Dates`_.

  ``delegation-marker``
    Marker to add to a task when delegating it. Defaults to ``@delegated``.

  ``delegation-action``
    Action to take when delegating a task.
    One of 'none', or 'mail-to' (defaulting to 'mail-to').

    'none' does nothing, but 'mail-to' will attempt to start your email
    program to write an email. If your task has a 'to:' attribute (or
    whatever you set up for ``delegation-to``, it will be used as the
    recipient for the email.

  ``delegation-to``
    Attribute name to use when delegating a task via email. Defaults to
    ``to``. Eg. "clean the dishes to:bob" will compose the email to "bob"
    when delegating a task and the delegation action is "mail-to".

  ``editor``
    The external text editor to use instead of whatever is defined in the
    ``VISUAL`` or ``EDITOR`` environment variables.
    If pter can’t find a valid editor in neither this configuration option
    nor these environment variables, it will fall back to ``nano`` in the
    wild hopes that it might be installed.

    Defaults to nothing, because the environment variables should be all
    that’s required.

    This option is ignored in ``qpter``.

  ``protocols``
    What protocols should be considered when using the 'Open URL' function
    on a task. Defaults to ``http, https, mailto, ftp, ftps``.

  ``add-creation-date``
    Whether or not to automatically add the creation date of a task
    to it. Defaults to ``yes``.

  ``create-from-search``
    If set to ``yes``, positive expressions (that do not refer to time or
    ``done``) of the active search (eg. ``@context +project word``, but not
    ``-@context due:+7d done:y -others``) will be added automatically to a
    newly created task. Defaults to ``no``.

  ``auto-id``
    Whether or not to automatically add an ID to newly created tasks.
    Defaults to ``no``.

  ``hide-sequential``
    Whether or not to automatically hide tasks that have uncompleted
    preceding tasks (see `Task Sequences`_). Defaults to ``yes``.

  ``info-timeout``
    How long should info messages remain visible in the status bar of the
    TUI application. Defaults to ``5``, so 5 seconds.

  ``use-completion``
    Whether or not to use completion for contexts (``@``) and projects
    (``+``) in the search field, task creation, and task editing fields of
    the TUI. Defaults to ``yes``.

  ``delete-is``
    What behaviour the delete function is actually showing. Can be one of
    these:

     - ``disabled``, no functionality at all. There is no delete. This is
       the default.
     - ``trash``, deleted tasks are moved to the trash file (see
       ``trash-file`` option below).
     - ``permanent``, actually deletes the task.

  ``trash-file``
    What your trash file is. This option is only used if ``delete-is`` is
    set to ``trash``. Defaults to ``~/.config/pter/trash.txt``.

  ``reuse-recurring``
    Reuse existing recurring task entry instead of creating a new one. If
    set, completing a task with a ``rec:`` (recurring) tag will be reused
    for the follow-up task instead of creating a new task.

    Defaults to ``no``.

  ``related-show-self``
    Whether or not to show the current task, too, when showing its related
    tasks. This can be set to ``yes``, ``no`` or ``force``.

    ``yes`` means, not only the related tasks are shown, but also this one.

    ``force`` is the same as ``yes``, but if the current task does not have
    an ``id:`` attribute, it will be given one. In other words, this option
    may modify your ``todo.txt`` file.

    Defaults to ``yes``.


Symbols
-------

The following symbols (single unicode characters or even longer strings of
unicode characters) can be defined:

 - ``selection``, what symbol or string to use to indicate the selected item of a list
 - ``not-done``, what symbol or string to use for tasks that are not done
 - ``done``, what symbol or string to use for tasks that are done
 - ``overflow-left``, what symbol or string to use to indicate that there is more text to the left
 - ``overflow-right``, what symbol or string to use to indicate that there is more text to the right
 - ``overdue``, the symbol or string for tasks with a due date in the past
 - ``due-today``, the symbol or string for tasks with a due date today
 - ``due-tomorrow``, the symbol or string for tasks with a due date tomorrow
 - ``tracking``, the symbol or string to show that this task is currently being tracked

If you want to use spaces around your symbols, you have to quote them either
with ``'`` or ``"``.

An example could be::

    [Symbols]
    not-done = " "
    done = ✔


Keys
----

In the configuration file you can assign keyboard shortcuts to the various
functions in pter and qpter.

For details on how to setup shortcuts for qpter, please see below in
section `GUI Keys`_.

There are three main distinct groups of functions. The first, for general
lists:

 - ``cancel``: cancel or exit the current window or input field
 - ``jump-to``: enter a number to jump to that item in the list
 - ``first-item``: jump to the first item in a list
 - ``last-item``: jump to the last item in a list
 - ``page-up``: scroll up by one page
 - ``page-down``: scroll down by one page
 - ``next-item``: select the next item in a list
 - ``prev-item``: select the previous item in a list

Second, there are more complex functions to edit tasks or control pter
(for these functions you may use key sequences, see below for details):

 - ``quit``: quit the program
 - ``show-help``: show the full screen help (only key bindings so far)
 - ``open-manual``: open this manual in a browser
 - ``create-task``: create a new task
 - ``edit-task``: edit the selected task
 - ``edit-external``: edit the selected task in an external text editor
 - ``delete-task``: delete the selected task or move it to trash, depends
   on the configuration option ``delete-is`` (by default not bound to any
   key)
 - ``load-search``: show the saved searches to load one
 - ``open-url``: open a URL of the selected task
 - ``refresh-screen``: rebuild the GUI
 - ``reload-tasks``: enforce reloading of all tasks from all sources
 - ``save-search``: save the current search
 - ``search``: enter a new search query
 - ``clear-search``: clear the search query
 - ``search-context``: select a context from the selected task and search for it
 - ``search-project``: select a project from the selected task and search for it
 - ``select-context``: select a context from all used contexts and search for it
 - ``select-project``: select a project from all used projects and search for it
 - ``show-related``: show tasks that are related to this one (by means of ``after:`` or ``ref:``)
 - ``toggle-done``: toggle the "done" state of a task
 - ``toggle-hidden``: toggle the "hidden" state of a task
 - ``toggle-tracking``: start or stop time tracking for the selected task
 - ``delegate``: delegate a task
 - ``prio-a``: set the selected task's priority to ``(A)``
 - ``prio-b``: set the selected task's priority to ``(B)``
 - ``prio-c``: set the selected task's priority to ``(C)``
 - ``prio-d``: set the selected task's priority to ``(D)``
 - ``prio-none``: remove the priority from the selected task
 - ``prio-up``: increase the priority of the selected task
 - ``prio-down``: decrease the priority of the selected task
 - ``multi-select``: add this to a set of selected tasks, which you can then perform bulk operations on
 - ``nop``: nothing (in case you want to unbind keys)

And finally, the list of functions for edit fields:

 - ``cancel``, cancel editing, leave the editor (reverts any changes)
 - ``del-left``, delete the character left of the cursor
 - ``del-right``, delete the character right of the cursor
 - ``del-to-bol``, delete all characters from the cursor to the beginning of the line
 - ``go-bol``, move the cursor to the beginning of the line
 - ``go-eol``, move the cursor to the end of the line
 - ``go-left``, move the cursor one character to the left
 - ``go-right``, move the cursor one charackter to the right
 - ``goto-empty``, move the cursor to the next ``tag:value`` where the is no ``value``
 - ``submit-input``, accept the changes, leave the editor (applies the changes)
 - ``select-file``, when creating a new task, this allows you to select
   what todo.txt file to save the task in
 - ``comp-next``, next item in the completion list
 - ``comp-prev``, previous item in the completion list
 - ``comp-use``, use the selected item in the completion list
 - ``comp-close``, close the completion list

Keyboard shortcuts are given by their character, for example ``d``.
To indicate the shift key, use the upper-case of that letter (``D`` in this
example).

To express that the control key should be held down for this shortcut,
prefix the letter with ``^``, like ``^d`` (for control key and the letter
"d").

Additionally there are some special keys understood by pter:

 - ``<backspace>``
 - ``<del>``
 - ``<left>`` left cursor key
 - ``<right>`` right cursor key
 - ``<up>`` cursor key up
 - ``<down>`` cursor key down
 - ``<pgup>`` page up
 - ``<pgdn>`` page down
 - ``<home>``
 - ``<end>``
 - ``<escape>``
 - ``<return>``
 - ``<tab>``
 - ``<f1>`` through ``<f12>``

An example could look like this::

  [Keys]
  ^k = quit
  <F3> = search
  C = create-task


Key Sequences
~~~~~~~~~~~~~

For the functions of the second list, the more complex functions for
editing tasks or controlling pter, you may also use key sequences. For
example, you may want to prefix all shortcuts to manipulate the priority of
a task with the letter ``p`` and define these sequences::

  [Keys]
  p+ = prio-up
  p- = prio-down
  pa = prio-a
  pb = prio-b
  pc = prio-c
  pd = prio-d
  p0 = prio-none

Now to increase the priority of a task, you would type first ``p``,
followed by ``+``.

The progress of a key sequence will show in the lower left of the screen,
showing the keys that you have pressed so far. To cancel a key sequence
type the single key shortcut for ``cancel`` (usually ``Escape`` or ``Ctrl-C``)
or just type any invalid key that's not part of the sequence (in the
previous example, ``px`` would do the trick).


GUI Keys
~~~~~~~~

To assign shortcuts to functions in the Qt GUI, you will have to use the Qt
style key names, see https://doc.qt.io/qt-5/qkeysequence.html#details .

The assignment is done in the group ``GUI:Keys``, like this::

  [GUI:Keys]
  new = Ctrl+N
  toggle-done = Ctrl+D

Available function names are:

 - ``quit``, quit qpter
 - ``open-manual``, open this manual
 - ``open-file``, open an additional todo.txt,
 - ``new``, open the editor to create a new task,
 - ``new-related``, open the editor to create a new task that is
   automatically related (has a ``ref:`` attribute) to the
   currently selected task. If the currently selected task does not have an
   ``id:`` yet, it will be given one automatically
 - ``new-subsequent``, open the editor to create a new task that is
   following the currently selected task (has an ``after:`` attribute).
   If the currently selected task does not have an ``id:`` yet, it will
   be given one automatically.
 - ``edit``, opens the editor for the selected task,
 - ``toggle-done``, toggles the completion of a task,
 - ``toggle-tracking``, toggle the 'tracking' attribute of the selected task,
 - ``toggle-hidden``, toggle the 'hidden' attribute of the selected task,
 - ``search``, opens and focuses the search field,
 - ``named-searches``, opens and focuses the list of named searches,
 - ``focus-tasks``, focuses the task list,
 - ``delegate``, delegate the selected task,
 - ``delete-task``, delete the selected task (subject to the value of the configuration option ``delete-is``)
 - ``prio-up``, increase the priority of the selected task
 - ``prio-down``, decrease the priority of the selected task
 - ``prio-none``, remove the priority of the selected task
 - ``multi-select``: add this to a set of selected tasks, which you can then perform bulk operations on
 - ``toggle-dark-mode``, toggle between dark and light mode (requires qdarkstyle to be installed)


Colors
------

Colors are defined in pairs, separated by comma: foreground and background
color. Some color's names come with a ``sel-`` prefix so you can define the
color when it is a selected list item.

You may decide to only define one value, which will then be used as the text
color. The background color will then be taken from ``normal`` or ``sel-normal``
respectively.

If you do not define the ``sel-`` version of a color, pter will use the
normal version and put the ``sel-normal`` background to it.

If you specify a special background for the normal version, but none for the
selected version, the special background of the normal version will be used
for the selected version, too!

 - ``normal``, any normal text and borders
 - ``sel-normal``, selected items in a list
 - ``error``, error messages
 - ``sel-overflow``, ``overflow``, color for the scrolling indicators when editing tasks (and when selected)
 - ``sel-overdue``, ``overdue``, color for a task when it’s due date is in the past (and when selected)
 - ``sel-due-today``, ``due-today``, color for a task that’s due today (and when selected)
 - ``sel-due-tomorrow``, ``due-tomorrow``, color for a task that’s due tomorrow (and when selected)
 - ``inactive``, color for indication of inactive texts
 - ``help``, help text at the bottom of the screen
 - ``help-key``, color highlighting for the keys in the help
 - ``pri-a``, ``sel-pri-a``, color for priority A (and when selected)
 - ``pri-b``, ``sel-pri-b``, color for priority B (and when selected)
 - ``pri-c``, ``sel-pri-c``, color for priority C (and when selected)
 - ``context``, ``sel-context``, color for contexts (and when selected)
 - ``project``, ``sel-project``, color for projects (and when selected)
 - ``tracking``, ``sel-tracking``, color for tasks that are being tracked right now (and when selected)

If you prefer a red background with green text and a blue context, you could define your
colors like this::

  [Colors]
  normal = 2, 1
  sel-normal = 1, 2
  context = 4


GUI:Colors
----------

The GUI has a somewhat different coloring scheme. The available colors are:

 - ``normal``, any regular text in the description of a task,
 - ``done``, color for tasks that are done,
 - ``overdue``, text color for overdue tasks,
 - ``due-today``, color for tasks that are due today,
 - ``due-tomorrow``, color for tasks that are due tomorrow,
 - ``project``, color for projects,
 - ``context``, color for contexts,
 - ``tracking``, color for tasks that are currently being tracked,
 - ``pri-a``, color for the priority A,
 - ``pri-b``, color for the priority b,
 - ``pri-c``, color for the priority C,
 - ``url``, color for clickable URLs (see ``protocols`` in `General`_)


Highlight
---------

Highlights work exactly like colors, but the color name is whatever tag you
want to have colored.

If you wanted to highlight the ``due:`` tag of a task, you could define
this::

  [Highlight]
  due = 8, 0

For the GUI, use ``GUI:Highlight``. The colors can be specific as hex
values (3, or 6-digits) or named::

  [GUI:Highlight]
  due = red
  t = #4ee
  to = #03fe4b


Task Format
-----------

The task formatting is a mechanism that allows you to configure how tasks are
being displayed in pter. It uses placeholders for elements of a task that you can
order and align using a mini language similar to `Python’s format
specification
mini-language <https://docs.python.org/library/string.html#formatspec>`_, but
much less complete.

qpter uses only part of the definition, see below in the list of field
names, if you only care for qpter.

If you want to show the task’s age and description, this is your
task format::

    task-format = {age} {description}

The space between the two fields is printed! If you don’t want a space
between, this is your format::

    task-format = {age}{description}

You might want to left align the age, to make sure all task descriptions start
below each other::

    task-format = {age: <}{description}

Now the age field will be left aligned and the right side is filled with
spaces. You prefer to fill it with dots?::

    task-format = {age:.<}{description}

Right align works the same way, just with ``>``. There is currently no
centering.

Suppose you want to surround the age with brackets, then you would want to use
this::

    task-format = {[age]:.<}{description}

Even if no age is available, you will always see the ``[...]`` (the amount of
periods depends on the age of the oldest visible task; in this example some
task is at least 100 days old).

If you don’t want to show a field, if it does not exist, for example the
completion date when a task is not completed, then you must not align it::

    task-format = {[age]:.<}{completed}{description}

You can still add extra characters left or right to the field. They will not
be shown if the field is missing::

    task-format = {[age}:.<}{ completed 😃 }{description}

Now there will be an emoji next to the completion date, or none if the task has
no completion date.

All that being said, qpter uses the same ``task-format`` configuration
option to show tasks, but will disregard some fields (see below) and only
use the field names, but not alignment or decorations.


Field Names
~~~~~~~~~~~

The following fields exist:

 - ``description``, the full description text of the task
 - ``created``, the creation date (might be missing)
 - ``age``, the age of the task in days (might be missing)
 - ``completed``, the completion date (might be missing, even if the task is completed)
 - ``done``, the symbol for a completed or not completed task (see below)
 - ``pri``, the character for the priority (might not be defined)
 - ``due``, the symbol for the due status (overdue, due today, due tomorrow; might not be defined)
 - ``duedays``, in how many days a task is due (negative number when overdue tasks)
 - ``selection``, the symbol that’s shown when this task is selected in the list (disregarded in qpter)
 - ``nr``, the number of the task in the list (disregarded in qpter)
 - ``tracking``, the symbol to indicate that you started time tracking of this task (might not be there)

``description`` is potentially consuming the whole line, so you might want to
put it last in your ``task-format``.


GUI
----

The GUI specific options are defined in the ``[GUI]`` section:

  ``font``
    The name of the font to use for the task list.

  ``font-size``
    The font size to use for the task list. You can specify the size either
    in pixel (eg. ``12px``) or point size (eg. ``14pt``). Unlike pixel
    sizes, point sizes may be a non-integer number, eg. ``16.8pt``. 

  ``single-instance``
    Whether or not qpter may only be started once.

  ``clickable``
    If enabled, this allows you to click on URLs (see option ``protocols``
    in `General`_) to open them in a webbrowser, and to click on contexts
    and projects to add them to the current search. Disabling this option
    may improve performance. The default is ``yes``, ie. URLs, contexts,
    and projects are clickable.

  ``daily-reload``
    The time (in format HH:MM) when qpter will automatically reload upon
    passing midnight. Defaults to 00:00.


Include
-------

You can specify a second configuration file to include after the primary
configuration file been loaded. This secondary configuration supports all
options as the primary but any option in the secondary configuration will
override existing options of the primary configuration option.

Example::

    [Include]
    path = ../extra.conf


Keyboard controls
=================

pter and qpter have different keyboard shortcuts.


pter
-----

These default keyboard controls are available in any list:

 - "↓", "↑" (cursor keys): select the next or previous item in the list
 - "j", "k": select the next or previous item in the list
 - "Home": go to the first item
 - "End": go the last item
 - ":": jump to a list item by number (works even if list numbers are not shown)
 - "1".."9": jump to the list item with this number
 - "Esc", "^C": cancel the selection (this does nothing in the list of tasks)

In the list of tasks, the following controls are also available:

 - "?": Show help
 - "m": open this manual in a browser
 - "e": edit the currently selected task
 - "E": edit the currently selected task in an external text editor
 - "n": create a new task
 - "/": edit the search query
 - "^": clear the search
 - "c": search for a context of the currently selected task
 - "p": search for a project of the currently selected task
 - "r": search for all tasks that this task is referring to with ``ref:`` or ``after:``
 - "F6": select one project out of all used projects to search for
 - "F7": select one context out of all used contexts to search for
 - "q": quit the program
 - "l": load a named search
 - "s": save the current search
 - "L": load a named task template
 - "S": Save a task as a named template
 - "u": open a URL listed in the selected task
 - "t": Start/stop time tracking of the selected task
 - ">": Delegate the selected task

In edit fields the following keyboard controls are available:

 - "←", "→" (cursor keys): move the cursor one character to the left or right
 - "Home": move the cursor to the first charater
 - "End": move the cursor to the last character
 - "Backspace", "^H": delete the character to the left of the cursor
 - "Del": delete the character under the cursor
 - "^U": delete from before the cursor to the start of the line
 - "Escape", "^C": cancel editing
 - "Enter", "Return": accept input and submit changes
 - "↓", "Tab", "^N": next item in the completion list
 - "↑", "^P": previous item in the completion list
 - "Tab": jump to the next ``key:value`` field where there is not ``value``
 - "Enter": use the selected item of the completion list
 - "Esc", "^C": close the completion list


qpter
------

 - Quit: ``Ctrl+Q``
 - Open the manual: ``F1``
 - Focus the task list: ``F6``
 - Open and focus the named searches: ``F8``
 - Create a new task: ``Ctrl+N``
 - Edit the selected task: ``Ctrl+E``
 - Toggle 'done' state of selected task: ``Ctrl+D``
 - Toggle 'hidden' state of selected task: ``Ctrl+H``
 - Toggle 'tracking' state of selected task: ``Ctrl+T``
 - Delegate the selected task: ``Ctrl+G``


Relative dates
==============

Instead of providing full dates for searches or for ``due:`` or ``t:`` when
editing tasks, you may write things like ``due:+4d``, for example, to specify
a date in 4 days.

A relative date will be expanded into the actual date when editing a task
or when being used in a search.

The suffix ``d`` stands for days, ``w`` for weeks, ``m`` for months, ``y`` for years.
The leading ``+`` is implied when left out and if you don’t specify it, ``d`` is
assumed.

``due`` and ``t`` tags can be as simple as ``due:1`` (short for ``due:+1d``, ie.
tomorrow) or as complicated as ``due:+15y-2m+1w+3d`` (two months before the date
that is in 15 years, 1 week and 3 days).

``due`` and ``t`` also support relative weekdays. If you specify ``due:sun`` it is
understood that you mean the next Sunday. If today is Sunday, this is
equivalent to ``due:1w`` or ``due:+7d``.

Finally there are ``today`` and ``tomorrow`` as shortcuts for the current day and
the day after that, respectively. These terms exist for readability only, as
they are equivalent to ``0d`` (or even just ``0``) and ``+1d`` (or ``1d``, or even
just ``1``), respectively.


Searching
=========

One of the most important parts of pter is the search. You can search for
tasks by means of search queries. These queries can become very long at
which point you can save and restore them (see below in `Named Searches`_).

Unless configured otherwise by you, the search is case-sensitive.

Here's a detailed explanation of search queries.

Some example search queries are listed in `Named Searches`_.


Search for phrases
------------------

The easiest way to search is by phrase in tasks.

For example, you could search for ``read`` to find any task containing the word
``read`` or ``bread`` or ``reading``.

To filter out tasks that do *not* contain a certain phrase, you can search with
``not:word`` or, abbreviated, ``-word``.


Search for tasks that are completed
-----------------------------------

By default all tasks are shown, but you can show only tasks that are not
completed by searching for ``done:no``.

To only show tasks that you already marked as completed, you can search for
``done:yes`` instead.


Hidden tasks
------------

Even though not specified by the todotxt standard, some tools provide the
“hide” flag for tasks: ``h:1``. pter understands this, too, and by default
hides these tasks.

To show hidden tasks, search for ``hidden:yes``. Instead of searching for
``hidden:`` you can also search for ``h:`` (it’s a synonym).


Projects and Contexts
---------------------

To search for a specific project or context, just search using the
corresponding prefix, ie. ``+`` or ``@``.

For example, to search for all tasks for project "FindWaldo", you could search
for ``+FindWaldo``.

If you want to find all tasks that you filed to the context "email", search
for ``@email``.

Similar to the search for phrases, you can filter out contexts or projects by
search for ``not:@context``, ``not:+project``, or use the abbreviation ``-@context``
or ``-+project`` respectively.


Priority
--------

Searching for priority is supported in two different ways: you can either
search for all tasks of a certain priority, eg. ``pri:a`` to find all tasks of
priority ``(A)``.
Or you can search for tasks that are more important or less important than a
certain priority level.

Say you want to see all tasks that are more important than priority ``(C)``, you
could search for ``moreimportant:c``. The keyword for “less important” is
``lessimportant``.

``moreimportant`` and ``lessimportant`` can be abbreviated with ``mi`` and ``li``
respectively.


Due date
--------

Searching for due dates can be done in two ways: either by exact due date or
by defining “before” or “after”.

If you just want to know what tasks are due on 2018-08-03, you can search for
``due:2018-08-03``.

But if you want to see all tasks that have a due date set *after* 2018-08-03,
you search for ``dueafter:2018-08-03``.

Similarly you can search with ``duebefore`` for tasks with a due date before a
certain date.

``dueafter`` and ``duebefore`` can be abbreviated with ``da`` and ``db`` respectively.

If you only want to see tasks that have a due date, you can search for
``due:yes``. ``due:no`` also works if you don’t want to see any due dates.

Searching for due dates supports `Relative Dates`_.


Creation date
-------------

The search for task with a certain creation date is similar to the search
query for due date: ``created:2017-11-01``.

You can also search for tasks created before a date with ``createdbefore`` (can
be abbreviated with ``crb``) and for tasks created after a date with
``createdafter`` (or short ``cra``).

To search for tasks created in the year 2008 you could search for
``createdafter:2007-12-31 createdbefore:2009-01-01`` or short ``cra:2007-12-31
crb:2009-01-01``.

Searching for creation dates supports `Relative Dates`_.


Completion date
---------------

The search for tasks with a certain completion date is pretty much identical
to the search for tasks with a certain creation date (see above), but using
the search phrases ``completed``, ``completedbefore`` (the short version is ``cob``), or
``completedafter`` (short form is ``coa``).

Searching for completion dates supports `Relative Dates`_.


Threshold or Tickler search
---------------------------

pter understand the the non-standard suggestion to use ``t:`` tags to
indicate that a task should not be active prior to the defined date.

If you still want to see all tasks, even those with a threshold in the future,
you can search for ``threshold:`` (or, short, ``t:``). See also the
`General`_ configuration option ``default-threshold``.

You can also pretend it’s a certain date in the future (eg. 2042-02-14) and
see what tasks become available then by searching for ``threshold:2042-02-14``.

``threshold`` can be abbreviated with ``t``. ``tickler`` is also a synonym for
``threshold``.

Searching for ``threshold`` supports `Relative Dates`_.


Task Identifier
---------------

You can search for task IDs with ``id:``. If you search for multiple
task IDs, all of these are searched for, not a task that has all given IDs.

You can also exclude tasks by ID from a search with ``not:id:`` or
``-id:``.


Sequence
--------

You can search for tasks that are supposed to follow directly or indirectly
other tasks by searching for ``after:taskid`` (``taskid`` should be the
``id`` of a task). Any task that is supposed to be completed after that
task, will be found.

If the configuration option ``hide-sequential`` is set to ``yes`` (the
default), tasks are hidden that have uncompleted preceding tasks (see
`General`_).

If you want to see all tasks, disregarding their declared sequence, you can
search for ``after:`` (without anything after the ``:``).


Task References
---------------

Tasks that refer to other tasks by any of the existing means (eg. ``ref:``
or ``after:``) can be found by searching for ``ref:``.

If you search using multiple references (eg. ``ref:4,5`` or ``ref:4
ref:5``) the task IDs are considered a logical ``or``.


Filename
--------

You can search for parts of a filename that a task belongs to with
``file:``. ``not:`` (or ``-``) can be used to exclude tasks that belong to
a certain file.

For example: ``file:todo.txt`` or ``-file:archive``.


Sorting
=======

Tasks can be sorted by passing ``sort:`` to the search. The properties of
tasks to sort by are separated by comma. The following properties can be
used for sorting:

  ``due_in``
    The number of days until the task is due, if there is a due
    date given.

  ``completed``
    Whether or not the task has been completed.

  ``priority``
    The priority of the task, if any.

  ``linenr``
    The line of the task in its todo.txt file

  ``file``
    The name of the todo.txt file the task is in.

  ``project``
    The first project (alphabetically sorted) of the task.

  ``context``
    The first context (alphabetically sorted) of the task.

The default sorting order is ``completed,due_in,priority,linenr`` and will
be assumed if no ``sort:`` is provided in the search.


Named Searches
==============

Search queries can become very long and it would be tedious to type them
again each time.

To get around it, you can save search queries and give each one a name. The
default keyboard shortcut to save a search is "s" and to load a search is
"l".

The named queries are stored in your configuration folder in the file
``~/.config/pter/searches.txt``.

Each line in that file is one saved search query in the form ``name = search
query``.

Here are some useful example search queries::

  Due this week = done:no duebefore:mon
  Done today = done:yes completed:0
  Open tasks = done:no


Task Templates
==============

When using todo.txt files for project planning it can be very tedious to type
due dates, time estimates project and context, tickler values, custom tags, 
etc for every task. Another scenario is if a certain type of task comes up on 
a regular basis, e.g. bugfixes.

To get around typing out the task every time, you can edit a file stored in your
configuration folder ``~/.config/pter/templates.txt``. The syntax is identical to
the ``searches.txt`` file. Alternatively an existing task can be saved as a template.

Each line in that file is one saved template in the form ``name = task template``.

The default keyboard shortcut to load a template is "L", to set no template, select
the ``None`` template. To save an existing task the default key is "S". Once a 
template has been selected any new task created will contain the template text when
editing starts.

Here are some useful example search queries::

  Paper revision = @paper +revision due:+7d estimate:
  Bug fix = (A) @programming due:+2d estimate: git:
  Project X = @work +projectx due:2021-04-11 estimate: 


Time Tracking
=============

pter can track the time you spend on a task. By default, type "t" to
start tracking. This will add a ``tracking:`` attribute with the current local
date and time to the task.

When you select that task again and type "t", the ``tracking:`` tag will be
removed and the time spent will be saved in the tag ``spent:`` as hours and
minutes.

If you start and stop tracking multiple times, the time in ``spent:`` will
accumulate accordingly. The smallest amount of time tracked is one minute.

This feature is non-standard for todo.txt but compatible with every other
implementation.


Delegating Tasks
================

The ``delegate`` function (on shortcut ``>`` (pter) or ``Ctrl+G`` (qpter)
by default) can be used to mark a task as delegated and trigger the
delegation action.

When delegating a task the configured marker is being added to the task
(configured by ``delegation-marker`` in the configuration file).

The delegation action is configured by setting the ``delegation-action`` in
the configuration file to ``mail-to``. In that case an attempt is made to
open your email program and start a new email. In case you defined a
``to:`` (configurable by defining ``delegation-to``) in your task
description, that will be used as the recipient for the email.


Unique Task Identifiers
=======================

Tasks can be given an identifier with the ``id:`` attribute. pter can
support you in creating unique IDs by creating a task with ``id:#auto`` or,
shorter, ``id:#``.

If you would like to group your tasks IDs, you can provide a prefix to the
id::

  Clean up the +garage id:clean3

If you now create a task with ``id:clean#`` or ``id:clean#auto``, the next
task will be given ``id:clean4``.

In case you want all your tasks to be created with a unique ID, have a look
at the configuration option ``auto-id`` (in section `General`_).

You can refer to other tasks using the attribute ``ref:`` following the id
of the task that you are referring to. This may also be a comma separated
list of tasks (much like ``after:``, see `Task Sequences`_).

You may use the ``show-related`` function (by default on the key ``r``) to
show the tasks that this task is referring to by means of ``ref:`` or
``after:``.


Task Sequences
==============

You can declare that a task is supposed to be done after another task has
been completed by setting the ``after:`` attribute to the preceding task.

By default, ie. with an empty search, any task that is declared to be
``after:`` some other preceding task will not be shown unless the preceding
task has been marked as done.

If you do not like this feature, you can disable it in the
``hide-sequential`` in the configuration file (see `General`_).


Examples
--------

These three tasks may exist::

  Buy potatoes @market id:1
  Make fries @kitchen id:2 after:1
  Eat fries for dinner after:2

This means that ``Make fries`` won’t show in the list of tasks until ``Buy
potatoes`` has been completed. Similarily ``Eat fries for dinner`` will not
show up until ``Make fries`` has been completed.

You can declare multiple ``after:`` attributes, or comma separate multiple
prerequisites to indicate that *all* preceding tasks must be completed
before a task may be shown::

  Buy oil id:1
  Buy potatoes id:2
  Buy plates id:3
  Make fries id:4 after:1,2
  Eat fries after:3 after:4

In this case ``Make fries`` will not show up until both ``Buy oil`` and
``Buy potatoes`` has been completed.

Similarly ``Eat fries`` requires both tasks, ``Make fries`` and ``Buy
plates``, to be completed.


Recurring Tasks
===============

Recurring (or repeating) tasks can be indicated by adding the ``rec:`` tag
and a `Relative Dates`_ specifier, like this::

  A weekly task rec:1w
  Do this again in 3 days rec:3d

By marking such a task as done, a new task will be added with the same
description, but a new creation date.

If you’d rather not have pter create new tasks every time, you can set the
``reuse-recurring`` option in the configuration file to ``yes``.

Recurring tasks usually only have meaning when a ``due:`` date is given,
but when there is no ``due:``, a ``t:`` will be used as a fallback if there
is any.

When completing such a task, pter can either create the follow-up task
based on the date of completion or based on the due date of the task. This
behaviour called the "recurring mode" which can be either

 - strict: the new due date is based on the old due date, or
 - normal: the new due date is based on the completion date.

To use strict mode, add a ``+`` before the time interval. For example you would
write ``rec:+2w`` for strict mode and ``rec:2w`` for normal mode.

An example. Given this task (starting June, you want to rearrange your
flowers in the living room every week)::

  2021-06-01 Rearrange flowers in the living room due:2021-06-05 rec:1w

In strict mode (``rec:+1w``), if you complete that task already on
2021-06-02, the next due date will be 2021-06-13 (old due date + 1 week).
But in normal mode (``rec:1w``) the new due date will be 2021-06-09 (date of
completion + 1 week).

If your recurring tasks has a due date and a threshold/tickler tag
(``t:``), upon completion the new task will also receive a ``t:`` tag with
the same relative time to the due date as the original task.

So, if you set up a due date 2021-06-05 and a threshold ``t:2021-06-04``
the new task will also have a threshold in such a way that the task is
hidden until one day before the due date.


Getting Things Done
===================

With pter you can apply the Getting Things Done method to a single todo.txt
file by using context and project tags, avoiding multiple lists.

For example, you could have a ``@in`` context for the list of all tasks
that are new. Now you can just search for ``@in`` (and save it as a named search) to find all new tasks.

To see all tasks that are on your "Next task" list, a good start is to
search for "``done:no not:@in``" (and save this search query, too).


Extensions to todo.txt
======================

Pter is fully compatible with the standard format, but also supports
the following extra key/value tags:

- ``after:4``, signifies that this entry can only be started once entry with ``id:4`` has been completed.
- ``due:2071-01-01``, defines a due date for this task.
- ``h:1``, hides a task.
- ``id:3``, allows you to assign a unique identifier to entries in the todo.txt, like ``3``. pter will accept when there non-unique IDs, but of course uniquely identifying entries will be tricky.
- ``rec:1w``, indicate that this task should be recurring in 1 week intervals.
- ``ref:6``, indicate that this task refers to the task with ``id:6``.  Comma-separated IDs are supported, like ``ref:13,9``.
- ``spent:5h3m``, pter can be used for time tracking and will store the time spent on a task in the ``spent`` attribute.
- ``t:2070-12-24``, the threshold tag can be used to hide before the given date has come.
- ``to:person``, when a task has been delegated (by using a delegation marker like ``@delegated``), ``to`` can be used to indicate to whom the task has been delegated. The option is configurable, see ``delegation-to`` above for details.
- ``tracking:``, a technical tag used for time tracking. It indicates that you started working on the task and wanted to do time tracking. The value is the date and time when you started working. Upon stopping tracking, the spent time will be stored in the ``spent`` tag.


Conforming to
=============

pter works with and uses the todo.txt file format and strictly adheres to the format
as described at http://todotxt.org/. Additional special key/value tags are
described in the previous section.


Bugs
====

Probably plenty. Please report your findings at `Codeberg <https://codeberg.org/vonshednob/pter>`_, `Github <https://github.com/vonshednob/pter>`_ or via email to the authors at `<https://vonshednob.cc/pter>`_.

