import numpy as np
import pandas as pd
from nltk.corpus import wordnet

glossary_filename = "New_GRE_Buddhist_Glossary.csv"
increment_of_very_clear = 3


def create_csv():
    glossary_dict = {"word": [], "revised": []}
    glossary = pd.DataFrame(glossary_dict)
    glossary.to_csv(glossary_filename, index=False)


def keep_appending_words():
    try:
        glossary = pd.read_csv(glossary_filename)
    except FileNotFoundError:
        if_exit = input(
            ''''{0}' not found. Exit or create a new file '{0}'?[e/c]'''.format(glossary_filename)).strip().lower()
        if if_exit == "c":
            create_csv()
            glossary = pd.read_csv(glossary_filename)
        else:
            if if_exit != "e":
                print("Illegal input! File '{}' is not created".format(glossary_filename))
            return
    try:
        while True:
            word_to_add = input("word to add:").strip()
            if word_to_add not in glossary["word"].tolist():
                if not wordnet.synsets(word_to_add):
                    still_add = input("'{}' is not in Princeton English Thesaurus. Are you sure to add?[y/n]".format(
                        word_to_add)).strip().lower()
                    if still_add != "y":
                        if still_add != "n":
                            print("Illegal input. '{}' is not added.".format(word_to_add))
                        else:
                            print("addition canceled.")
                        continue
                glossary = pd.concat([glossary, pd.DataFrame({"word": [word_to_add], "revised": [0]})],
                                     ignore_index=True)
                glossary.to_csv(glossary_filename, index=False)
    except KeyboardInterrupt:
        return


def show_word_detail_and_synonyms(word):
    syns = wordnet.synsets(word)
    if not syns:
        print("\t'{}' is not in Princeton English Thesaurus!".format(word))
        return
    for syn in syns:
        print("\t" + syn.name())
        print("\t" * 2 + "definition:", syn.definition())
        print("\t" * 2 + "examples:")
        for example in syn.examples():
            print("\t" * 3 + example)


def keep_revising_words():
    try:
        glossary = pd.read_csv(glossary_filename)
    except FileNotFoundError:
        print("'{}' not found!".format(glossary_filename))
        return
    try:
        glossary_size = len(glossary)
        glossary = pd.concat([glossary, pd.DataFrame({"rand_num": [0] * glossary_size})], axis=1)
        while True:
            glossary.loc[:, "rand_num"] = np.random.permutation(glossary_size)
            glossary.sort_values(by=["revised", "rand_num"], inplace=True)
            words_indexes = glossary[glossary["revised"] == glossary.iloc[0]["revised"]].index
            for idx in words_indexes:
                word = glossary.loc[idx, "word"]
                print(word)
                while True:
                    choice = input("\t1:next; 2:show word details and synonyms; 3:very clear").strip()
                    if choice == "1":
                        glossary.loc[idx, "revised"] += 1
                        break
                    elif choice == "2":
                        show_word_detail_and_synonyms(word)
                        while True:
                            choice = input("\t1:next; 2:forgot; 3:very clear").strip()
                            if choice == "1":
                                glossary.loc[idx, "revised"] += 1
                                break
                            elif choice == "2":
                                glossary.loc[idx, "revised"] = 0
                                break
                            elif choice == "3":
                                glossary.loc[idx, "revised"] += increment_of_very_clear
                                break
                            else:
                                print("\tUndefined choice!")
                        break
                    elif choice == "3":
                        glossary.loc[idx, "revised"] += increment_of_very_clear
                        break
                    else:
                        print("\tUndefined choice!")
                glossary.sort_index().to_csv(glossary_filename, index=False, columns=["word", "revised"])
    except KeyboardInterrupt:
        return


def delete_word(word):
    try:
        glossary = pd.read_csv(glossary_filename)
    except FileNotFoundError:
        print("'{}' not found!".format(glossary_filename))
        return
    delete_index = glossary[glossary["word"] == word].index
    if len(delete_index) == 0:
        print("'{}' not found".format(word))
    else:
        for idx in delete_index:
            glossary.drop(idx, inplace=True)
        print("'{}' deleted successfully".format(word))
    glossary.to_csv(glossary_filename, index=False)


if __name__ == "__main__":
    while True:
        choice = input("\n1:add word; 2:revise word; 3:delete word; 4:exit").strip()
        if choice == "1":
            keep_appending_words()
        elif choice == "2":
            keep_revising_words()
        elif choice == "3":
            delete_word(input("word to delete:").strip())
        elif choice == "4":
            break
        else:
            print("Illegal input! Choose again")
