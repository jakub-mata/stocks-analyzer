# STOCKS ANALYZER


### student
Jakub Mata


## Requirements
- Python 3.6 or newer
- Beautiful Soup 
- Requests
- Numpy
- Pandas
- Matplotlib

### How to install dependencies

You can use pip to install dependencies listed above:

```
pip install beautifulsoup4

pip install requests

pip install numpy

pip install pandas

pip install -U matplotlib
```
## How to use

 The application is controlled through your terminal. Open your terminal and type:
 ```
 python3 stocks_analyzer.py *wanted stock(s)*
 ```
 You can use `python` instead of `python3` of the version on your machine matches the version. If you're on Windows, use `py` instead. The name of the program by a positional argument (desired stock(s). Example usage:
 ```
 python3 stocks_analyzer.py Apple
 ```
 nebo
 ```
 python3 stocks_analyzer.py Boeing Tesla Microsoft
 ```
. Should your stock name have multiple words, type it in quotes. The application then searches for your query and presents you with all the matching output. You are then required to choose the correct one. If no match is found, the application warns you and ends. Example:
```
python3 stocks_analyzer.py Apple
The site is loading...
Matches found. Type the correct number. Type -1 if none match:
1.  APPLE COMP INC
2.  DR PEPPER SNAPPLE GROUP
Type here: 
```
After fetching the data, you get a dataframe (table) displayed in your terminal relating to each stock. Furthermore, you get a figure with graphs, linear approximation (linear regression) of the graph and some additional info on the side. You might be able to save this figure depending on your PC's default application. 

### Optional arguments
The application also has other 3 optional arguments:
- `--no_plot or -p`
	- This option *disables* displaying the plot with your data. 
- `--no_table or -t`
	- This option *disables* displaying a table with your data in your terminal
- `--merge`
	- The default display option is to show all graphs separately on the same figure. This is done to degradation of visualized data (mostly because the differences between stocks may be large enough to flatten the curves). However, you can choose the merge them if you wish (e.g. you know the stocks have similar value and the output wouldn't be influenced)
- `--plain`
	- The default display option is to show linear approximation with all graphs. By choosing `--plain`, you can disable this feature.	

Note that the application *will not stop you* from choosing contradicting optional arguments. If you choose `--merge` and `--no_plot`, the merge option will have no effect since no plot will be displayed. If you choose `--no_table` and `--no_plot`, you will get no output.  

## How the program actually works

The application is separated into 3 files:
- `stocks_analyzer.py`
	- the main function
	- includes a function spaces and the main call
- `interface.py`
	- resolving all the interaction with user
- `data.py`  
	- working with and displaying data 

After the application starts running by calling the `interface.py` file for user arguments, the main call `show_table_an_plot()` is called. We then have to extract the data from the site by calling  `get_table_query()`, which in turn calls web crawling functions.

The site used for web scraping is https://www.kurzy.cz/akcie-svet/index.asp. Their API for GET requests is 
```
{
"Act0": "-3",
"P": "wavsrchres",
"SPhr": *stock_name*,
"S_OK": "Hledej"
} 
```
. We send the request with the requests library and create a soup by calling our `soup_maker()` function, which uses Beautiful Soup. This soup contains matching results. We fetch them with `find_matches()` and `get_text_from_matches()` and present them to the user with `find_wanted_stock()` in the `interface.py` file to pick the correct one. The table data have a common CSS attribute
`align: "right"` which is used to find it. 

If no matches are found, the `get_table_query()` function returns `None`, which accumulates to notifying the user and ending the application (in `show_table_and_plot`).

This process loops for all the inputted stocks and then `get_table_query()` returns all the data in a table.

`Show_table_and_plot` either prints out a warning to the user if something is wrong or proceeds. Then it chooses between `show_plot()` (stocks in different graphs) and `one_plot()`(all in one graph) functions from `data.py` depending on whether the `--merge` arguments was called.

### Data manipulation

The functions extract the data from the tables and create Pandas dataframes, which are then printed to the terminal.  `statistics()` called from the main `show_plot()`computes the mean, standard deviation and general direction of the function in percentages. These are appended to the plot (not in case of `one_plot()` because the graph becomes too messy). `lin_reg()`, which computes linear regression function for a given set of values, is called. Lastly, the values themselves are plotted.  
 
