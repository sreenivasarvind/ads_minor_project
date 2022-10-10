import hashlib
from collections import OrderedDict
import glob
import re
import matplotlib.pyplot as plt
from partitions import get_partition_size

class OHBF():
    def __init__(self, bit_size, number_of_mods = 3):
        self._bit_array = [0 for i in range(bit_size)]
        self._size_of_bit_array = bit_size
        self._number_of_mods = number_of_mods
        self._list_of_words_inserted=[]

    def _return_hash_values(self, text_to_hash):
        indexes_to_set = []
        hash_value = int.from_bytes(hashlib.md5(("{}".format(text_to_hash)).encode('UTF-8')).digest(), 'little')
        partition_beginning_index = []
        print("Before, {},{}".format(self._size_of_bit_array, self._number_of_mods))
        list_of_mod_values =  get_partition_size(self._size_of_bit_array, self._number_of_mods)
        print("after")
        print("\n")
        sum =0
        for indv_mod_value in list_of_mod_values:
            sum+= indv_mod_value
            partition_beginning_index.append(sum)
        print(list_of_mod_values, partition_beginning_index)
        print("\n\n")


        # Arvind - add your code to effectively split the bit array size into self._number_of_mods prime parts
        # for index_position in range(self._number_of_mods):
        #     if index_position != self._number_of_mods-1 and index_position==0:
        #         partition_beginning_index.append(int(self._size_of_bit_array/self._number_of_mods))
        #     elif index_position != self._number_of_mods-1:
        #         partition_beginning_index.append(partition_beginning_index[index_position-1]+int(self._size_of_bit_array/self._number_of_mods))

        # print(partition_beginning_index)
        list_of_mod_values = [partition_beginning_index[0]] + [partition_beginning_index[i+1]-partition_beginning_index[i] for i in range(len(partition_beginning_index)-1)]
        # print(list_of_mod_values)
        for index_position, indv_mod_value in enumerate(list_of_mod_values):
            # print(hash_value,indv_mod_value)
            hash_value_to_set = hash_value%indv_mod_value
            if index_position ==0:
                indexes_to_set.append(hash_value_to_set)
            else:
                indexes_to_set.append(partition_beginning_index[index_position-1]+hash_value_to_set)
        # print(indexes_to_set)
        return indexes_to_set

    def _set_bit_positions(self, bit_positions_to_set):
        for index_position in bit_positions_to_set:
            self._bit_array[index_position] = 1

    def _check_existence(self,word_to_search):
        for index in self._return_hash_values(word_to_search):
            if self._bit_array[index] == 0:
                return False
        return True

    def add_to_filer_and_set_bits(self, list_of_words_to_add_to_filter):
        self._list_of_words_inserted = list_of_words_to_add_to_filter
        for indv_word in list_of_words_to_add_to_filter:
            bit_positions_to_set = self._return_hash_values(indv_word)
            self._set_bit_positions(bit_positions_to_set)


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
            elif (search_prediction == False) and (word_to_search in self._list_of_words_inserted):
                wrong_predictions+=1
        # print("correct_predictions - {}\nfalse_positive - {}\nwrong_predictions - {}".format(correct_predictions,false_positive,wrong_predictions))
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

def plot_graph(x_axis_values, dictionary_of_filter_size_to_false_positives):
    for filter_size, y_axis_values in dictionary_of_filter_size_to_false_positives.items():
        # print(x_axis_values, y_axis_values)
        plt.plot(x_axis_values, y_axis_values, label = "filter size - {}".format(filter_size))
    plt.title('Comparison between number of hash functions and false positives in Bloom Filter')
    plt.xlabel('Number of modulo operations')
    plt.ylabel('Number of false positives')
    plt.legend()
    plt.show()

def main():
    list_of_x_axis_values = [i for i in range(2,9)]
    dictionary_of_filter_size_to_false_positives ={}
    filter_size_array = [i for i in range(10000,100000,10000)]
    # print(filter_size_array)
    for number_of_filter_size in filter_size_array:
        # print("*********************")
        x_axis_values = []
        y_axis_values = []
        for number_of_mods in range(2,2):
            # print("Bloom filter size - {}, Number of hashes - {}".format(filter_size, number_of_mods))
            sbf_object = OHBF(number_of_filter_size, number_of_mods)
            word_to_add_to_filter, words_to_search = get_words_to_add_to_bloom_filter()
            sbf_object.add_to_filer_and_set_bits(word_to_add_to_filter)
            search_results = sbf_object.check_if_list_of_words_contain(words_to_search)
            x_axis_values.append(number_of_mods)
            y_axis_values.append(sbf_object.print_summary(search_results))
            # print("\n\n")
        dictionary_of_filter_size_to_false_positives[number_of_filter_size] = y_axis_values
        
    print(list_of_x_axis_values, dictionary_of_filter_size_to_false_positives)
    plot_graph(list_of_x_axis_values, dictionary_of_filter_size_to_false_positives)
    print("*********************")

if __name__ == "__main__":
    main()