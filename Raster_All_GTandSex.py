import csv
import matplotlib.pyplot as plt
import ast
import math
from matplotlib.backends.backend_pdf import PdfPages
import os

csv_file = "/Users/samdhanani/Desktop/MuhleLab/Operant_Data_Folders/a csv file with the values you want to plot"
date = "06-05-24"  # Specify the date you want to plot
max_x_value = 2500 

pdf_file_path = "/Users/samdhanani/Desktop/06-05-24.pdf"
pdf_pages = PdfPages(pdf_file_path)

with open(csv_file, 'r') as file:
    reader = csv.DictReader(file)
    genotype_sex_dict = {}  # 

    for row in reader:
        if row['Date'] == date:
            genotype_sex = (row['Genotype'], row['Sex'])
            if genotype_sex not in genotype_sex_dict:
                genotype_sex_dict[genotype_sex] = []
            genotype_sex_dict[genotype_sex].append(row)

    with PdfPages(pdf_file_path) as pdf_pages:
        # Generate plots for each group of genotype and sex
        for genotype_sex, subjects in genotype_sex_dict.items():
            num_rows = math.ceil(len(subjects) / 2)
            num_cols = min(len(subjects), 2)
            fig, axs = plt.subplots(num_rows, num_cols, figsize=(20, 10 * num_rows))
            genotype, sex = genotype_sex
            fig.suptitle(f'{genotype} - {sex} - {date}', fontsize=14)

            for i, subject in enumerate(subjects):
                event_occurrences = ast.literal_eval(subject['plot'])
                row_idx = i // num_cols
                col_idx = i % num_cols
                axs[row_idx, col_idx].eventplot(event_occurrences, lineoffsets=0.2, linelengths=0.1, linewidths=0.5)
                axs[row_idx, col_idx].set_xlabel('Time')
                axs[row_idx, col_idx].set_ylabel('Event')
                axs[row_idx, col_idx].set_title(subject['Subject'])
                axs[row_idx, col_idx].set_yticks([])
                axs[row_idx, col_idx].grid(True)
                axs[row_idx, col_idx].set_xlim(0, max_x_value)

            # Adjust subplot spacing
            fig.subplots_adjust(hspace=0.7, wspace=0.08, left=0.015, right=0.987)
            
            # Save the plot to PDF
            pdf_pages.savefig()

# No need to close the PDF file, it's automatically closed after the 'with' block
