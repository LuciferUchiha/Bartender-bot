# BartenderBot

## Table of Contents

* [About the Project](#about-the-project)
* [Installation](#installation)
* [Usage](#usage)
* [License](#license)
* [Contribute](#contribute)

## About The Project

This is a simple discord bot that was implemented with Python 3.8. The bot helps you 
with thirsty needs by providing you recipes for cocktails. It also allows you to search 
for cocktails by ingredients or name.


## Installation
1. Go to [discord developer portal](https://discord.com/developers/applications).
2. Create a new application.
3. Under the "Bot" tab on the left create a new bot.
4. Go to the "OAuth2" tab on the left.
5. Select bot from the "Scopes" options and select at least "Send Messages", 
"Manage Messages" and "Read Message History" permissions.
6. Copy the URL that was generated for you, paste it into your browser, and 
select your server from the dropdown options. The bot should now be added.
7. Clone the project and open it in your IDEA.<br>```git clone https://github.com/LuciferUchiha/BartenderBot.git```
8. Install the dependencies by running ```pip install -r requirements.txt``` in the project root.

## Usage:
The following words are correct keywords (\<KW\>): ```$bt, bartender and god```

#### Shortcuts
The following values are equivalent:

```
cocktails <=> -c
ingredients <=> -i
```

### Find cocktail
Will return any cocktail if it contains the search criteria. Multiple search criteria can be used by separating them with a space.
``` 
<KW> find cocktails <search criteria1> <search criteria2> ...
``` 

### Find ingredient 
Will return any ingredients if it contains the search criteria. Multiple search criteria can be used by separating them with a space.
``` 
<KW> find ingredients <search criteria1> <search criteria2> ...
``` 

### List all cocktails 
``` 
<KW> cocktails
```

### List all ingredients 
``` 
<KW> ingredients
```

### List all categories 
``` 
<KW> categories
```

### List all cocktails by category 
``` 
<KW> list <category>
```

### How many cocktails? 
``` 
<KW> count cocktails
```

### How many ingredients? 
``` 
<KW> count ingredients
```

### Cocktails with ingredient
Will return all cocktails that contain passed ingredients. Multiple ingredients can be used by separating them with a space.
``` 
<KW> with <ingredient> <ingredient2> ...
```

### How to make a cocktail 
``` 
<KW> recipe <cocktail>
```

## License
Distributed under the MIT License. See `LICENSE.md` for more information.

## Contribute
If you wish to contribute, see `CONTRIBUTING.md` for more information.
