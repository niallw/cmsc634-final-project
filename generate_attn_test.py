import os
import csv
import matplotlib.pyplot as plt
import random
import copy
import shutil
import numpy as np

def check_intermediate_sample(arr):
    # The values were randomly generated by a uniform random-number generator, with 
    # results rescaled to sum to 100. Each set was constrained to meet three 
    # requirements: 
    #     - The minimum value had to be greater than 3; 
    #     - the maximum value had to be less than 39, and 
    #     - all differences between values in a set had to be greater than .1. 
    min_val = min(arr)
    max_val = max(arr)
    total = sum(arr)

    return (min_val > 3 and max_val < 39 and total < 97 and total > 61)

def check_final_sample(arr):
    # all differences between values in a set had to be greater than .1. 
    for i in range(len(arr)):
        cur_val = arr[i]
        for j in range(len(arr)):
            if j == i:
                continue
            other_val = arr[j % len(arr)]
            if abs(cur_val - other_val) <= 0.1:
                return False
    return True

def get_sample():
    values = np.random.uniform(3, 39, [4])

    while not check_intermediate_sample(values):
        values = np.random.uniform(3, 39, [4])
    
    values = np.append(values, 100 - sum(values)) # add the 5th value
    while not check_final_sample(values):
        values = np.random.uniform(3, 39, [4])
        while not check_intermediate_sample(values):
            values = np.random.uniform(3, 39, [4])

    return values

def generate_bar_chart(i, values):
    names = ['A', 'B', 'C', 'D', 'E']
    random.shuffle(names)

    plt.rcParams['font.weight'] = 'bold'
    fig, ax = plt.subplots()
    plt.bar(names, values, width=0.8, linewidth=1.5, align='center', edgecolor='black', color='white')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_linewidth(1.5)
    ax.spines['left'].set_linewidth(1.5)
    plt.yticks([0,40])
    ax.set_ylim(ymax=40)
    ax.xaxis.set_tick_params(width=1.5)
    ax.yaxis.set_tick_params(width=1.5)
    plt.savefig('{}_barchart.png'.format(i))
    return plt

def generate_pie_chart(i, values):
    names = ['A', 'B', 'C', 'D', 'E']
    random.shuffle(names)

    plt.rcParams['font.weight'] = 'bold'
    fig1, ax1 = plt.subplots()
    ax1.pie(values, labels=names, colors=['white']*5, wedgeprops ={"edgecolor":"black",'linewidth':1.5, 'linestyle':'solid', 'antialiased': True})
    plt.savefig('{}_piechart.png'.format(i))
    return plt

def generate_answer_key(index, values):
    names = ['A', 'B', 'C', 'D', 'E']
    to_sort = []

    for i in range(len(values)):
        to_sort.append((names[i], values[i]))

    to_sort.sort(key = lambda x: x[1])

    max_val = to_sort[-1][1]

    with open('{}_answers.txt'.format(index), 'w') as f:
        for t in to_sort:
            f.write('{} | Size: {} | Proportion: {}%\n'.format(t[0], t[1], t[1] / max_val * 100))
            # f.write('{} | Size: {}\n'.format(t[0], t[1]))
    return to_sort

def main():
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(cur_dir)
    if not os.path.isdir('attn_check'):
        os.mkdir('attn_check')
    else:
        shutil.rmtree('attn_check')
        os.mkdir('attn_check')
    os.chdir(os.path.join(cur_dir, 'attn_check'))
        
    # Ten sets of five numbers that added to 100 were generated and each set was 
    # encoded by a bar chart and a pie chart, resulting in 20 graphs. 
    # For each graph, the answer sheet indicated which pie segment or bar was largest 
    # and sub- jects were asked to judge what percentage each of the other four values 
    # was of the maximum
    for i in range(2):
        values = get_sample()
        generate_bar_chart(i+1, values)
        generate_pie_chart(i+1, values)
        # generate_answer_key(i+1, values)

if __name__ == "__main__":
    main()