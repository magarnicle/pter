"""Common constants for both ncurses and qiui"""
import pathlib
import os
import re

try:
    from xdg import BaseDirectory
except ImportError:
    BaseDirectory = None


PROGRAMNAME = 'pter'
QTPROGRAMNAME = 'qpter'
HERE = pathlib.Path(os.path.abspath(__file__)).parent
HOME = pathlib.Path.home()
CONFIGDIR = HOME / ".config" / PROGRAMNAME
CONFIGFILE = HOME / ".config" / PROGRAMNAME / (PROGRAMNAME + ".conf")
CACHEDIR = HOME / ".cache" / PROGRAMNAME
CACHEFILE = CACHEDIR / (PROGRAMNAME + ".settings")

if BaseDirectory is not None:
    CONFIGDIR = pathlib.Path(BaseDirectory.save_config_path(PROGRAMNAME) or CONFIGDIR)
    CONFIGFILE = CONFIGDIR / (PROGRAMNAME + ".conf")
    CACHEDIR = pathlib.Path(BaseDirectory.save_cache_path(PROGRAMNAME) or CACHEDIR)
    CACHEFILE = CACHEDIR / (PROGRAMNAME + ".settings")

SEARCHES_FILE = CONFIGDIR / "searches.txt"
TEMPLATES_FILE = CONFIGDIR / "templates.txt"
LOGFILE = CACHEDIR / (PROGRAMNAME + ".log")
DEFAULT_TRASHFILE = CONFIGDIR / "trash.txt"

URL_RE = re.compile(r'([A-Za-z][A-Za-z0-9+\-.]*)://([^ ]+)')

DEFAULT_TASK_FORMAT = '{multi-selection}{selection: >} {nr: >} {done} {tracking }{due }{(pri) }{description}'
ATTR_TRACKING = 'tracking'
ATTR_T = 't'
ATTR_DUE = 'due'
ATTR_PRI = 'pri'
ATTR_ID = 'id'

DELEGATE_ACTION_NONE = 'none'
DELEGATE_ACTION_MAIL = 'mail-to'
DELEGATE_ACTIONS = (DELEGATE_ACTION_NONE, DELEGATE_ACTION_MAIL)

DELETE_OPTION_DISABLED = 'disabled'
DELETE_OPTION_TRASH = 'trash'
DELETE_OPTION_PERMANENT = 'permanent'
DELETE_OPTIONS = (DELETE_OPTION_DISABLED, DELETE_OPTION_TRASH, DELETE_OPTION_PERMANENT)

DEFAULT_SORT_ORDER = 'completed,due_in,priority,linenr'
DEFAULT_INFO_TIMEOUT = 5

