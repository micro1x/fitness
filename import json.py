import json 
import requests 

# Your Spoonacular API key

ingredients = []
ingredient_str = ','.join(ingredients)
recipes = []

# Construct the URL with the list of ingredients
url = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredient_str}&number=4&ignorePantry=True&apiKey={api_key}"

# Perform a GET request
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse JSON response
    data = response.json()
    print("JSON Response:")
#    print(json.dumps(data, indent = 4))
    for things in data:
        #print(json.dumps(things.get("missedIngredients"),indent = 4))
        for item in things.get("missedIngredients"):
            recipes.append(item.get("originalName"))
    for things in recipes:
        for item in things.split():
            if item.lower() == "recipes":
                recipes.remove(things)
    for i in range(len(recipes)):
        if len(recipes[i]) == 1:
            print(recipes[i])
            recipes.remove(recipes[i])
    print(recipes)
else:
    print("Error:", response.status_code)
    