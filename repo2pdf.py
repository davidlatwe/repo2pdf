"""Repo2PDF Command-line Interface

- https://github.com/davidlatwe/repo2pdf
Convert whole repository into PDF files for printing.
Dependency:
	- Pygments
	- wkhtmltopdf

Usage: repo2pdf [REPOPATH] [--tab-width INT_VALUE] [--ignore-git]
		[--keep-html] [--debug-html] [--debug-pdf]
		[--version] [--help]
	
"""

from subprocess import Popen, PIPE
import os
import sys
import re

import pdfquiet


def repo2pdf(
		repo,
		keep_html= False,
		tab_width= 4,
		ignore_git= False,
		debug_html= False,
		debug_pdf= False):
	"""
	"""
	# check
	pdfquiet.check_dependency()

	print('Prepare to convert : %s' % repo)

	# check if dir exists
	if not os.path.isdir(repo):
		print("Directory doesn\'t exists.\n%s" % repo)
		sys.exit(1)

	# change dir
	os.chdir(repo)

	# grab files
	file_list = []
	if os.path.isfile('./.gitignore') and not ignore_git:
		# filter out with .gitignore, if that exists
		sh_exe = 'sh.exe'
		sh_cmd = '( git status --short| grep "^?" | \
					cut -d\  -f2- && git ls-files ) | sort -u'

		git_file_list = Popen([sh_exe, '-c', sh_cmd],
			shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE)
		stdout, stderr = git_file_list.communicate()

		if stderr:
			print("[!!!] ERROR filtering with .gitignore :\n%s" % stderr)
			sys.exit(1)
		if stdout:
			file_list = stdout.split()
			file_list.remove('.gitignore')
	else:
		# list all files
		for dirpath, dnames, fnames in os.walk('./'):
			for fn in fnames:
				file_list.append(os.path.join(dirpath, fn)[2:])

	# make PDF root dir
	root_dir = os.path.dirname(repo)
	git_name = os.path.basename(repo)
	pdf_name = git_name + '_PDF'
	pdf_repo = os.path.join(root_dir, pdf_name)
	if not os.path.isdir(pdf_repo):
		os.mkdir(pdf_repo)

	# change dir
	os.chdir(root_dir)

	# convert to HTML and PDF
	for i, fn in enumerate(file_list):
		file_path = os.path.join(git_name, fn)
		html_path = os.path.join(pdf_name, fn + '__.html')
		html_dir = os.path.dirname(html_path)
		step = int(float(i) / len(file_list) * 100)
		# make dir
		if not os.path.isdir(html_dir):
			os.makedirs(html_dir)

		# convert to HTML
		cmd_list = [
			'pygmentize',
			'-O',
			'full,style=arduino,linenos=1',
			'-o',
			html_path,
			file_path
		]
		mkhtml = Popen(cmd_list,
			shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE)
		stdout, stderr = mkhtml.communicate()
		print('\n% 3d%%... HTML [%s] %s' % (
							step,
							' ' if stderr else 'x',
							file_path))
		if stderr:
			if debug_html:
				print('- '*40)
				print(stdout)
				print('- '*40)
				print('x '*40)
				print(stderr)
				print('x '*40)
			continue

		# convert tab to space
		if tab_width:
			html_file = ''
			with open(html_path) as f:
				html_file = f.read()
			spaces = ' ' * tab_width
			html_file = re.sub('\t', spaces, html_file)
			with open(html_path, "w") as f:
				f.write(html_file)
		
		# convert to PDF
		pdf_path = os.path.join(pdf_name, fn + '__.pdf')
		cmd_list = [
			'python',
			pdfquiet.__file__,
			html_path,
			pdf_path,
			fn
		]
		mkpdf = Popen(cmd_list,
			shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE)
		stdout, stderr = mkpdf.communicate()
		print('         PDF [%s] %s' % (' ' if stderr else 'x', file_path))
		if stderr:
			if debug_pdf:
				print('- '*40)
				print(stdout)
				print('- '*40)
				print('x '*40)
				print(stderr)
				print('x '*40)

		# remove HTML
		if not keep_html:
			try:
				os.remove(html_path)
				print('         del [x] %s' % html_path)
			except:
				print('         del [ ] %s' % html_path)

	print('Done.')


def main():
	import argparse

	parser = argparse.ArgumentParser(usage=__doc__)

	parser.add_argument('REPOPATH', action= 'store', type=str,
		help= 'Repository path. If input "demo", will convert this repo \
		[repo2pdf] as demonstration')

	parser.add_argument('--tab-width', dest= 'tab_width', type= int,
		default= 4,	help= 'Convert tabs to spaces before convet to PDF, \
		input tab_width number. Default is 4.')

	parser.add_argument('--ignore-git', dest= 'ignore_git',
		action= 'store_true', help= 'Ignore git, this will grab all files, \
		include submodules.')

	parser.add_argument('--keep-html', dest= 'keep_html',
		action= 'store_true', help= 'Keep .html files after PDF generated.')
	
	parser.add_argument('--debug-html', dest= 'debug_html',
		action= 'store_true', help= 'Print out error during HTML convert.')
	
	parser.add_argument('--debug-pdf', dest= 'debug_pdf',
		action= 'store_true', help= 'Print out error during PDF convert.')

	parser.add_argument('--version', action= 'version',
		version= '%(prog)s 1.0')
	
	kwargs, args = parser.parse_known_args()

	if kwargs.REPOPATH == 'demo':
		kwargs.REPOPATH = os.path.dirname(__file__)
	
	repo2pdf(
		kwargs.REPOPATH,
		keep_html= kwargs.keep_html,
		tab_width= kwargs.tab_width,
		ignore_git= kwargs.ignore_git,
		debug_html= kwargs.debug_html,
		debug_pdf= kwargs.debug_pdf
		)
	
	sys.exit(0)


if __name__ == '__main__':
	main()