SETTING_GROUP_GENERAL = 'General'
SETTING_GROUP_SYMBOLS = 'Symbols'
SETTING_GROUP_COLORS = 'Colors'
SETTING_GROUP_HIGHLIGHT = 'Highlight'
SETTING_GROUP_KEYS = 'Keys'
SETTING_GROUP_EDITORKEYS = 'Editor:Keys'
SETTING_GROUP_GUICOLORS = 'GUI:Colors'
SETTING_GROUP_GUIHIGHLIGHT = 'GUI:Highlight'
SETTING_GROUP_GUIKEYS = 'GUI:Keys'
SETTING_GROUP_GUI = 'GUI'
SETTING_GROUP_INCLUDE = 'Include'
SETTING_HUMAN_DATES = 'human-friendly-dates'
SETTING_USE_COMPLETION = 'use-completion'
SETTING_PROTOCOLS = 'protocols'
SETTING_DELEG_MARKER = 'delegation-marker'
SETTING_DELEG_ACTION = 'delegation-action'
SETTING_DELEG_TO = 'delegation-to'
SETTING_DEFAULT_THRESHOLD = 'default-threshold'
SETTING_EXT_EDITOR = 'editor'
SETTING_TAB_CYCLES = 'tab-cycles'
SETTING_ADD_CREATED = 'add-creation-date'
SETTING_SEARCH_CASE_SENSITIVE = 'search-case-sensitive'
SETTING_SAFE_SAVE = 'safe-save'
SETTING_SCROLL_MARGIN = 'scroll-margin'
SETTING_SHOW_NUMBERS = 'show-numbers'
SETTING_USE_COLORS = 'use-colors'
SETTING_TASK_FORMAT = 'task-format'
SETTING_REUSE_RECURRING = 'reuse-recurring'
SETTING_CLEAR_CONTEXT = 'clear-contexts'
SETTING_RELATED_SHOW_SELF = 'related-show-self'
SETTING_FONT = 'font'
SETTING_FONTSIZE = 'font-size'
SETTING_SINGLE_INSTANCE = 'single-instance'
SETTING_CREATE_FROM_SEARCH = 'create-from-search'
SETTING_AUTO_ID = 'auto-id'
SETTING_HIDE_SEQUENTIAL = 'hide-sequential'
SETTING_CLICKABLE = 'clickable'
SETTING_DAILY_RELOAD = 'daily-reload'
SETTING_DELETE_IS = 'delete-is'
SETTING_TRASHFILE = 'trash-file'
SETTING_INFO_TIMEOUT = 'info-timeout'
SETTING_ICON_SELECTION = 'selection'
SETTING_ICON_MULTI_SELECTION = 'multi-selection'
SETTING_ICON_NOT_DONE = 'not-done'
SETTING_ICON_DONE = 'done'
SETTING_ICON_OVERFLOW_LEFT = 'overflow-left'
SETTING_ICON_OVERFLOW_RIGHT = 'overflow-right'
SETTING_ICON_OVERDUE = 'overdue'
SETTING_ICON_DUE_TODAY = 'due-today'
SETTING_ICON_DUE_TOMORROW = 'due-tomorrow'
SETTING_ICON_TRACKING = 'tracking'
SETTING_COL_NORMAL = 'normal'
SETTING_COL_PRI_A = 'pri-a'
SETTING_COL_PRI_B = 'pri-b'
SETTING_COL_PRI_C = 'pri-c'
SETTING_COL_INACTIVE = 'inactive'
SETTING_COL_CONTEXT = 'context'
SETTING_COL_PROJECT = 'project'
SETTING_COL_ERROR = 'error'
SETTING_COL_HELP_TEXT = 'help'
SETTING_COL_HELP_KEY = 'help-key'
SETTING_COL_OVERFLOW = 'overflow'
SETTING_COL_OVERDUE = 'overdue'
SETTING_COL_DUE_TODAY = 'due-today'
SETTING_COL_DUE_TOMORROW = 'due-tomorrow'
SETTING_COL_TRACKING = 'tracking'
SETTING_COL_URL = 'url'
SETTING_GK_QUIT = 'quit'
SETTING_GK_NEW = 'new'
SETTING_GK_NEW_REF = 'new-related'
SETTING_GK_NEW_AFTER = 'new-subsequent'
SETTING_GK_EDIT = 'edit'
SETTING_GK_OPEN_FILE = 'open-file'
SETTING_GK_TOGGLE_DONE = 'toggle-done'
SETTING_GK_DELETE_TASK = 'delete-task'
SETTING_GK_SEARCH = 'search'
SETTING_GK_TOGGLE_TRACKING = 'toggle-tracking'
SETTING_GK_OPEN_MANUAL = 'open-manual'
SETTING_GK_NAMED_SEARCHES = 'named-searches'
SETTING_GK_FOCUS_TASKS = 'focus-tasks'
SETTING_GK_TOGGLE_HIDDEN = 'toggle-hidden'
SETTING_GK_TOGGLE_DARK = 'toggle-dark-mode'
SETTING_GK_DELEGATE = 'delegate'
SETTING_GK_INC_PRIO = 'prio-up'
SETTING_GK_DEC_PRIO = 'prio-down'
SETTING_GK_REM_PRIO = 'prio-none'
SETTING_GK_SET_PRIOA = 'prio-a'
SETTING_GK_SET_PRIOB = 'prio-b'
SETTING_GK_SET_PRIOC = 'prio-c'
SETTING_GK_SET_PRIOD = 'prio-d'
SETTING_GK_MULTI_SELECT = 'multi-select'

TF_SELECTION = 'selection'
TF_MULTI_SELECTION = 'multi-selection'
TF_NUMBER = 'nr'
TF_DESCRIPTION = 'description'
TF_DONE = 'done'
TF_TRACKING = 'tracking'
TF_DUE = 'due'
TF_ALL = 'all'
TF_DUEDAYS = 'duedays'
TF_PRIORITY = 'pri'
TF_CREATED = 'created'
TF_COMPLETED = 'completed'
TF_AGE = 'age'
