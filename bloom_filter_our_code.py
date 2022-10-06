import glob
import re
import hashlib
from collections import OrderedDict
import matplotlib.pyplot as plt


class SBF():
    def __init__(self, bit_size, number_of_hash_functions = 3):
        self._bit_array = [0 for i in range(bit_size)]
        self._size_of_bit_array = bit_size
        self._number_of_hash_functions = number_of_hash_functions
        self._list_of_words_inserted=[]

    def _return_hash_values(self, text_to_hash):
        dictionary_of_hash_functions = OrderedDict({
            'md5':int.from_bytes(hashlib.md5(("{}".format(text_to_hash)).encode('UTF-8')).digest(), 'little')%self._size_of_bit_array,
            'sha1':int.from_bytes(hashlib.sha1(("{}".format(text_to_hash)).encode('UTF-8')).digest(), 'little')%self._size_of_bit_array,
            'sha256':int.from_bytes(hashlib.sha256(("{}".format(text_to_hash)).encode('UTF-8')).digest(), 'little')%self._size_of_bit_array,
            'sha224':int.from_bytes(hashlib.sha224(("{}".format(text_to_hash)).encode('UTF-8')).digest(), 'little')%self._size_of_bit_array,
            'sha384':int.from_bytes(hashlib.sha384(("{}".format(text_to_hash)).encode('UTF-8')).digest(), 'little')%self._size_of_bit_array,
            'sha3_512':int.from_bytes(hashlib.sha3_512(("{}".format(text_to_hash)).encode('UTF-8')).digest(), 'little')%self._size_of_bit_array,
            'blake2b':int.from_bytes(hashlib.blake2b(("{}".format(text_to_hash)).encode('UTF-8')).digest(), 'little')%self._size_of_bit_array,
            'blake2s':int.from_bytes(hashlib.blake2s(("{}".format(text_to_hash)).encode('UTF-8')).digest(), 'little')%self._size_of_bit_array,
        })
        return dict(list(dictionary_of_hash_functions.items())[:self._number_of_hash_functions])
    
    def _set_bit_positions(self, bit_positions_to_set):
        for index_position in bit_positions_to_set:
            self._bit_array[index_position] = 1

    def _check_existence(self,word_to_search):
        for index in list(self._return_hash_values(word_to_search).values()):
            if self._bit_array[index] == 0:
                return False
        return True

    def add_to_filer_and_set_bits(self, list_of_words_to_add_to_filter):
        self._list_of_words_inserted = list_of_words_to_add_to_filter
        for indv_word in list_of_words_to_add_to_filter:
            bit_positions_to_set = self._return_hash_values(indv_word)
            self._set_bit_positions(list(bit_positions_to_set.values()))


    def check_if_list_of_words_contain(self, list_of_words_to_search):
        dictionary_of_searches_to_return = {}
        for indv_word_to_search in list_of_words_to_search:
            dictionary_of_searches_to_return[indv_word_to_search] = self._check_existence(indv_word_to_search)
        return dictionary_of_searches_to_return

    def print_summary(self, search_results):
        correct_predictions = 0
        false_positive = 0
        wrong_predictions = 0
        for word_to_search, search_prediction in search_results.items():
            if ((search_prediction == True) and (word_to_search in self._list_of_words_inserted)) or ((search_prediction==False) and (word_to_search not in self._list_of_words_inserted)):
                correct_predictions+=1
            elif (search_prediction == True) and (word_to_search not in self._list_of_words_inserted):
                false_positive+=1
            elif (search_prediction==False) and (word_to_search in self._list_of_words_inserted):
                wrong_predictions+=1
        print("correct_predictions - {}\nfalse_positive - {}\nwrong_predictions - {}".format(correct_predictions,false_positive,wrong_predictions))
        return false_positive


def get_words_to_add_to_bloom_filter():
    list_of_all_file_paths = glob.glob("{}/*".format("data"))
    list_of_all_file_paths = sorted(list_of_all_file_paths)
    word_dictionary_to_return = {}
    for file_path in list_of_all_file_paths:
        file_text = ''
        with open(file_path) as file_handler:
            file_text = file_handler.read()
        file_text=file_text.replace("\n"," ").lower()
        file_text = [re.sub(r"[^a-zA-Z]+", ' ', "{} ".format(k)) for k in file_text.split("\n")]
        temp_list = [i for i in file_text[0].split(" ") if i!='']
        list_to_push = list(set(temp_list))
        list_to_push.sort()
        word_dictionary_to_return[file_path] = list_to_push
    return  sum(list(word_dictionary_to_return.values())[1:],[]), list(word_dictionary_to_return.values())[0],

def plot_graph(x_axis_values, y_axis_values):
    plt.plot(x_axis_values, y_axis_values)
    plt.title('Bloom filter')
    plt.xlabel('Number of Hash functions')
    plt.ylabel('Number of false positives')
    plt.show()

def main():
    filter_size = 100000
    for number_of_filter_size in [10000, 50000, 100000, 1000000]:
        print("*********************")
        x_axis_values = []
        y_axis_values = []
        for number_of_hashes in range(1,9):
            print("Bloom filter size - {}, Number of hashes - {}".format(filter_size, number_of_hashes))
            sbf_object = SBF(number_of_filter_size, number_of_hashes)
            word_to_add_to_filter, words_to_search = get_words_to_add_to_bloom_filter()
            sbf_object.add_to_filer_and_set_bits(word_to_add_to_filter)
            search_results = sbf_object.check_if_list_of_words_contain(words_to_search)
            x_axis_values.append(number_of_hashes)
            y_axis_values.append(sbf_object.print_summary(search_results))
            print("\n\n")
        plot_graph(x_axis_values, y_axis_values)
        print("*********************")



if __name__ == "__main__":
    main()