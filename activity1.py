import sqlite3
import pandas as pd

conn=sqlite3.connect(':memory:')

conn.execute("CREATE TABLE recipe(recipe_id INTEGER PRIMARY KEY, recipe_name TEXT NOT NULL,prep_mins INTEGER NOT NULL)")

conn.execute("CREATE TABLE ingridients(ing_id INTEGER PRIMARY KEY, ing_name TEXT NOT NULL, ing_qty TEXT NOT NULL, recipe_id INTEGER NOT NULL, FOREIGN KEY(recipe_id) REFERENCES recipe(recipe_id))")

conn.execute("INSERT INTO recipe VALUES (1, 'Pasta', 30), (2, 'Pizza', 45), (3, 'Salad', 15), (4, 'Soup', 25), (5, 'Sandwich', 10)")
conn.execute("INSERT INTO ingridients VALUES (1, 'Pasta', '200g', 1), (2, 'Tomato Sauce', '100ml', 1), (3, 'Cheese', '50g', 2), (4, 'Dough', '300g', 2), (5, 'Lettuce', '100g', 3), (6, 'Tomato', '50g', 3), (7, 'Chicken Broth', '500ml', 4), (8, 'Carrots', '100g', 4), (9, 'Bread', '2 slices', 5), (10, 'Ham', '50g', 5)")

conn.commit()

print("Recipe Table:")
print(pd.read_sql_query("SELECT * FROM recipe", conn))
print()
print("Ingridients Table:")
print(pd.read_sql_query("SELECT * FROM ingridients", conn))
print()

col_alias=pd.read_sql("SELECT recipe_id AS ID, recipe_name AS Name, prep_mins AS Preparation_Time FROM recipe", conn)
print("Recipe Table with Column Aliases:")
print(col_alias)
print()

#subquery with IN
large_ingredients=pd.read_sql("SELECT * FROM ingridients WHERE recipe_id IN (SELECT recipe_id FROM recipe WHERE prep_mins > 20)", conn)
print("Ingridients for Recipes with Preparation Time > 20 minutes:")
print(large_ingredients)
print()

#subquery with =
quikest=pd.read_sql("SELECT * FROM ingridients WHERE recipe_id = (SELECT recipe_id FROM recipe WHERE prep_mins = (SELECT MIN(prep_mins) FROM recipe))", conn)
print("Ingridients for the Quickest Recipe:")
print(quikest)
print()

conn.close()
