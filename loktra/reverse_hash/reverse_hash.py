'''
reverse hash:
'''


def reverse_hash(hash_value):
    main_string = 'acdegilmnoprstuw'
    tmp_list = list()
    final_list = list()

    # range(0, 9) for a string of length 9 characters from the given list of characters...
    # the content of the tmp_list will be in reverse order...
    for x in range(0,9):
        index_val = hash_value % 37
        tmp_list.append(main_string[int(index_val)])
        hash_value = int(hash_value/37)

    # reversing the content of the tmp_list...
    for idx in range(len(tmp_list)):
        final_list.append(tmp_list.pop())

    return final_list


if __name__=='__main__':
    hash_value = 930846109532517
    print(str(reverse_hash(hash_value)), sep='')