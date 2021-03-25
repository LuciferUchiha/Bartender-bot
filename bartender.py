import json


class Bartender:
    with open("recipes.json") as recipes_file:
        recipes = json.load(recipes_file)

    with open("ingredients.json") as ingredients_file:
        ingredients = json.load(ingredients_file)

    def handle(self, message):
        switcher = {
            "help": self.help,
            "ingredients": self.list_all_ingredients,
            "cocktails": self.list_all_cocktails
        }
        print(message)
        argument = message.content[3:].strip()
        func = switcher.get(argument, "This command does not exist, to see which commands exist type '$bt help'")
        # Execute the function
        return func()

    def help(self):
        # TODO write a list of all commands
        return "This will list all commands"

    def list_all_ingredients(self):
        string = ""
        for key, value in self.ingredients.items():
            string += key + " (" + str(value.get("abv")) + "%)\n"
        return string

    def list_all_cocktails(self):
        string = ""
        for cocktail in self.recipes:
            string += cocktail.get("name") + "\n"
        return string
