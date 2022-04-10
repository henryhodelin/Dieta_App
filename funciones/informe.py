
plantilla = """
\documentclass[final]{beamer}

\\usepackage[size=a0,orientation=portrait,scale=1.1]{beamerposter}

\\usetheme{gemini}

\\usecolortheme{seagull}

\\useinnertheme{rectangles}

\\usepackage[utf8]{inputenc}

\\usepackage{graphicx}

\\usepackage{booktabs}

\\usepackage{tikz}

\\usepackage{pgfplots}

\\newlength{\sepwidth}

\\newlength{\colwidth}

\\setlength{\sepwidth}{0.03\paperwidth}

\\setlength{\colwidth}{0.45\paperwidth}

\\newcommand{\separatorcolumn}{\\begin{column}{\sepwidth}\end{column}}

\\footercontent{
	
    FECHA \hfill
	\insertdate \hfill
	\href{mailto:myemail@exampl.com}{\\texttt{myemail@example.com}}
}

\input{custom-defs.tex}

%% Reference Sources
\\addbibresource{refs.bib}

\\renewcommand{\pgfuseimage}[1]{\includegraphics[scale=2.0]{#1}}

\\title{A Beamer Poster Template with Logos based on Gemini Theme}

\\author{Alyssa P. Hacker \inst{1} \and Ben Bitdiddle \inst{2} \and Lem E. Tweakit \inst{2}}

\\institute[shortinst]{\inst{1} Some Institute \samelineand \inst{2} Another Institute}

\\date{January 01, 2025}

\\begin{document}

\\begin{block}{A block title}
		
		This poster was made by modifying the Gemini Beamer Poster Theme~\parencite{Athalye2018} and the Beamer \texttt{seagull} Color Theme.
		Some block contents, followed by a diagram, followed by a dummy paragraph.
		
		\\begin{figure}
			\centering
			\\begin{tikzpicture}[scale=6]
				\draw[step=0.25cm,color=gray] (-1,-1) grid (1,1);
				\draw (1,0) -- (0.2,0.2) -- (0,1) -- (-0.2,0.2) -- (-1,0)
				-- (-0.2,-0.2) -- (0,-1) -- (0.2,-0.2) -- cycle;
			\end{tikzpicture}
			\caption{A figure caption.}
		\end{figure}
		
		Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi ultricies
		eget libero ac ullamcorper. Integer et euismod ante. Aenean vestibulum
		lobortis augue, ut lobortis turpis rhoncus sed. Proin feugiat nibh a
		lacinia dignissim. Proin scelerisque, risus eget tempor fermentum, ex
		turpis condimentum urna, quis malesuada sapien arcu eu purus.
		
	\end{block}

\\end{document}
"""

article = """

\documentclass[a4paper]{article}


\\usepackage[pages=all, color=black, position={current page.south}, placement=bottom, scale=1, opacity=1, vshift=5mm]{background}

\\title{A simple article template}

\\author{Author One}

\\begin{document}

\\maketitle
	
\\begin{abstract}

		
\\noindent \\textbf{Keywords:} article, template, simple

Hola esto es una prueba

\\end{abstract}

\\section{Introduction}

Aqui esta todo muy tranquilo espero que las cosas salgan bien

\\end{document}
"""

preheader =  """

\documentclass[a4paper]{article}


\\usepackage[pages=all, color=black, position={current page.south}, placement=bottom, scale=1, opacity=1, vshift=5mm]{background}

"""

header = """
\\title{A simple article template}

\\author{Author One}

\\begin{document}

\\maketitle
	
\\begin{abstract}

{}
"""

def create_preheader(Titulo, Autor):
    inicio  = """

\documentclass[a4paper]{article}


\\usepackage[pages=all, color=black, position={current page.south}, placement=bottom, scale=1, opacity=1, vshift=5mm]{background}

"""
    insert_title = '\\title{' + Titulo + '}' 

    insert_autor =  """

\\author{"""+Autor+'}'

    
    last_preheader = """

\\begin{document}

\\maketitle
    """

    header = inicio + insert_title + insert_autor + last_preheader

    return header 

def insert_abstract():

    resumen = """
    
    
    """

    return resumen
