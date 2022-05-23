#!/usr/bin/env python3
import sys
from pprint import pprint
from pathlib import Path
from box import Box
import json
from bs4 import BeautifulSoup


def write_text( file_path , text_lines_list ):
	#with open( file_path , 'a', encoding='utf-8' ) as f:
	with open( file_path , 'w', encoding='utf-8' ) as f:
		f.writelines( text_lines_list )

def read_text( file_path ):
	with open( file_path ) as f:
		return f.read().splitlines()


def write_json( file_path , python_object ):
	with open( file_path , 'w', encoding='utf-8' ) as f:
		json.dump( python_object , f , ensure_ascii=False , indent=4 )

def read_json( file_path ):
	with open( file_path ) as f:
		return json.load( f )

# https://pytutorial.com/parse-html-file-beautifulsoup
def parse_view_one( view ):
	# View Two
	if "passage_html" not in view:
		return False
	passage_html = BeautifulSoup( view[ "passage_html" ] , "html.parser" )
	passage_text = passage_html.text.strip()
	answer_html = BeautifulSoup( view[ "answer_html" ] , "html.parser" )
	answer_text = passage_html.text.strip()
	return {
		"passage_html": passage_html ,
		"passage_text": passage_text ,
		"answer_html": answer_html ,
		"answer_text": answer_text
	}

def parse_view_two( view ):
	# View Two
	pprint( view.keys() )
	if "detailed_guidance_html" not in view:
		return False
	explanation_html = BeautifulSoup( view[ "detailed_guidance_html" ] , "html.parser" )
	explanation_text = explanation_html.text.strip()
	# print( explanation_html )
	equations = explanation_html.find_all( "math1" )
	print( equations )
	return {
		"explanation_html": explanation_html ,
		"explanation_text": explanation_text ,
	}

# pandoc -f html+tex_math_dollars+tex_math_single_backslash -t latex


# https://stackoverflow.com/a/11461355
# ghc --make fixmath.hs
# cat input.html | \
# perl -0pe 's/(\$\$?[^\$]+\$\$?)/\<!--MATH$1-->/gm' | \
# pandoc -s --parse-raw -f html -t json | \
# ./fixmath | \
# pandoc -f json -t latex -s > output.tex
if __name__ == "__main__":
	save_file = read_json( "./Physics/Chapter 02.json" )
	for index , question in enumerate( save_file ):
		view_one = parse_view_one( question[ "view_one" ] )
		view_two = parse_view_two( question[ "view_two" ] )
		# pprint( view_two )







