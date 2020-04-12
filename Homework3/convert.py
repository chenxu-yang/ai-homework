import sys
import os
import _pickle as pickle
import json



def main():
    with open('allrestaurant.pickle') as fpkl, open('allrestaurant.json', 'w') as fjson:
        data = pickle.load(fpkl)
        json.dump(data, fjson, ensure_ascii=False, sort_keys=True, indent=4)



if __name__ == '__main__':
    main()

