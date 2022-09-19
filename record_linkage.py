# DATA 120: Linking restaurant records in Zagat and Fodor's data sets
#
# Su Karaca


import numpy as np
import pandas as pd
import util
import jellyfish
import itertools


#all possible category pairs
conditions = ["low", "medium", "high"]
possible_27 = [b for b in itertools.product(conditions, repeat=3)]



#defining a function that creates a list of category tuples given a dataframe with paired rows
def create_category_tuples(given_df):
    list_name = []
    for i in range(len(given_df)):
        score_name = jellyfish.jaro_winkler(given_df.iloc[i]["Rest_Zagat"], given_df.iloc[i]["Rest_Fodors"])
        score_city = jellyfish.jaro_winkler(given_df.iloc[i]["City_Z"], given_df.iloc[i]["City_F"])
        score_address = jellyfish.jaro_winkler(given_df.iloc[i]["Address_Z"], given_df.iloc[i]["Address_F"])
        cat_name = util.get_jw_category(score_name)
        cat_city = util.get_jw_category(score_city)
        cat_address = util.get_jw_category(score_address)
        any_tuple = (cat_name, cat_city, cat_address)
        list_name.append(any_tuple)
    return list_name
    
    

#creates a dictionary of keys: category tuples, values: probabilities
def prob_of_tuples(list_given):
    count_tup = 0
    all_probs = {}
    for tup in possible_27:
        num = list_given.count(tup)
        prob = num / (len(list_given))
        all_probs[tup] = prob
        
    return all_probs


#THE ACTUAL FUNCTION


