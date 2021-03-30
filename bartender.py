import json


class Bartender:
    with open("recipes.json") as recipes_file:
        recipes = json.load(recipes_file)

    with open("ingredients.json") as ingredients_file:
        ingredients = json.load(ingredients_file)

    default = "This command does not exist, to see which commands exist type '$bt help'"
    error = "There was a problem with processing the command"

    def handle(self, message):
        command_prefix = message.content.strip().lower()
        answer = self.default
        if command_prefix == "help":
            answer = "This will list all commands"
        elif self.starts_with_ingredients_prefix(command_prefix):
            answer = self.get_all_ingredients()
        elif self.starts_with_cocktails_prefix(command_prefix):
            answer = self.get_all_cocktails()
        elif command_prefix == "categories":
            answer = self.get_all_categories()
        elif command_prefix.startswith("count"):
            answer = self.get_count(command_prefix.removeprefix("count").strip())
        elif command_prefix.startswith("recipe"):
            answer = self.get_recipe(command_prefix.removeprefix("recipe").strip())
        elif command_prefix.startswith("list"):
            answer = self.get_cocktails_by_category(command_prefix.removeprefix("list").strip())
        elif command_prefix.startswith("find"):
            answer = self.find(command_prefix.removeprefix("find").strip)
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

    def get_count(self, param):
        answer = self.error
        if self.starts_with_ingredients_prefix(param):
            answer = len(self.ingredients)
        elif self.starts_with_cocktails_prefix(param):
            answer = len(self.recipes)

        return answer

    def get_recipe(self, param):
        answer = f"There is no recipe for a cocktail called {param}. To see all cocktails with a recipe " \
                 f"type '$bt cocktails'"
        for cocktail in self.recipes:
            if param == cocktail.get("name").lower():
                formatted_ingredients = self.get_formatted_ingredients(cocktail.get("ingredients"))
                garnish = self.get_garnisch(cocktail)
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

    def starts_with_cocktails_prefix(self, param):
        return param.startswith("-c") or param.startswith("cocktails")

    def remove_cocktails_prefix(self, param):
        if param.startswith("-c"):
            param = param.removeprefix("-c")
        elif param.startswith("cocktails"):
            param = param.removeprefix("cocktails")
        return param

    def starts_with_ingredients_prefix(self, param):
        return param.startswith("-i") or param.startswith("ingredients")

    def remove_ingredients_prefix(self, param):
        if param.startswith("-i"):
            param = param.removeprefix("-i")
        elif param.startswith("ingredients"):
            param = param.removeprefix("ingredients")
        return param

    def find(self, param):
        answer = ""
        if self.starts_with_cocktails_prefix(param):
            param = self.remove_cocktails_prefix(param)
            for criteria in param.strip().split():
                answer += f"**Criteria: {criteria}**\n"
                answer += self.get_cocktails_containing(criteria)
        elif self.starts_with_ingredients_prefix(param):
            param = self.remove_ingredients_prefix(param)
            for criteria in param.strip().split():
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
