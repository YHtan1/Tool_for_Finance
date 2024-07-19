#print webpage to pdf
#I was looking for a website to print webpages to pdf but couldn't find one
#Made my own html to pdf convertor in python

#import
from pyhtml2pdf import converter

#paste link for webpage in first parameter, name of output pdf in the second parameter
converter.convert(r'D:/Downloads/4.2%20PCA_%20a%20formal%20description%20with%20proofs%20_%20Multivariate%20Statistics.mhtml', 'sample.pdf')