def find_matches(mu, lambda_):
    
    # WRITE YOUR CODE HERE
    # AND REPLACE THE BELOW RETURN STATEMENT
    fodors = pd.read_csv('fodors.csv', header=None)
    fodors.rename(columns={0: 'Indexes_F', 1: 'Rest_Fodors', 2: 'City_F', 3:'Address_F'}, inplace=True)

    known_links = pd.read_csv('known_links.csv', header=None)
    known_links.rename(columns={0: 'Zagat_Index', 1: 'Fodors_Index'}, inplace=True)


    zagat = pd.read_csv('zagat.csv', header=None)
    zagat.rename(columns={0: 'Indexes_Z', 1: 'Rest_Zagat', 2: 'City_Z', 3: 'Address_Z'}, inplace=True)


    #creating the matches dataframe from the known_links columns
    matches_zagat =  pd.merge(known_links,zagat,left_on='Zagat_Index',right_on='Indexes_Z')

    matches = pd.merge(matches_zagat,fodors,left_on='Fodors_Index',right_on='Indexes_F')

    matches = matches.drop(columns=['Zagat_Index', 'Fodors_Index', 'Indexes_Z', 'Indexes_F'])

    #creating the unmatches dataframe by sample method
    zs = zagat.sample(1000, replace = True, random_state = 1234).reset_index().drop(columns=['index'])
    fs = fodors.sample(1000, replace = True, random_state = 5678).reset_index().drop(columns=['index'])

    zs['Rest_Fodors'] = pd.Series(fs['Rest_Fodors'])
    zs['City_F'] = pd.Series(fs['City_F'])
    zs['Address_F'] = pd.Series(fs['Address_F'])
    unmatches = zs
    unmatches.drop(columns = ['Indexes_Z'])
    
    
    #defining lists of match and unmatch tuples
    list_of_match_tuples = create_category_tuples(matches)
    list_of_unmatch_tuples = create_category_tuples(unmatches)
    
    
    
    #probability dictionaryies of matches and unmatches tuples
    prob_match = prob_of_tuples(list_of_match_tuples)
    prob_unmatch = prob_of_tuples(list_of_unmatch_tuples)



    #a dictionary of combined probabilities of uw and mw
    probabilities = {}
    for tupl in possible_27:
        mw = prob_match[tupl]
        uw = prob_unmatch[tupl]
        probabilities[tupl] = (uw, mw)
        
        

    #creates ordered probability lists of tuples
    possible_tuples = []
    for key in possible_27:
        if probabilities[key] == (0.0, 0.0):
            possible_tuples.append(key)
            

    sorted_order = []
    sira = []
    for key in possible_27:
        if key not in possible_tuples:
            if probabilities[key][0] == 0.0:
                sira.append((key, probabilities[key][1]))
                sira.sort(key = lambda x: x[1], reverse=True)
                #ranks by descending match probability because if m(w) is bigger more match chance
    for each_s in sira:
        sorted_order.append(each_s[0])
        

    ordered = []
    for key in possible_27:
        if key not in possible_tuples:
            if key not in sorted_order:
                if probabilities[key][1] != 0.0:
                    divided = probabilities[key][1]/probabilities[key][0]
                    ordered.append((key, divided))
                    ordered.sort(key = lambda x: x[1], reverse = True)
                    #ranks by descending m(w)/u(w)
    for each_k in ordered:
        sorted_order.append(each_k[0])
        
        
    ranked = []
    for key in possible_27:
        if key not in possible_tuples:
            if key not in sorted_order:
                ranked.append((key, probabilities[key][0]))
                ranked.sort(key = lambda x: x[1], reverse=False)
                #rankes by ascending unmatched probability because smaller the u(w) more match chance
    for each_r in ranked:
        sorted_order.append(each_r[0])
        
        
        
    #creates an ordered list of the tuples
    ordered_list = []
    for tupls in sorted_order:
        each_tuple_in = []
        each_tuple_in.append(tupls)
        each_tuple_in.append(probabilities[tupls])
        ordered_list.append(each_tuple_in)

    ordered_list.reverse()
    reversed_list = ordered_list[:]
    ordered_list.reverse()

    
    
    #creates match tuple list
    match_tuples = []
    cumulative_sum1 = 0
    for eacht in ordered_list:
        if (cumulative_sum1 + eacht[1][0]) > mu:
            break
        elif (cumulative_sum1 + eacht[1][0]) <= mu:
            cumulative_sum1 = cumulative_sum1 + eacht[1][0]
            match_tuples.append(eacht[0])
        
    #creates unmatch tuple list
    unmatch_tuples = []
    cumulative_sum2 = 0
    for eacht in reversed_list:
        #if w1 and w2 crossover, this will count all of the ambiguous tuples as being associated with matches
        if eacht[0] not in match_tuples:
            if (cumulative_sum2 + eacht[1][1]) > lambda_:
                break
            elif (cumulative_sum2 + eacht[1][1]) <= lambda_:
                cumulative_sum2 = cumulative_sum2 + eacht[1][1]
                unmatch_tuples.append(eacht[0])
                
    #adds the rest of the unmatched points (if any) to the possible tuples
    for eacht in ordered_list:
        if eacht[0] not in match_tuples:
            if eacht[0] not in unmatch_tuples:
                possible_tuples.append(eacht[0])
                
                
    
    #creates a dataframe of every possible pair of Zagat and Fodors
    every_possible_pair = pd.DataFrame(columns = ["Rest_Zagat", "Rest_Fodors",
                                                  "City_Z", "City_F",
                                                  "Address_Z", "Address_F"])
    for z in range(0, len(zagat)):
        for f in range(0, len(fodors)):
            every_possible_pair = every_possible_pair.append({"Rest_Zagat": zagat.iloc[z]["Rest_Zagat"],
                                                              "Rest_Fodors": fodors.iloc[f]["Rest_Fodors"],
                                                              "City_Z": zagat.iloc[z]["City_Z"],
                                                              "City_F": fodors.iloc[f]["City_F"],
                                                              "Address_Z": zagat.iloc[z]["Address_Z"],
                                                              "Address_F": fodors.iloc[f]["Address_F"]},
                                                             ignore_index = True)
            
    #creates category tuples for every row in the dataframe
    every_pairs_tuple = create_category_tuples(every_possible_pair)
    
    
    #creates a dictionary of keys: index of pair tuples from the pair dataframe and values: pair tuples
    tuples_dict = {}

    for r in range(0, len(every_possible_pair)):
        tuples_dict[r] = every_pairs_tuple[r]
        
    
    
    #creates the three dataframes for match pairs, unmatch pairs, and possible pairs using the dictionary created
    match_pairs = pd.DataFrame(columns = ["Rest_Zagat", "City_Z", "Address_Z",
                                        "Rest_Fodors", "City_F", "Address_F"])
    unmatch_pairs = pd.DataFrame(columns = ["Rest_Zagat", "City_Z", "Address_Z",
                                        "Rest_Fodors", "City_F", "Address_F"])
    possible_pairs = pd.DataFrame(columns = ["Rest_Zagat", "City_Z", "Address_Z",
                                        "Rest_Fodors", "City_F", "Address_F"])

    for e in range(len(tuples_dict)):
        if tuples_dict[e] in match_tuples:
            match_pairs = match_pairs.append({"Rest_Zagat": every_possible_pair.iloc[e]["Rest_Zagat"],
                                            "City_Z": every_possible_pair.iloc[e]["City_Z"],
                                            "Address_Z": every_possible_pair.iloc[e]["Address_Z"],
                                            "Rest_Fodors": every_possible_pair.iloc[e]["Rest_Fodors"],
                                            "City_F": every_possible_pair.iloc[e]["City_F"],
                                            "Address_F": every_possible_pair.iloc[e]["Address_F"]},
                                             ignore_index = True)
        elif tuples_dict[e] in unmatch_tuples:
            unmatch_pairs = unmatch_pairs.append({"Rest_Zagat": every_possible_pair.iloc[e]["Rest_Zagat"],
                                            "City_Z": every_possible_pair.iloc[e]["City_Z"],
                                            "Address_Z": every_possible_pair.iloc[e]["Address_Z"],
                                            "Rest_Fodors": every_possible_pair.iloc[e]["Rest_Fodors"],
                                            "City_F": every_possible_pair.iloc[e]["City_F"],
                                            "Address_F": every_possible_pair.iloc[e]["Address_F"]},
                                             ignore_index = True)
        elif tuples_dict[e] in possible_tuples:
            possible_pairs = possible_pairs.append({"Rest_Zagat": every_possible_pair.iloc[e]["Rest_Zagat"],
                                            "City_Z": every_possible_pair.iloc[e]["City_Z"],
                                            "Address_Z": every_possible_pair.iloc[e]["Address_Z"],
                                            "Rest_Fodors": every_possible_pair.iloc[e]["Rest_Fodors"],
                                            "City_F": every_possible_pair.iloc[e]["City_F"],
                                            "Address_F": every_possible_pair.iloc[e]["Address_F"]},
                                             ignore_index = True)
            
    return (match_pairs, unmatch_pairs, possible_pairs)


if __name__ == '__main__':
    matches, possibles, unmatches = \
        find_matches(0.005, 0.005)

    print("Found {} matches, {} possible matches, and {} "
          "unmatches.".format(matches.shape[0],
                                               possibles.shape[0],
                                               unmatches.shape[0]))
                                               
                                               
                                               
#end of code check line
