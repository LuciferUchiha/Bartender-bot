import json


class Bartender:
    with open("recipes.json") as recipes_file:
        recipes = json.load(recipes_file)

    with open("ingredients.json") as ingredients_file:
        ingredients = json.load(ingredients_file)

    ERROR = "There was a problem with processing the command"

    def handle(self, message):
        command_prefix = message.content.strip().lower()
        if self.starts_with_ingredients_prefix(command_prefix):
            return self.get_all_ingredients()
        elif self.starts_with_cocktails_prefix(command_prefix):
            return self.get_all_cocktails()
        elif command_prefix == "categories":
            return self.get_all_categories()
        elif command_prefix.startswith("count"):
            return self.get_count(command_prefix.removeprefix("count").strip())
        elif command_prefix.startswith("recipe"):
            return self.get_recipe(command_prefix.removeprefix("recipe").strip())
        elif command_prefix.startswith("list"):
            return self.get_cocktails_by_category(command_prefix.removeprefix("list").strip())
        elif command_prefix.startswith("find"):
            return self.find(command_prefix.removeprefix("find").strip())
        elif command_prefix.startswith("with"):
            return self.get_cocktails_with(command_prefix.removeprefix("with").strip())
        return "This command does not exist or you mistyped something"

    def get_all_ingredients(self):
        """Returns a string containing all of the ingredients the bot knows."""
        return "".join(f"{key} ({value.get('abv')}%)\n" for key, value in self.ingredients.items())

    def get_all_cocktails(self):
        """Returns a string containing the names of all of the cocktails the bot knows."""
        return "".join(f"{cocktail.get('name')}\n" for cocktail in self.recipes)

    def get_all_categories(self):
        """Returns a string containing all the cocktail categories the bot knows."""
        categories_list = sorted(set(str(cocktail.get("category")) for cocktail in self.recipes))
        return "".join(f"{category}\n" for category in categories_list)

    def get_count(self, param):
        """Returns the amount of ingredients or cocktails the bot knows."""
        if self.starts_with_ingredients_prefix(param):
            return len(self.ingredients)
        elif self.starts_with_cocktails_prefix(param):
            return len(self.recipes)

        return self.ERROR

    def get_recipe(self, param):
        """Returns the full recipe for the passed cocktail name."""
        for cocktail in self.recipes:
            if param == cocktail.get("name").lower():
                formatted_ingredients = self.get_formatted_ingredients(cocktail.get("ingredients"))
                garnish = self.get_garnish(cocktail)
                return f"__**{cocktail.get('name')}**__\n" \
                       f"**Ingredients:**\n" \
                       f"{formatted_ingredients}" \
                       f"{garnish}" \
                       f"**Preparation:**\n" \
                       f"{cocktail.get('preparation')} \n"
        return (f"There is no recipe for a cocktail called {param}. To see all cocktails with a recipe "
                "type '<KW> cocktails'")

    def get_formatted_ingredients(self, ingredients):
        """Returns a string of ingredients formatted as list for the cocktails including the special ones if it has
        any."""
        formatted_ingredients = ""
        special_ingredients = ""
        for ingredient in ingredients:
            if special_ingredient := ingredient.get("special") is not None:
                special_ingredients += f" - {special_ingredient}\n"
            else:
                formatted_ingredients += f" - {ingredient.get('amount')} {ingredient.get('unit')} " \
                                         f"{ingredient.get('ingredient')}\n"

        return formatted_ingredients + special_ingredients

    def get_garnish(self, cocktail):
        """Returns the garnish for the cocktail if it has one."""
        if garnish := cocktail.get('garnish') is not None:
            return f" **Garnish:**\n - {garnish}\n"

        return ""

    def get_cocktails_by_category(self, category):
        """Returns all cocktails in the given category."""
        answer = ""
        for cocktail in self.recipes:
            if category == str(cocktail.get("category")).lower():
                answer += f"{cocktail.get('name')}\n"

        return answer if len(answer) > 0 else f"There is no category called {category} or it contains no cocktails"

    def find(self, param):
        """Returns all ingredients or cocktails containing the criteria in the parameter separated by commas."""
        answer = ""
        if self.starts_with_cocktails_prefix(param):
            param = self.remove_cocktails_prefix(param)
            for criteria in param.strip().split(","):
                criteria = criteria.strip()
                answer += f"**Criteria: {criteria}**\n"
                answer += self.get_cocktails_containing(criteria)
        elif self.starts_with_ingredients_prefix(param):
            param = self.remove_ingredients_prefix(param)
            for criteria in param.strip().split(","):
                criteria = criteria.strip()
                answer += f"**Criteria: {criteria}**\n"
                answer += self.get_ingredients_containing(criteria)

        return answer

    def get_cocktails_containing(self, criteria):
        """Returns all cocktails containing the criteria in its name."""
        answer = ""
        for cocktail in self.recipes:
            if criteria in str(cocktail.get("name")).lower():
                answer += f"{cocktail.get('name')}\n"

        return answer if len(answer) > 0 else "Nothing was found matching your criteria"

    def get_ingredients_containing(self, criteria):
        """Returns all ingredients containing the criteria in its name."""
        answer = ""
        for ingredient in self.ingredients.keys():
            if criteria in ingredient.lower():
                answer += f"{ingredient}\n"

        return answer if len(answer) > 0 else "Nothing was found matching your criteria"

    def get_cocktails_with(self, param):
        """Returns all cocktails containing the searched for ingredients in the parameter separated by commas."""
        answer = ""
        for ingredient in param.strip().split(","):
            for cocktail in self.recipes:
                cocktail_ingredients = cocktail.get("ingredients")
                answer += self.does_cocktail_contain(cocktail, cocktail_ingredients, ingredient.strip())

        return answer if len(answer) > 0 else "Nothing was found matching your criteria"

    def does_cocktail_contain(self, cocktail, cocktail_ingredients, ingredient):
        """Returns the name of the cocktail if the cocktail contains the searched for ingredient."""
        for cocktail_ingredient in cocktail_ingredients:
            current_ingredient = cocktail_ingredient.get("ingredient")
            if current_ingredient is not None and ingredient in current_ingredient.lower():
                return f"{cocktail.get('name')}\n"

        return ""

    @staticmethod
    def starts_with_cocktails_prefix(param):
        """Returns true if passed string starts with the cocktails prefix (-c or cocktails)."""
        return param.startswith("-c") or param.startswith("cocktails")

    @staticmethod
    def remove_cocktails_prefix(param):
        """Returns a string with the cocktails prefix (-c or cocktails) removed. If the string does not start with
        the cocktails prefix it will return the original string."""
        if param.startswith("-c"):
            param = param.removeprefix("-c")
        elif param.startswith("cocktails"):
            param = param.removeprefix("cocktails")
        return param

    @staticmethod
    def starts_with_ingredients_prefix(param):
        """Returns true if passed string starts with the ingredient prefix (-i or ingredients)."""
        return param.startswith("-i") or param.startswith("ingredients")

    @staticmethod
    def remove_ingredients_prefix(param):
        """Returns a string with the ingredient prefix (-i or ingredients) removed. If the string does not start with
        the ingredients prefix it will return the original string."""
        if param.startswith("-i"):
            param = param.removeprefix("-i")
        elif param.startswith("ingredients"):
            param = param.removeprefix("ingredients")
        return param
