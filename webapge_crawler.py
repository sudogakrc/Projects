#web page crawler: this code starts with an initial link from the University of Chicago course catalogue 
#and creates course and relative key word pairings from the course's title and description. Code continues 
#until completing every course listed by opening the relative links found on the initial webpage.

#utilized beautifulsoup


import util
import bs4

INDEX_IGNORE = set(['a', 'also', 'an', 'and', 'are', 'as', 'at', 'be',
                    'but', 'by', 'course', 'for', 'from', 'how', 'i',
                    'ii', 'iii', 'in', 'include', 'is', 'not', 'of',
                    'on', 'or', 's', 'sequence', 'so', 'social', 'students',
                    'such', 'that', 'the', 'their', 'this', 'through', 'to',
                    'topics', 'units', 'we', 'were', 'which', 'will', 'with',
                    'yet'])


### YOUR FUNCTIONS HERE


def convert_str(tag):

#creates lists of list[0]=title string, list[1]=description string

    t = tag.text
    t = t.split("\n")

    course_t_d = []
    course_t_d.append(t[1])
    course_t_d.append(t[2])
    return course_t_d
    
    
def create_list_of_tuples(soup_str):

    course_divs = soup_str.find_all('div', class_="courseblock")

#below code produces a list of lists as described in the convert_str()
#adds the title of the main subsequence title to each of the subsequence course titles
#adds the description of the main subsequence description to each of the subsequence course description

    new = []
    for i in course_divs:
        if util.is_subsequence(i) == False and util.is_subsequence(i.next_sibling) == False:
            new.append(convert_str(i))
        if util.is_subsequence(i) == False and util.is_subsequence(i.next_sibling) == True:
            for each in util.find_sequence(i):
                seq_comb = [x+ " " + y for x,y in zip(convert_str(each), convert_str(i))]
                new.append(seq_comb)

    course_t = []
    course_d = []
    for s in new:
        course_t.append(s[0])
        course_d.append(s[1])
        
#below code prepares the title words
    
    course_t_split = []
    for ti in course_t:
        c = ti.lower().replace("\xa0", " ").replace(".", "").split()
        course_t_split.append(c)

    course_title_words = []
    for ts in course_t_split:
        newlist = sorted(set(ts), key=lambda x:ts.index(x))
        newlist = [item for item in newlist if item not in INDEX_IGNORE]
        course_title_words.append(newlist)
        
#below code creates course codes

    
    course_codes = []
    for course in course_title_words:
        word_comb = course[0].upper() + " " + course[1].upper()
        course_codes.append(word_comb)
        
#below code prepares the description words
    
    course_d_split = []
    for di in course_d:
        z = di.lower().replace(",", "").replace(".", "").split()
        course_d_split.append(z)

    course_desc_words = []
    for ds in course_d_split:
        newlist2 = sorted(set(ds), key=lambda x:ds.index(x))
        newlist2 = [wor for wor in newlist2 if wor not in INDEX_IGNORE]
        course_desc_words.append(newlist2)
        
#below code combines title words with description words

    combined_words = [x+y for x,y in zip(course_title_words, course_desc_words)]
    
#below code creates a dictionary with keys: course codes and values: descriptive combined words

    keys = course_codes
    values = combined_words
    dictionary_of_index = dict(zip(keys, values))
    
#below code creates tuples from the dictionary above

    list_of_tuples = []
    for place in dictionary_of_index:
        for val in dictionary_of_index[place]:
            tuples_of_index = (place, val)
            list_of_tuples.append(tuples_of_index)
    return list_of_tuples

def go():
    '''
    Crawl the college catalog and generate a list with an index.

    Outputs:
        list with the index
    '''

    starting_url = ("https://www.classes.cs.uchicago.edu/archive/2015/winter/12200-1/new.collegecatalog.uchicago.edu/thecollege/programsofstudy.1.html")
    limiting_domain = "classes.cs.uchicago.edu"

    # YOUR CODE HERE
    
#next code creates a list of links found on the initial page that are ok to use
    
    html1 = (starting_url)
    html1 = util.get_request(html1)
    text1 = util.read_request(html1)

    soup1 = bs4.BeautifulSoup(text1, "html5lib")

    list_of_links_on_page = []
    for links in soup1.find_all('a', href=True):
        list_of_links_on_page.append(links['href'])


    edited_links = []
    for lin in list_of_links_on_page:
        removed = util.remove_fragment(lin)
        converted = util.convert_if_relative_url(starting_url, removed)
        edited_links.append(converted)
        edited_links = [no for no in edited_links if no]

    ok_links = []
    for edi in edited_links:
        if util.is_url_ok_to_follow(edi, limiting_domain):
            ok_links.append(edi)
            
#below code combines all the list of tuples created in each page link extracted
    
    actual_tuple_list = []
    for actual_links in ok_links:
        html2 = (actual_links)
        if util.get_request(html2) is not None:
            html2 = util.get_request(html2)
            
            if util.read_request(html2) is not None:
                text2 = util.read_request(html2)
                soup = bs4.BeautifulSoup(text2, "html5lib")
                list_for_each_link = create_list_of_tuples(soup)
                for course_el in list_for_each_link:
                    actual_tuple_list.append(course_el)

    return actual_tuple_list

#final check -- passed
