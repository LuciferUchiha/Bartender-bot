import json

class Bartender:
    with open("recipes.json") as recipes_file:
        recipes = json.load(recipes_file)

    with open("ingredients.json") as ingredients_file:
        ingredients = json.load(ingredients_file)

    default = "This command does not exist, to see which commands exist type '$bt help'"
    error = "There was a problem with processing the command"

    def handle(self, message):
        # Remove KEYWORD
        argument = message.content[3:].strip().lower()
        answer = self.default
        if argument == "help":
            answer = "This will list all commands"
        elif argument == "ingredients":
            answer = self.get_all_ingredients()
        elif argument == "cocktails":
            answer = self.get_all_cocktails()
        elif argument.startswith("count"):
            parameters = self.remove_from_word(argument, "count").strip()
            answer = self.get_count(parameters)
        return answer

    def get_all_ingredients(self):
        answer = ""
        for key, value in self.ingredients.items():
            answer += key + " (" + str(value.get("abv")) + "%)\n"
        return answer

    def get_all_cocktails(self):
        answer = ""
        for cocktail in self.recipes:
            answer += cocktail.get("name") + "\n"
        return answer

    def remove_from_word(self, word, toRemove):
        return word[word.find(toRemove) + len(toRemove):]

    def get_count(self, parameters):
        print(parameters)
        answer = ""
        if parameters == "ingredients":
            answer = len(self.ingredients)
        elif parameters == "cocktails":
            answer = len(self.recipes)
        else:
            answer = self.error
        return answer

