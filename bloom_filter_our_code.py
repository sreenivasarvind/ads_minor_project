import glob
import re
import matplotlib.pyplot as plt
from sbf import SBF
from ohbf import OHBF

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

def plot_graph(x_axis_values, dictionary_of_filter_size_to_false_positives,type_of_graph="hash"):
    for filter_size, y_axis_values in dictionary_of_filter_size_to_false_positives.items():
        plt.plot(x_axis_values, y_axis_values, label = "filter size - {}".format(filter_size))
    plt.title('Comparison between number of hash functions and false positives in {} Bloom Filter'.format("Standard" if type_of_graph=="hash" else "One Hash"))
    plt.xlabel('Number of {} functions'.format(type_of_graph))
    plt.ylabel('Number of false positives')
    plt.legend()
    plt.show()

def implement_standard_bloom_filter():
    filter_size = 100000
    list_of_x_axis_values = [i for i in range(1,9)]
    dictionary_of_filter_size_to_false_positives ={}
    filter_size_array = [i for i in range(10000,100000,10000)]
    # print(filter_size_array)
    for number_of_filter_size in filter_size_array:
        # print("*********************")
        x_axis_values = []
        y_axis_values = []
        for number_of_hashes in range(1,9):
            # print("Bloom filter size - {}, Number of hashes - {}".format(filter_size, number_of_hashes))
            sbf_object = SBF(number_of_filter_size, number_of_hashes)
            word_to_add_to_filter, words_to_search = get_words_to_add_to_bloom_filter()
            sbf_object.add_to_filer_and_set_bits(word_to_add_to_filter)
            search_results = sbf_object.check_if_list_of_words_contain(words_to_search)
            x_axis_values.append(number_of_hashes)
            y_axis_values.append(sbf_object.print_summary(search_results))
            # print("\n\n")
        dictionary_of_filter_size_to_false_positives[number_of_filter_size] = y_axis_values
    # print(list_of_x_axis_values, dictionary_of_filter_size_to_false_positives)
    plot_graph(list_of_x_axis_values, dictionary_of_filter_size_to_false_positives)
    print("*********************")

def implement_one_hash_bloom_filter():
    list_of_x_axis_values = [i for i in range(7,9)]
    dictionary_of_filter_size_to_false_positives ={}
    filter_size_array = [i for i in range(10000,100000,10000)]
    # print(filter_size_array)
    for number_of_filter_size in filter_size_array:
        # print("*********************")
        x_axis_values = []
        y_axis_values = []
        for number_of_mods in range(2,9):
            # print("Bloom filter size - {}, Number of hashes - {}".format(filter_size, number_of_mods))
            sbf_object = OHBF(number_of_filter_size, number_of_mods)
            word_to_add_to_filter, words_to_search = get_words_to_add_to_bloom_filter()
            sbf_object.add_to_filer_and_set_bits(word_to_add_to_filter)
            search_results = sbf_object.check_if_list_of_words_contain(words_to_search)
            x_axis_values.append(number_of_mods)
            y_axis_values.append(sbf_object.print_summary(search_results))
            # print("\n\n")
        dictionary_of_filter_size_to_false_positives[number_of_filter_size] = y_axis_values
    plot_graph(list_of_x_axis_values, dictionary_of_filter_size_to_false_positives, "modulo")
    print("*********************")

if __name__ == "__main__":
    # implement_standard_bloom_filter()
    implement_one_hash_bloom_filter()