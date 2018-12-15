Editing preference group trees
==============================

`zope.preference` has the concept of `preference group trees`_ and
`preference categories` to group preferences.

.. _`preference group trees`: http://pypi.python.org/pypi/zope.preference#preference-group-trees

If a `preference category` is displayed using `z3c.preference` automatically
all `preference groups` belonging to the category are rendered as groups in the
edit form (aka ``GroupForm``).

**Note:** Currently only the preference category and its *direct* children
are rendered in the tree.


Set up
------

At first we have to define some preference interfaces presenting the tree. In
this example we think of a web application with some areas:

  >>> import zope.interface
  >>> import zope.schema
  >>> class IGeneralSettings(zope.interface.Interface):
  ...     """General preferences"""
  ...
  ...     language = zope.schema.Choice(
  ...         title=u"Language",
  ...         description=u"The language which should be used for display.",
  ...         values=['German', 'English', 'Russian'],
  ...         default='German')

  >>> class IRSSSettings(zope.interface.Interface):
  ...     """Preferences for the RSS area of the application."""
  ...
  ...     number = zope.schema.Int(
  ...         title=u"Item count",
  ...         description=u"Maximum number of items in each feed.")

  >>> class ISearchSettings(zope.interface.Interface):
  ...     """Preferences for the search area of the application."""
  ...
  ...     store_searches = zope.schema.Bool(
  ...         title=u"Store searches?",
  ...         description=u"Should searches be kept for later use?",
  ...         default=True)

The interfaces must be registered for preferences:

  >>> from zope.configuration import xmlconfig
  >>> import zope.preference
  >>> context = xmlconfig.file('meta.zcml', zope.preference)

  >>> context = xmlconfig.string('''
  ...     <configure
  ...         xmlns="http://namespaces.zope.org/zope"
  ...         i18n_domain="test">
  ...
  ...       <preferenceGroup
  ...           id="app"
  ...           title="General Settings"
  ...           description="Settings for the whole app"
  ...           schema="z3c.preference.categories.IGeneralSettings"
  ...           category="true"
  ...           />
  ...
  ...       <preferenceGroup
  ...           id="app.search"
  ...           title="Search Settings"
  ...           schema="z3c.preference.categories.ISearchSettings"
  ...           category="false"
  ...           />
  ...
  ...       <preferenceGroup
  ...           id="app.rss"
  ...           title="RSS Settings"
  ...           description="Settings for the RSS feeds"
  ...           schema="z3c.preference.categories.IRSSSettings"
  ...           category="false"
  ...           />
  ...
  ...     </configure>''', context)


To access the forms a browser is needed, the user must be authorized as
the preferences are stored in the principal annotations:

>>> from zope.testbrowser.wsgi import Browser
>>> browser = Browser()
>>> browser.addHeader('Authorization', 'Basic mgr:mgrpw')

The form displays the titles and descriptions of the categories:

>>> browser.open('http://localhost/++preferences++/app')
>>> print(browser.contents)
<!DOCTYPE ...
...General Settings...
...Settings for the whole app...
...RSS Settings...
...Settings for the RSS feeds...
...Search Settings...

Editing preference group trees using browser
--------------------------------------------

There is a namespace to access the preferences. On the page a form is
displayed which shows the default values:

>>> browser.open('http://localhost/++preferences++/app')
>>> browser.getControl('Language').displayValue
['German']
>>> browser.getControl('Item count').value
''
>>> browser.getControl('yes').selected
True
>>> browser.getControl('no').selected
False

The values can be changed and submitting the form makes them persistent:

>>> browser.getControl('Language').displayValue = ['English']
>>> browser.getControl('Item count').value = '20'
>>> browser.getControl('no').click()
>>> browser.getControl('Apply').click()

After submitting the form gets displayed again and shows the changed values:

>>> 'Data successfully updated.' in browser.contents
True
>>> browser.getControl('Language').displayValue
['English']
>>> browser.getControl('Item count').value
'20'
>>> browser.getControl('no').selected
True
