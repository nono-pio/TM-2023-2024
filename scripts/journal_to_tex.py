MOUNTH = [
    "janvier",
    "fevrier",
    "mars",
    "avril",
    "mai",
    "juin",
    "juillet",
    "aout",
    "septembre",
    "octobre",
    "novembre",
    "decembre",
]

exemple = """
\\documentclass[12pt,a4paper]{article}

\\usepackage[utf8]{inputenc}

\\author{Nolan Piccand}
\\title{Journal de Bord}

\\begin{document}

\\maketitle

\\tableofcontents

\\newpage

\\section{Septembre}

\\subsection{Semaine 3 au 9 septembre}

\\begin{description}
   \\item[3 Septembre] Regarder sur Wikipédia
   \\item[9 Septembre] Lu un livre
\\end{description}


\\subsection{Semaine 3 au 9 septembre}

\\begin{description}
   \\item[3 Septembre] Regarder sur Wikipédia
   \\item[9 Septembre] Lu un livre
\\end{description}

\\subsection{Semaine 3 au 9 septembre}

\\begin{description}
   \\item[3 Septembre] Regarder sur Wikipédia
   \\item[9 Septembre] Lu un livre
\\end{description}



\\section{Octobre}

\\subsection{Semaine 3 au 9 septembre}

\\begin{description}
   \\item[3 Septembre] Regarder sur Wikipédia
   \\item[9 Septembre] Lu un livre
\\end{description}


\\subsection{Semaine 3 au 9 septembre}

\\begin{description}
   \\item[3 Septembre] Regarder sur Wikipédia
   \\item[9 Septembre] Lu un livre
\\end{description}

\\subsection{Semaine 3 au 9 septembre}

\\begin{description}
   \\item[3 Septembre] Regarder sur Wikipédia
   \\item[9 Septembre] Lu un livre
\\end{description}

\\end{document}
"""

TITLE = "Journal de Bord"
AUTHOR = "Nolan Piccand"


def day_section(day: int, mounth: str, note_content: list[str]) -> str:
    content = "".join(note_content)

    return f"\t\\item[{day} {mounth.capitalize()}] {content}"


def week_section(
    week_start: int, week_end: int, mounth: str, day_content: list[str]
) -> str:
    content = "\n".join(day_content)

    return f"""\\subsection{{Semaine {week_start} au {week_end} {mounth}}}

\\begin{{description}}
{content}
\\end{{description}}
"""


def mounth_section(mounth: str, week_content: list[str]) -> str:
    content = "\n".join(week_content)
    return f"""\\section{'{'+mounth.capitalize()+'}'}
    
{content}"""


def make_file_text(mounth_content: list[str]) -> str:
    content = "\n".join(mounth_content)
    return f"""\\documentclass[12pt,a4paper]{{article}}

\\usepackage[utf8]{{inputenc}}

\\author{'{'+AUTHOR+'}'}
\\title{'{'+TITLE+'}'}

\\begin{{document}}

\\maketitle
\\tableofcontents
\\newpage

{content}

\\end{{document}}"""


print(
    make_file_text(
        [
            mounth_section(
                MOUNTH[0],
                [
                    week_section(
                        3,
                        9,
                        MOUNTH[0],
                        [
                            day_section(3, MOUNTH[0], ["Regarder sur Wikipédia"]),
                            day_section(4, MOUNTH[0], ["Regarder sur Wiki"]),
                        ],
                    ),
                    week_section(9, 56, MOUNTH[0], []),
                ],
            ),
            mounth_section(MOUNTH[1], []),
        ]
    )
)
