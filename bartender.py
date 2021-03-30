import json


class Bartender:
    with open("recipes.json") as recipes_file:
        recipes = json.load(recipes_file)

    with open("ingredients.json") as ingredients_file:
        ingredients = json.load(ingredients_file)

    default = "This command does not exist, to see which commands exist type '$bt help'"
    error = "There was a problem with processing the command"

    def handle(self, message):
        argument = message.content.strip().lower()
        answer = self.default
        if argument == "help":
            answer = "This will list all commands"
        elif argument == "ingredients":
            answer = self.get_all_ingredients()
        elif argument == "cocktails":
            answer = self.get_all_cocktails()
        elif argument == "categories":
            answer = self.get_all_categories()
        elif argument.startswith("count"):
            parameters = self.remove_from_word(argument, "count").strip()
            answer = self.get_count(parameters)
        elif argument.startswith("recipe"):
            parameters = self.remove_from_word(argument, "recipe").strip()
            answer = self.get_recipe(parameters)
        elif argument.startswith("list"):
            parameters = self.remove_from_word(argument, "list").strip()
            answer = self.get_cocktails_by_category(parameters)
        elif argument.startswith("find"):
            parameters = self.remove_from_word(argument, "find").strip()
            answer = self.find(parameters)
        return answer

    def get_all_ingredients(self):
        answer = ""
        for key, value in self.ingredients.items():
            answer += f"{key} ({value.get('abv')}%)\n"
        return answer

    def get_all_cocktails(self):
        answer = ""
        for cocktail in self.recipes:
            answer += f"{cocktail.get('name')}\n"
        return answer

    def get_all_categories(self):
        answer = ""
        categories_list = []
        for cocktail in self.recipes:
            categories_list.append(cocktail.get("category"))

        # Remove duplicates
        categories_list = list(set(categories_list))
        categories_list.sort(key=str)
        for category in categories_list:
            answer += f"{category}\n"
        return answer

    def remove_from_word(self, word, toRemove):
        return word[word.find(toRemove) + len(toRemove):]

    def get_count(self, parameters):
        answer = self.error
        if parameters == "ingredients":
            answer = len(self.ingredients)
        elif parameters == "cocktails":
            answer = len(self.recipes)

        return answer

    def get_recipe(self, parameter):
        answer = f"There is no recipe for a cocktail called {parameter}. To see all cocktails with a recipe " \
                 f"type '$bt cocktails'"
        for cocktail in self.recipes:
            formatted_ingredients = self.get_formatted_ingredients(cocktail.get("ingredients"))
            garnish = self.get_garnisch(cocktail)
            if parameter == cocktail.get("name").lower():
                return f"__**{cocktail.get('name')}**__\n" \
                       f"**Ingriedients:**\n" \
                       f"{formatted_ingredients}" \
                       f"{garnish}" \
                       f"**Preparation:**\n" \
                       f"{cocktail.get('preparation')} \n"
        return answer

    def get_formatted_ingredients(self, ingredients):
        formatted_ingredients = ""
        special_ingredients = ""
        for ingredient in ingredients:
            if ingredient.get("special") is not None:
                special_ingredients += f" - {ingredient.get('special')}\n"
            else:
                formatted_ingredients += f" - {ingredient.get('amount')} {ingredient.get('unit')} {ingredient.get('ingredient')} "
                if ingredient.get("label") is not None:
                    f"({ingredient.get('label')})"
                formatted_ingredients += "\n"

        return formatted_ingredients + special_ingredients

    def get_garnisch(self, cocktail):
        if cocktail.get("garnish") is not None:
            return f"**Garnish:**\n" \
                   f" - {cocktail.get('garnish')} \n"
        else:
            return ""

    def get_cocktails_by_category(self, category):
        answer = ""
        for cocktail in self.recipes:
            if category == str(cocktail.get("category")).lower():
                answer += f"{cocktail.get('name')}\n"

        return answer

    def starts_with_cocktails_prefix(self, string):
        return string.startswith("-c") or string.startswith("cocktails")

    def remove_cocktails_prefix(self, string):
        if string.startswith("-c"):
            string = string.removeprefix("-c")
        elif string.startswith("cocktails"):
            string = string.removeprefix("cocktails")
        return string

    def starts_with_ingredients_prefix(self, string):
        return string.startswith("-i") or string.startswith("ingredients")

    def remove_ingredients_prefix(self, string):
        if string.startswith("-i"):
            string = string.removeprefix("-i")
        elif string.startswith("ingredients"):
            string = string.removeprefix("ingredients")
        return string

    def find(self, string):
        answer = ""
        if self.starts_with_cocktails_prefix(string):
            string = self.remove_cocktails_prefix(string)
            for criteria in string.strip().split():
                answer += f"**Criteria: {criteria}**\n"
                answer += self.get_cocktails_containing(criteria)
        elif self.starts_with_ingredients_prefix(string):
            string = self.remove_ingredients_prefix(string)
            for criteria in string.strip().split():
                answer += f"**Criteria: {criteria}**\n"
                answer += self.get_ingredients_containing(criteria)

        return answer

    def get_cocktails_containing(self, criteria):
        answer = ""
        for cocktail in self.recipes:
            if criteria in str(cocktail.get("name")).lower():
                answer += f"{cocktail.get('name')}\n"

        return answer

    def get_ingredients_containing(self, criteria):
        answer = ""
        for ingredient in self.ingredients.keys():
            if criteria in ingredient.lower():
                answer += f"{ingredient}\n"

        return answer
