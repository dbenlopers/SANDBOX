
import HGM, HGM.helpers
import math
from matplotlib import pyplot as plt



def plot_simple_function_as_list( fileName, values,xLabel,title ):
    """ plot an ensemble of values as a time series 
    @param fileName: where to save the plot   
    @param values:    the y values ( x is implicitely 1,2,... len(values) )
    @param xlabel:    
    @param title:    
    """
    x=range(len(values))
    plt.title(title)
    plt.xlabel(xLabel)
    plt.ylabel("score")
    plt.plot(x,values)
    plt.savefig(fileName)
    plt.clf()

def plot_histogram( fileName, scores, bins, xlabel=None, ylabel=None, title=None):
    nb_configs=len(scores)
    
    plt.clf()
    plt.hist(scores, bins=bins, range=None, normed=False, cumulative=False,
        bottom=None, histtype='bar', align='mid',
        orientation='vertical', rwidth=None, log=False)
    if xlabel != None : plt.xlabel(xlabel)
    if ylabel != None : plt.ylabel(ylabel)
    if title  != None : plt.title(title)
    
    plt.savefig(fileName)
    plt.clf()
    
def plot_histogram_with_margins(fileName, values, bins, xlabel=None, ylabel=None, title=None):
    
    meanX,stdX = HGM.helpers.compute_list_statistics(values)
    stdX=math.sqrt(stdX)
        
    plt.clf()
    plt.hist(values, bins=bins, range=None, normed=False, cumulative=False,
        bottom=None, histtype='bar', align='mid',
        orientation='vertical', rwidth=None, log=False)
            
    plt.axvspan(meanX-stdX,meanX+stdX, facecolor='g', alpha=0.4)
    plt.axvline(x=meanX, color='r')
    
    if xlabel != None : plt.xlabel(xlabel)
    if ylabel != None : plt.ylabel(ylabel)
    if title  != None : plt.title(title)

    plt.savefig(fileName)
    plt.clf()