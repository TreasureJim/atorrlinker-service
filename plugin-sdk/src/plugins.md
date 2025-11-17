# Location 
The plugins will be held in `PLUGIN_BASE_PATH` environment variable. Each plugin will have its own folder. 
Eg. For plugin named "elephant" it will be placed in `PLUGIN_BASE_PATH/elephant/main.py`.

# Requirements
If a python requires any extra packages it needs to be written in its `requirements.txt` file in the same folder as the plugins main python script.

# Plugin Advertising

Each plugin requires an advertising function named `atorrlinker_advertise` which atorrlinker will call to find information about which functions the plugin wants to advertise. The advertising function should return an `Advertising` instance which will contain a list of all the names of functions that can be called in the plugin. It will also contain the names and types of the arguments to the mentioned functions. 

Function names and arguments can be added to the `Advertising` instance by using the `search` decorator. 

Example

```python
advertiser = Advertiser()

def atorrlinker_advertise():
    return advertiser

@advertiser.search
def book_search(name: str, publish_year: int|None = None):
    pass
```
