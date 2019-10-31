import os, sys
import random
import argparse
random.seed(1234)
from collections import Counter

class NameSampler:
    def __init__(self, dist=False, gender=False, year_from=1880, year_to=2017, name_path=""):
        self.dist = dist
        self.gender = gender
        self.year_from = year_from
        self.year_to = year_to
        self.name_path = name_path
        assert self.year_from >= 1880
        assert self.year_to   <= 2017

        self.name2count = Counter()
        self.name2count_male = Counter()
        self.name2count_female = Counter()

        for y in range(self.year_from, self.year_to+1):
            self.year_file = os.path.join(*[self.name_path, "names", "yob" + str(y) + ".txt"])
            for line in open(self.year_file):
                line = line.split(',')
                assert len(line) == 3, "%s idoes not have 3 sections" % (",".join(line))
                if self.gender:
                    if line[1] == 'F':
                        if self.dist:
                            self.name2count_female[line[0]] += int(line[-1].strip())
                        else:
                            self.name2count_female[line[0]] = 1
                    else:
                        if self.dist:
                            self.name2count_male[line[0]] += int(line[-1].strip())
                        else:
                            self.name2count_male[line[0]] = 1
                else:
                    if self.dist:
                        self.name2count[line[0]] += int(line[-1].strip())
                    else:
                        self.name2count[line[0]] = 1

        self.name_candidates = list(self.name2count.elements())
        self.name_candidates_male = list(self.name2count_male.elements())
        self.name_candidates_female = list(self.name2count_female.elements())


    def sample(self, k=10):
        assert k > 0
        if self.gender:
            sample_names_male = [random.choice(self.name_candidates_male) for _ in range(k)]
            sample_names_female = [random.choice(self.name_candidates_female) for _ in range(k)]
            return (sample_names_male, sample_names_female)

        else:
            sample_names = [random.choice(self.name_candidates) for _ in range(k)]
            return sample_names


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-f', "--from", type=int, action='store', 
            default=1880, dest='arg_from', 
            help='names from this year', required=False)
    arg_parser.add_argument('-t', "--to", type=int, action='store', 
            default=2017, dest='arg_to', 
            help='names to this year', required=False)
    arg_parser.add_argument('-n', "--num", type=int, action='store', 
            default=10, dest='arg_num', 
            help='number of names to sample', required=False)
    arg_parser.add_argument('-d', "--distribution", action='store_true', 
            default=False, dest='arg_dist',
            help="follow actual distribution (i.e., frequency of names) or not", required=False)
    arg_parser.add_argument('-g', "--gender", action='store_true', 
            default=False, dest='arg_gender',
            help="sample names for each gender or not", required=False)


    args = arg_parser.parse_args()
    assert args.arg_from >= 1880
    assert args.arg_to   <= 2017
    assert args.arg_num > 0

    ns = NameSampler(args.arg_dist, args.arg_gender, args.arg_from, args.arg_to, name_path="")
    print(ns.sample(args.arg_num))
    print(ns.sample(args.arg_num))
    print(ns.sample(args.arg_num))


