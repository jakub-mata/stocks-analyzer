import numpy as np
from numpy.polynomial import Polynomial
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from matplotlib.cm import tab20  # VS Code might display as unknown import symbol

def extract_table(table):
    """
    Extracts information from a table to get dates and their respective closing stock values

    Args:
        table: the table to extract from

    Returns a tuple, first position == list of dates, second_position == list of closing values    
    """
    dates = []
    closing_value = []
    ROW_WIDTH = 7
    for i in range(0, len(table)-2): #The actual table on the site has two td's more hidden inside
        if i % ROW_WIDTH == 0:
            date = str(table[i].string)
            date = date.replace("\xa0", "")
            dates.append(date)
        elif i % 7 == 4:      
            value = str(table[i].string)
            value = value.replace("\xa0", "")
            closing_value.append(float(value))
    return dates, closing_value


def dataFrame_maker(lst_of_dates: list, lst_of_values: list, name: str):
    df = pd.DataFrame({
        name: pd.Series(lst_of_values, index = lst_of_dates)
    })
    return df


def lin_reg(x_values, y_values) -> tuple:
    """
    Returns a slope and y-intercept of a function approximating a given set of points 
    """
    #x_values = [datetime.datetime.timestamp(date) for date in x_values]
    x = np.array(x_values)
    y = np.array(y_values, dtype = float)
    coefficients = Polynomial.fit(x, y, deg=1).convert().coef
    slope: float = coefficients[1]
    intercept: float = coefficients[0]
    return (slope, intercept)


def lin_reg_mask(dates: list, values: list, x_float):
    """
    Handles dates and values to make lin approximation a straight line (dates do not include weekends which
    prompts spikes to appear). Returns handled data to use for linear regression.
    """
    mask = ((np.arange(len(dates))) % 5 == 0) | (np.arange(len(dates)) == len(dates) - 1)
    selected_dates = np.array(dates)[mask]
    selected_values = np.array(values)[mask]
    selected_timestamps = x_float[mask]
    return selected_dates, selected_values, selected_timestamps

    
def statistics(values: list) -> list:
    """
    A function computing most valuable statitical data from our dataset.

    Args:
        - values: a list of values (our dataset of floats)

    Returns a list containing (in this order) mean, standard deviation and the relativce difference
    of the first and last value.
    """
    returned_stats: list = []

    #average
    sum:float = 0
    for value in values:
        sum += value
    mean: float = round(sum / len(values), 2)
    returned_stats.append(mean)

    #standard deviation
    std_dev = round(np.std(values), 2)
    returned_stats.append(std_dev)
    part: float = round(float(std_dev) * 100 / mean, 1)
    returned_stats.append(part)
    
    return returned_stats


def show_plot(tables, names, showTable, showPlot, lin_bool):
    """
    Creates and shows a plot for each table input.

    Args:
        axis: a list containing tuples (x, y) of coordinates

    Void return
    """
    fig, axes = plt.subplots(len(tables), figsize=(12, 10))
    idx = 0
    colors = tab20.colors
    df = None

    for table in tables:
        dates, values = extract_table(table)
        name = names[idx]
        if idx == 0:
            df = dataFrame_maker(dates, values, name)
        else:
            df[name] = values

        dates = dates[::-1]
        values = values[::-1]
        x_date = pd.to_datetime(dates, format="%d.%m.%Y")
        x_float = np.array(x_date.map(datetime.datetime.timestamp), dtype=float)
        y = np.array(values)

        statistics_data: list = statistics(values)  #Data statistics
        mean, std_dev, part = statistics_data

        axes[idx].text(0.05, 0.95, f'Mean: {mean}\nStd Dev: {std_dev} ({part}%)', verticalalignment='top', 
                       horizontalalignment='left', transform=axes[idx].transAxes, fontsize=8, backgroundcolor='white')

        # Labeling
        axes[idx].set_xlabel("Date")
        axes[idx].set_ylabel("Value [US Dollars]")
        axes[idx].plot(dates, y, label=name, color=colors[2*idx])  

        # Linreg
        if lin_bool:
            selected_dates, selected_values, selected_timestamps = lin_reg_mask(dates, values, x_float)  # Straight linear regression
            slope, intercept = lin_reg(selected_timestamps, selected_values)
            axes[idx].plot(selected_dates, slope * selected_timestamps + intercept, label=f"{name}-linear approximation", 
                           color=colors[2*idx+1])
            
        axes[idx].grid(visible=True, which="both", axis="both")
        axes[idx].legend(loc="lower right")
        idx += 1
    
    fig.autofmt_xdate()
    if showTable:
        print(df)

    if showPlot:
        plt.show()


def one_plot(tables, names, showTable, showPlot, lin_bool):
    """
    Creates one plot for all tables.
    """

    fig, axes = plt.subplots(figsize=(12, 10))
    idx = 0
    colors: list = tab20.colors
    df = None

    for table in tables:
        dates, values = extract_table(table)
        name = names[idx]
        if idx == 0:
            df = dataFrame_maker(dates, values, name)
        else:
            df[name] = values

        dates = dates[::-1]
        values = values[::-1]
        x_date = pd.to_datetime(dates, format="%d.%m.%Y")
        x_float = np.array(x_date.map(datetime.datetime.timestamp), dtype=float)
        y = np.array(values)

        selected_dates, selected_values, selected_timestamps = lin_reg_mask(dates, values, x_float)

        axes.set_xlabel("Date")
        axes.set_ylabel("Value [US Dollars]")
        axes.plot(dates, y, label=name, color=colors[2*idx])  

        #linreg
        if lin_bool:
            selected_dates, selected_values, selected_timestamps = lin_reg_mask(dates, values, x_float)
            slope, intercept = lin_reg(selected_timestamps, selected_values)
            axes.plot(selected_dates, slope * selected_timestamps + intercept, label=f"{name}-linear approximation", 
                      color=colors[2*idx+1])
        idx += 1

    axes.legend(loc="upper left")
    axes.grid(visible=True, which="both", axis="both")
    fig.autofmt_xdate()
    if showTable:
        print(df)
    if showPlot:
        plt.show()





