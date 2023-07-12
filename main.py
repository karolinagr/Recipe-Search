import requests
import json
import csv
import os


def clear_console():
    os.system('cls')


def recipe_search(ingredient, meal_type, vegan_option):
    YOUR_APP_KEY = '63886eeea6d415f1a5d1886980d48d2b'
    YOUR_APP_ID = 'f924f1ff'
    if vegan_option == "v":
        vegan_option = "vegan"
        url_ingredient = 'https://api.edamam.com/search?q={}&app_id={}&app_key={}&mealType={}&health={}'.format(
            ingredient, YOUR_APP_ID, YOUR_APP_KEY, meal_type, vegan_option)
    else:
        url_ingredient = 'https://api.edamam.com/search?q={}&app_id={}&app_key={}&mealType={}'.format(ingredient,
                                                                                                      YOUR_APP_ID,
                                                                                                      YOUR_APP_KEY,
                                                                                                      meal_type)
    response = requests.get(url_ingredient)
    recipes_response = response.json()
    return recipes_response['hits']


def run():
    ingredient = input("What kind of ingredient would you like to use? \n")
    meal_type = input(
        "What kind of meal type are you looking for: Breakfast, Dinner, Lunch, Snack, or Teatime? \n").lower()
    vegan_option = input("Are you looking for vegan 'v' or meat option 'm'? \n")
    recipes = recipe_search(ingredient, meal_type, vegan_option)
    new_recipes = sorted(recipes, key=lambda y: y['recipe']['calories'])

    for result in new_recipes:
        recipe_item = result['recipe']
        print(recipe_item['label'])
        print(recipe_item['calories'])
        print(recipe_item['uri'])
        print('')

    with open('recipes.txt', 'w+') as text_file:
        for recipe in new_recipes:
            recipe_str = json.dumps(recipe)
            text_file.write(f'{recipe_str}\n\n')
    with open('recipes.csv', 'w+', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        for recipe in new_recipes:
            recipe_info = recipe['recipe']
            recipe_name = recipe_info['label']
            recipe_url = recipe_info['url']
            recipe_ingredients = ', '.join(recipe_info['ingredientLines'])
            writer.writerow([recipe_name, recipe_url, recipe_ingredients])

    print("Recipes saved successfully.")
    clear_console()
    run()


print('Welcome in EDAMAM recipe search!\n')

run()
