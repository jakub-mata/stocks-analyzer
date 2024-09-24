from bs4 import BeautifulSoup
import requests
import time
import interface 
import data


###INTERFACE INFO
form_action = "https://www.kurzy.cz/akcie-svet/index.asp"
args = interface.args()
stock_names = args.query
show_table: bool = True 
show_table: bool = args.no_table   
show_plot: bool = args.no_plot
merge_bool: bool = args.merge
lin_reg:bool = args.plain

###FUNCTION SPACE
def soup_maker(url: str, timeout: int=0, par=None):
    """
    A function that creates a Beautiful Soup object from a site of a given url.

    Args: 
        -url: url for the site
        -timeout: if a sites is dynamic, a timeout might be set to wait for it to load
        -par: parameters to pass with the request

    Returns a Beautiful Soup object   
    """  
    request = requests.get(url, params = par)
    print("The site is loading...")
    time.sleep(timeout)
    return BeautifulSoup(request.text, "html.parser")


def anchor_with_siblings(tag):
    return tag.name == "a" and tag.parent.name == "td" and tag.string != "Osobního seznamu" and list(tag.children)[0].name != "img"


def find_matches(page):
    results_query = page.find_all(anchor_with_siblings)
    lst_of_matches = []
    for match in results_query:
        lst_of_matches.append(match)
    return lst_of_matches


def get_text_from_matches(matches: list):
    text_form = []
    for match in matches:
        text_form.append(match.get_text())
    if text_form == []: return None  
    return text_form    


def show_table_and_plot(tables, stock_names: list, show_table: bool, show_plot: bool, merge_bool: bool, lin_reg: bool):
    
    if len(tables) == 0:
        return
    
    if not merge_bool and len(tables) != 1:
        data.show_plot(tables, stock_names, show_table, show_plot, lin_reg)
    else:
        data.one_plot(tables, stock_names, show_table, show_plot, lin_reg)    


def get_table_query(desired_stock):
    table: list = []
    name_list: list = []
    for stock in desired_stock:
        #API
        params = {
        "Act0": "-3",
        "P": "wavsrchres",
        "SPhr": stock,
        "S_OK": "Hledej"
        }

        #web crawling
        search_soup = soup_maker(form_action, 0, params)  #search result page
        matches: list = find_matches(search_soup)
        matches_text = get_text_from_matches(matches)
        if matches_text is None:  #Error handling
            print(f"No matches found for {stock} in the database.")
            continue

        #user-input 
        idx:int = interface.find_wanted_stock(matches_text) 
        if idx is False:  #Error handling
            print(f"Invalid selection for {stock}.")
            continue
        
        name_list.append(matches_text[idx])
        wanted = matches[idx]
        redirect = wanted["href"] 

        #web-crawling
        stock_page_soup = soup_maker(redirect, timeout=3)
        table.append(stock_page_soup.find_all("td", attrs={"align": "right"}))
    
    return table, name_list


###MAIN   
table_query = get_table_query(stock_names)  
show_table_and_plot(table_query[0], table_query[1], show_table, show_plot, merge_bool, lin_reg)
