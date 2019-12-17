class Paper(object):
    """论文类"""
    def __init__(self,
                 title,
                 author,
                 school,
                 degree,
                 year,
                 abstract="",
                 keywords="",
                 advisor="",
                 catalog="",
                 toc=""):
        self.title = title
        self.author = author
        self.school = school
        self.degree = degree
        self.year = year
        self.abstract = abstract
        self.keywords = keywords
        self.advisor = advisor
        self.catalog = catalog
        self.toc = toc