with open('figures_updated.py', 'r') as f:
    content = f.read()

import re

# We will replace the ylabel blocks in the LAST function (generate_recall_comparison_plots)
# The lines are:
#                 if r == 0 and c == 0:
#                     ax.set_ylabel('Recall $\\Delta$ (%)', color='#1f77b4', fontsize=18)
#                 else:
#                     ax.set_ylabel('')
# We want to add: ax.yaxis.set_label_coords(-0.18, -0.15)

old_left = """                if r == 0 and c == 0:
                    ax.set_ylabel('Recall $\\\\Delta$ (%)', color='#1f77b4', fontsize=18)
                else:
                    ax.set_ylabel('')"""
                    
new_left = """                if r == 0 and c == 0:
                    ax.set_ylabel('Recall $\\\\Delta$ (%)', color='#1f77b4', fontsize=18)
                    ax.yaxis.set_label_coords(-0.18, -0.15)
                else:
                    ax.set_ylabel('')"""

old_right = """                if r == 0 and c == 2:
                    ax_twin.set_ylabel('Absolute Recall@100 (%)', color='#555555', fontsize=18)
                else:
                    ax_twin.set_ylabel('')"""
                    
new_right = """                if r == 0 and c == 2:
                    ax_twin.set_ylabel('Absolute Recall@100 (%)', color='#555555', fontsize=18)
                    ax_twin.yaxis.set_label_coords(1.18, -0.15)
                else:
                    ax_twin.set_ylabel('')"""

# Only replace in the generate_recall_comparison_plots function.
# It is the last block, so we can just use string replace from the end.
parts = content.split('def generate_recall_comparison_plots():')
if len(parts) == 2:
    new_func = parts[1].replace(old_left, new_left).replace(old_right, new_right)
    content = parts[0] + 'def generate_recall_comparison_plots():' + new_func

with open('figures_updated.py', 'w') as f:
    f.write(content)
