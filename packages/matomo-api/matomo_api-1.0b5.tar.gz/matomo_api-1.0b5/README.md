[//]: # "see https://www.markdownguide.org/ for markdown coding"

# Python wrapper for the Matomo Reporting API

> #### Release warning for users of versions 1.0b4 and before
> 
> This version is not backward compatible with earlier versions since it breaks on how to 
> import and use it.
> Previous versions used the deprecated `from matomo_api import *` to literally enter all names 
> that Matomo uses in their API into the receiving namespace.
> That cluttered the receiving namespace more than was preferable and introduced naming 
> conflicts on identifiers such as `format` and `date`.  
> This version departs from this approach and uses the standard `import matomo_api` instead.
> This necessitates qualifying all API identifiers with the name of the module, 
> or an alias as set by using `import matomo_api as ma`.
> See the usage example below for further details.

## Introduction

This Python wrapper is based on (scraped) information from Matomo's [developer](https://developer.matomo.org)
and [glossary](https://glossary.matomo.org) sites, together with the contents of the 
`getReportMetadata` and `getGlossaryMetrics` API Requests.

The design goal for this package has been to provide API documentation from within the Python environment. 
Classes, methods and their respective docstrings have been used to facilitate this, 
thus enabling IDE popup/autocomplete options to aid in setting up an API Query.  
Names of the API Modules, Methods, and parameters in this package follow Matomo documentation.
Since this also holds for any capitalization, this diverts from Python naming conventions.  

## Note on terminology

Python and the Matomo API clash on some terminology. Most prone to raise confusion are the terms module and method.
To distinguish in which context these terms are used, they will be capitalized when referring to the Matomo API,
while lowercase will be used for a Python context. 

>_To add to the confusion, Matomo uses the term Module in two interpretations:_
>    
>* _Group of related API Methods, e.g. 'Actions' or 'Events'. In API Queries it is the first 
   part of the 'method' parameter, such as 'Actions' in method=Actions.getPageUrls._
>* _Handler of all http API Requests (request parameter is module=API) as opposed
   to e.g. the handler of the web-gui (module=CoreHome)._
>
>_In this documentation only the first interpretation is used: **a Module is a collection of API Methods.**_


## General usage instructions

-   Instantiate an object of the `MatomoApi` class, while specifying the server url and authorization token.

-   Select (and instantiate) an API Module by using the autocomplete/popup of your IDE on this `MatomoApi` object.
    
-   Select and use a specific API Method by again using the IDE autocomplete/popup features on the selected API Module.

-   The parameter/value combinations for the API Query can be selected by typing the parameter name, 
    reading potential docstrings and sub-selecting attributes or methods via IDE popups/autocompletes.
    Apply these parameters by bundling them via the union operator `|` and use this bundle (actually a library) as
    argument for the selected API Method.

-   Wherever columns need to be specified, select them using the `col` class and sub-select via dot-notation
    using (again) the IDE popup/autocomplete.


## Typical usage example:

```python
import matomo_api as ma

URL = 'https://matomoserver.somesite.int'
TOKEN = '0b1c64cb1de641e36de6bc9dd658d47ab'

api = ma.MatomoApi(URL, TOKEN)

pars = ma.format.json | ma.language.da | ma.translateColumnNames() \
       | ma.idSite.one_or_more(1) | ma.date.yesterday | ma.period.day \
       | ma.showColumns(ma.col.date, ma.col.label)

qry_result = api.Actions().getExitPageUrls(pars)
```

## Elaboration of usage example

### Instantiate the API

```python
api = ma.MatomoApi(URL, TOKEN)
```

Variable `api` is assigned an instance of the `MatomoApi` class with actual server url and token as arguments.
<br>Documentation of this class as popup:

![MatomoApi class popup](https://www.unander.nl/ma-rsc/b5_MatomoApi_class_popup.png)

### Select and set parameters

```python
pars = ma.format.json | ma.language.da | ma.translateColumnNames() \
       | ma.idSite.one_or_more(1) | ma.date.yesterday | ma.period.day \
       | ma.showColumns(ma.col.date, ma.col.label)
```

Variable `pars` is assigned a union of API parameters that build the Query.
All parameters are available as either Python class or Python function.

Autocompletion for an API parameter:

![formatparameter autocomplete](https://www.unander.nl/ma-rsc/b5_format_parameter_autocomplete.png)

In case the API parameter is represented by a Python class, values are set by selecting 
a class attribute or method.
The documentation guides this selection:

![format parameter popup](https://www.unander.nl/ma-rsc/b5_format_parameter_popup.png)

Autocomplete for setting the values of this `format` API parameter:

![format parameter attributes](https://www.unander.nl/ma-rsc/b5_format_parameter_attributes_autocomplete.png)

The `idSite` API parameter uses a class method to set multiple site id's:

![idSite parameter popup](https://www.unander.nl/ma-rsc/b5_idSite_parameter_popup.png)
<br>![](https://www.unander.nl/ma-rsc/b5_idSite_oneormore_method_popup.png)

Some API parameters require column specifications, e.g. the `showColumns` parameter:

![hideColumns parameter popup](https://www.unander.nl/ma-rsc/b5_showColumns_parameter_popup.png)

To specify these columns, use the `col` class:

![col class attributes autocomplete](https://www.unander.nl/ma-rsc/b5_col_class_attribute_autocomplete.png)

### Complete the Query

```python
qry_result = api.Actions().getExitPageUrls(pars)
```

The methods of the `MatomoApi` class represent Matomo API Modules.
Use method autocomplete on the `api` object to select the API Module:

![MatomoApi methods autocomplete](https://www.unander.nl/ma-rsc/b5_MatomoApi_methods_autocomplete.png)

Popup documentation of an API method:

![Actions method popup](https://www.unander.nl/ma-rsc/b5_Actions_method_popup.png)

Upon using a `MatomoApi` class method, an object is instantiated representing an API Module with all its Methods.
These API Methods can be selected via autocompletion of this 'Module' object:

![Actions module autocomplete](https://www.unander.nl/ma-rsc/b5_Actions_module_methods_autocomplete.png)

Most Methods of an API Module have extensive documentation.  

![getExitPageUrls method popup](https://www.unander.nl/ma-rsc/b5_Action_module_getExitPageUrls_method_popup.png)

Using a Method returns the result of the API Query as [Response](https://docs.python-requests.org/en/master/) object. 
