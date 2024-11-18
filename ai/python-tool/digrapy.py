from graphviz import Digraph

def generate_flowchart():
    dot = Digraph(comment='Image Conversion to WebP')

    dot.node('A', 'Start')
    dot.node('B', 'Get current path')
    dot.node('C', 'Define whitelist and directory whitelist')
    dot.node('D', 'For each directory in whitelist_dirs')
    dot.node('E', 'For each file in directory')
    dot.node('F', 'Check if file is in whitelist or directory is in directory whitelist')
    dot.node('G', 'Check if file is an image')
    dot.node('H', 'Open image')
    dot.node('I', 'Check if image is animated')
    dot.node('J', 'Convert image to WebP')
    dot.node('K', 'Check file size')
    dot.node('L', 'Update code references')
    dot.node('M', 'End')

    dot.edges(['AB', 'BC', 'CD', 'DE', 'EF', 'FG', 'GH', 'HI', 'IJ', 'JK', 'KL', 'LM'])

    dot.render('flowchart.gv', view=True)

generate_flowchart()