from sys import argv

import numpy as np
import pandas as pd
from nltk.corpus import wordnet


class GlossaryReciter:
    # Initialize a GlossaryReciter
    # Input: glossary_filepath:filepath of glossary database
    # Output: an initialized GlossaryReciter
    def __init__(self, glossary_filepath):
        self.glossary_filepath = glossary_filepath
        self.very_clear_increment = 3

    # Create the csv file for storing word data and revised times
    # Input: None
    # Output: A file is created in the same directory as the code
    def create_csv(self):
        glossary_dict = {"word": [], "revised": []}
        glossary = pd.DataFrame(glossary_dict)
        glossary.to_csv(self.glossary_filepath, index=False)

    # Append words to the csv file containing words information
    # Input: None
    # Output: An updated csv file
    def keep_appending_words(self):
        try:
            glossary = pd.read_csv(self.glossary_filepath)
        except FileNotFoundError:
            if_exit = input(
                ''''{0}' not found. Exit or create a new file '{0}'?[e/c]'''.format(
                    self.glossary_filepath)).strip().lower()
            if if_exit == "c":
                self.create_csv()
                glossary = pd.read_csv(self.glossary_filepath)
            else:
                if if_exit != "e":
                    print("Illegal input! File '{}' is not created".format(self.glossary_filepath))
                return
        try:
            while True:
                word_to_add = input("word to add:").strip()
                if word_to_add not in glossary["word"].tolist():
                    if not wordnet.synsets(word_to_add):
                        still_add = input(
                            "'{}' is not in Princeton English Thesaurus. Are you sure to add?[y/n]".format(
                                word_to_add)).strip().lower()
                        if still_add != "y":
                            if still_add != "n":
                                print("Illegal input. '{}' is not added.".format(word_to_add))
                            else:
                                print("addition canceled.")
                            continue
                    glossary = pd.concat([glossary, pd.DataFrame({"word": [word_to_add], "revised": [0]})],
                                         ignore_index=True)
                    glossary.to_csv(self.glossary_filepath, index=False)
        except KeyboardInterrupt:
            return

    # Look up the word in the Princeton English Thesaurus
    # Input: A word
    # Output: the definition and examples provided by Princeton English Thesaurus
    def show_word_detail_and_synonyms(self, word):
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

    # Revising words by randomly choose a word from the words with the least revised times
    # Input:None
    # Output: the revised times for each word will be updated to the database
    def keep_revising_words(self):
        try:
            glossary = pd.read_csv(self.glossary_filepath)
        except FileNotFoundError:
            print("'{}' not found!".format(self.glossary_filepath))
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
                            self.show_word_detail_and_synonyms(word)
                            while True:
                                choice = input("\t1:next; 2:forgot; 3:very clear").strip()
                                if choice == "1":
                                    glossary.loc[idx, "revised"] += 1
                                    break
                                elif choice == "2":
                                    glossary.loc[idx, "revised"] = 0
                                    break
                                elif choice == "3":
                                    glossary.loc[idx, "revised"] += self.very_clear_increment
                                    break
                                else:
                                    print("\tUndefined choice!")
                            break
                        elif choice == "3":
                            glossary.loc[idx, "revised"] += self.very_clear_increment
                            break
                        else:
                            print("\tUndefined choice!")
                    glossary.sort_index().to_csv(self.glossary_filepath, index=False, columns=["word", "revised"])
        except KeyboardInterrupt:
            return

    # Delete a word from the database
    # Input: the word to delete
    # Output: the updated csv file
    def delete_word(self, word):
        try:
            glossary = pd.read_csv(self.glossary_filepath)
        except FileNotFoundError:
            print("'{}' not found!".format(self.glossary_filepath))
            return
        delete_index = glossary[glossary["word"] == word].index
        if len(delete_index) == 0:
            print("'{}' not found".format(word))
        else:
            for idx in delete_index:
                glossary.drop(idx, inplace=True)
            print("'{}' deleted successfully".format(word))
        glossary.to_csv(self.glossary_filepath, index=False)

    # Run the glossary reciter
    # Input: None
    # Output: None
    def run(self):
        while True:
            choice = input("\n1:add word; 2:revise word; 3:delete word; 4:exit").strip()
            if choice == "1":
                self.keep_appending_words()
            elif choice == "2":
                self.keep_revising_words()
            elif choice == "3":
                self.delete_word(input("word to delete:").strip())
            elif choice == "4":
                break
            else:
                print("Illegal input! Choose again")


# menu
# Input: csv filepath
if __name__ == "__main__":
    if len(argv) < 2:
        raise Exception("Too few arguments! Correct format: python {} <csv filepath>".format(argv[0]))
    reciter = GlossaryReciter(argv[1])
    reciter.run()
