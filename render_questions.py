import os
import pandas as pd
def render_1440p():
    questions = pd.read_csv('questions.csv',escapechar='\\')
    for i in range(len(questions)):
        question_text = questions.iloc[i]['Question']
        template_text = "\\documentclass[varwidth=\\linewidth,convert={density=300,size=1080,outext=.png}]{standalone}\n\\usepackage{amsfonts}\n\\usepackage{amsmath}\n\\usepackage{graphicx}\n\\usepackage{amssymb}\n\\begin{document}" + question_text + "\\end{document}"
        with open('template.tex', 'w') as f:
            f.write(template_text)
        # compile q{i}.png using pdflatex -shell-escape template.tex
        os.system('pdflatex -shell-escape template.tex')
        # move template.png to questions/{i}.png
        os.system('mv template.png questions_1440p/' + str(i) + '.png')
        # remove template files
        os.system('rm template.*')

        answer_text = questions.iloc[i]['Answer']
        template_text = "\\documentclass[varwidth=\\linewidth,convert={density=300,outext=.png}]{standalone}\n\\usepackage{amsfonts}\n\\usepackage{amsmath}\n\\usepackage{graphicx}\n\\usepackage{amssymb}\n\\begin{document}" + answer_text + "\\end{document}"
        with open('template.tex', 'w') as f:
            f.write(template_text)
        # compile a{i}.png using pdflatex -shell-escape template.tex
        os.system('pdflatex -shell-escape template.tex')
        # move template.png to answers/{i}.png
        os.system('mv template.png answers_1440p/' + str(i) + '.png')
        # remove template files
        os.system('rm template.*')

def render_1080p():
    questions = pd.read_csv('questions.csv',escapechar='\\')
    for i in range(len(questions)):
        question_text = questions.iloc[i]['Question']
        template_text = "\\documentclass[varwidth=\\linewidth,convert={density=300,size=810,outext=.png}]{standalone}\n\\usepackage{amsfonts}\n\\usepackage{amsmath}\n\\usepackage{graphicx}\n\\usepackage{amssymb}\n\\begin{document}" + question_text + "\\end{document}"
        with open('template.tex', 'w') as f:
            f.write(template_text)
        # compile q{i}.png using pdflatex -shell-escape template.tex
        os.system('pdflatex -shell-escape template.tex')
        # move template.png to questions/{i}.png
        os.system('mv template.png questions_1080p/' + str(i) + '.png')
        # remove template files
        os.system('rm template.*')

        answer_text = questions.iloc[i]['Answer']
        template_text = "\\documentclass[varwidth=\\linewidth,convert={density=300,outext=.png}]{standalone}\n\\usepackage{amsfonts}\n\\usepackage{amsmath}\n\\usepackage{graphicx}\n\\usepackage{amssymb}\n\\begin{document}" + answer_text + "\\end{document}"
        with open('template.tex', 'w') as f:
            f.write(template_text)
        # compile a{i}.png using pdflatex -shell-escape template.tex
        os.system('pdflatex -shell-escape template.tex')
        # move template.png to answers/{i}.png
        os.system('mv template.png answers_1080p/' + str(i) + '.png')
        # remove template files
        os.system('rm template.*')
render_1440p()
render_1080p()