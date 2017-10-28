import _pickle as pickle
from os import path
from nltk.tokenize import word_tokenize
from glob import glob

import config
import prep_data
from parse_ingredients import parse_ingredient_list

def tokenize_sentence(sentence):
    return ' '.join(list(filter(
        lambda x: x.lower() != "advertisement",
        word_tokenize(sentence))))

def recipe_is_complete(r):
    if ('title' not in r) or ('instructions' not in r):
        return False
    if (r['title'] is None) or (r['instructions'] is None):
        return False
    return True

def tokenize_recipes(recipes):
    tokenized = []
    N = len(recipes)
    for i, r in enumerate(recipes.values()):
        if recipe_is_complete(r):
            ingredients = '; '.join(parse_ingredient_list(r['ingredients'])) + '; '
            tokenized.append((
                tokenize_sentence(r['title']),
                tokenize_sentence(ingredients) + tokenize_sentence(r['instructions'])))
        if i % 10000 == 0:
            print('Tokenized {:,} / {:,} recipes'.format(i, N))
    return tuple(map(list, zip(*tokenized)))


def pretokenize():
    # Get folder path containing text files
    data = []
    for filename in glob(path.join(config.path_recipe_box_data, 'bbc_business/*.txt')):
        with open(filename) as f:
            d={}
            d['title'] = f.readline()
            d['ingredients'] = f.readline()
            d['instructions'] = f.read()
            data.append(d)
    return data
    

def tokenize_books(recipes):
    tokenized = []
    N = len(recipes)
    for i,r in enumerate(recipes):
        ingredients = '; '.join(tokenize_sentence(r['ingredients'])) + '; '
        tokenized.append((
            tokenize_sentence(r['title']),
            tokenize_sentence(ingredients) + tokenize_sentence(r['instructions'])))
        if i % 10000 == 0:
            print('Tokenized {:,} / {:,} recipes'.format(i, N))
    return tuple(map(list, zip(*tokenized)))





def pickle_recipes(recipes):
    # pickle to disk
    with open(path.join(config.path_data, 'tokens.pkl'), 'wb') as f:
        pickle.dump(recipes, f, 2)

def load_recipes():
    # pickle to disk
    with open(path.join(config.path_data, 'tokens.pkl'), 'rb') as f:
        recipes = pickle.load(f)
    return recipes

def main():
    #recipes = prep_data.load_recipes()    
    #text_sum_data = tokenize_recipes(recipes)

    data = pretokenize()
    text_sum_data = tokenize_books(data)
    pickle_recipes(text_sum_data)

if __name__ == '__main__':
    main()
