import collections
import random
import cc1_levelset_proto
from cc1_levelset_io.cc1_levelset_reader import CC1LevelsetReader
from cc1_levelset_io.cc1_levelset_writer import CC1LevelsetWriter

class CC1LevelsetWrapper:
    def __init__(self, levelset):
        self.levelset = levelset
        self.eligible = set([i+1 for i in range(len(levelset.levels))])
        self.titles = [lv.title.lower() for lv in levelset.levels]
 
    def level_num(self, title):
        try:
            return self.titles.index(title.lower()) + 1
        except ValueError:
            return None

    def flatten_args(self, args):
        flat_args = []
        for arg in args:
            if isinstance(arg, collections.Iterable) and not isinstance(arg, str):
                flat_args.extend(arg)
            else:
                flat_args.append(arg)
        return flat_args
    
    def get_valid_arg_set(self, args):
        valid = set()
        args = self.flatten_args(args)
        for arg in args:
            if isinstance(arg, str):
                lvlnum = self.level_num(arg)
                if lvlnum:
                    valid.add(lvlnum)
                else:
                    print(f"Level '{arg}' not found in '{self.levelset.name}'. Ignoring.")
            elif isinstance(arg, int):
                if arg > 0 and arg <= len(self.levelset.levels):
                    valid.add(arg)
                else:
                    print(f"Level #{arg} not found in '{self.levelset.name}'. Ignoring.")
            else:
                raise Exception(f"arg must be int or set. got <{arg}> of type <{type(arg)}>")
        return valid

    # args can be int, str, collection of int, or collection of str
    def drop(self, *args):
        to_remove = self.get_valid_arg_set(args)
        already_removed = to_remove.difference(self.eligible)
        intersection = [self.levelset.levels[i-1].title for i in self.eligible.intersection(to_remove)]
        if len(already_removed) > 0:
            print(f"Elements {already_removed} were already removed. Ignoring.")
        print(f"Removed {len(intersection)} levels: {intersection}.")
        self.eligible.difference_update(to_remove)
        return self
    
    # args can be int, str, collection of int, or collection of str
    def keep(self, *args):
        to_keep = self.get_valid_arg_set(args)
        intersection = [self.levelset.levels[i-1].title for i in self.eligible.intersection(to_keep)]
        print(f"Kept {len(intersection)} levels: {intersection}")
        return self.drop(self.eligible.difference(to_keep))
    
    # args can be int, str, collection of int, or collection of str
    def add(self, *args):
        to_add = self.get_valid_arg_set(args)
        added = [self.levelset.levels[i-1].title for i in to_add.difference(self.eligible)]
        print(f"Added {len(added)} levels.")
        self.eligible.update(to_add)
        return self
    
    def get_level(self, level_num):
        return self.levelset.levels[level_num - 1]

class CC1RandomLevelsetGenerator:
    def __init__(self):
        self.reader = CC1LevelsetReader()
        self.writer = CC1LevelsetWriter()
        self.pool = dict()
    
    def add_set(self, levelset):
        self.pool[levelset] = CC1LevelsetWrapper(self.reader.import_and_read(levelset))
        return self.pool[levelset]

    def get_set(self, levelset):
        return self.pool[levelset]

    def drop(self, *titles):
        flat_list = []
        for title in titles:
            if isinstance(title, str):
                flat_list.append(title)
            else:
                flat_list.extend(title)
        for title in flat_list:
            for wrapper in self.pool.values():
                if title.lower() in wrapper.titles:
                    wrapper.drop(title)

    def count_eligible(self):
        return sum([len(wrapper.eligible) for wrapper in self.pool.values()])
    
    def generate_random_set(self, n_levels, filename=None):
        combined_set = cc1_levelset_proto.cc1_levelset_pb2.Levelset()
        for wrapper in self.pool.values():
            for level_num in wrapper.eligible:
                combined_set.levels.append(wrapper.get_level(level_num))
        
        picks = random.sample(range(len(combined_set.levels)), n_levels)
        
        random_set = cc1_levelset_proto.cc1_levelset_pb2.Levelset()
        for i, pick in enumerate(picks):
            level = combined_set.levels[pick]
            level.number = i + 1
            random_set.levels.append(level)

        if filename:
            self.writer.write(random_set, filename)
        return random_set

    def write(self, lset, filename):
        self.writer.write(lset, filename=filename)
