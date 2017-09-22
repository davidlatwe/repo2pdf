#!/usr/bin/env python

from subprocess import Popen, PIPE
import sys
import os

root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(root, 'vendor/python-pdfkit'))
import pdfkit


def check_dependency():
	"""
	"""
	as_checker = pdfkit.configuration()

	stdout, stderr = Popen(['pygmentize', '-V'], shell= True,
						stdout= PIPE, stderr= PIPE, stdin= PIPE).communicate()
	if stderr:
		raise IOError('No %s executable found: \n%s' % ('Pygments', 'pygmentize'))


if __name__ == '__main__':

	html_path = sys.argv[1]
	pdf_path = sys.argv[2]
	filename = sys.argv[3]
	
	opts = {
		'encoding': 'UTF-8',
		'header-font-name': 'Source Code Pro',
		'header-font-size': 8,
		'header-spacing': 3,
		'header-line': '',
		'header-left': '[[page]] ' + filename,
		'footer-right': '[page]'
	}

	pdfkit.from_file(html_path, pdf_path, options= opts)