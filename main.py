#!/usr/bin/env python3
import sys
from pathlib import Path
import markdown
from pprint import pprint

import html_generator

def write_text( file_path , text_lines_list ):
	with open( file_path , 'w', encoding='utf-8' ) as f:
		f.writelines( text_lines_list )

def read_text( file_path ):
	with open( file_path ) as f:
		# return f.read().splitlines()
		return f.read()

def parse_questions( markdown_blob ):
	question_regions = markdown_blob.split( "##" )
	parsed_questions = []
	for question_index , question in enumerate( question_regions[ 1 : ] ):
		try:
			parsed = {}
			# parsed[ "prompt" ] = markdown.markdown( question.split( "CHOICES" )[ 0 ][ 1 : ].rstrip( "\n\n" ) )
			parsed[ "prompt" ] = "## " + question.split( "CHOICES" )[ 0 ][ 1 : ].rstrip( "\n\n" )
			parsed[ "choices" ] = question.split( "CHOICES" )[ 1 ].split( "ANSWER = " )[ 0 ].lstrip( "\n\n" ).rstrip( "\n\n" ).split( "\n" )
			parsed[ "choices" ] = [ x.lstrip( "- " ) for x in parsed[ "choices" ] ]
			parsed[ "correct_answers" ] = question.split( "ANSWER = " )[ 1 ].split( "\n" )[ 0 ].split( "," )
			parsed[ "correct_answers" ] = [ x.strip() for x in parsed[ "correct_answers" ] ]

			# parsed[ "explanation" ] = markdown.markdown( "\n".join( question.split( "ANSWER = " )[ 1 ].split( "\n" )[ 1 : ] ).lstrip( "\n" ).rstrip( "\n\n" ) )
			# https://github.com/Python-Markdown/markdown/blob/a11431539d08e14b0bd821ceb101fa59d6a74c8a/markdown/serializers.py#L80=
			# https://github.com/Python-Markdown/markdown/blob/master/markdown/core.py#L258=
			# x = markdown.Markdown( output_format="html5" )
			# x.ESCAPED_CHARS = ['\\', '`', '*', '_', '{', '}', '[', ']', '(', ')', '>', '#', '+', '-', '.', '!']
			# x.ESCAPED_CHARS = [ '`', '*', '_', '{', '}', '[', ']', '#', '+', '-', '.', '!' ]
			# x.block_level_elements.append( "img" )
			# change pypi markdown --> serializers.py#L72 --> comment out < and > escape
			# parsed[ "explanation" ] = x.convert( "\n".join( question.split( "ANSWER = " )[ 1 ].split( "\n" )[ 1 : ] ).lstrip( "\n" ).rstrip( "\n\n" ) )
			parsed[ "explanation" ] = "\n".join( question.split( "ANSWER = " )[ 1 ].split( "\n" )[ 1 : ] ).lstrip( "\n" ).rstrip( "\n\n" )
			parsed_questions.append( parsed )
		except Exception as e:
			print( e )
			print( "Couldn't Parse MD Question File" )
	return parsed_questions

# https://katex.org/docs/autorender.html
# https://stackoverflow.com/questions/54289738/jquery-ui-link-to-get-always-the-very-last-version-of-jquery-ui-min-js
# https://getbootstrap.com/docs/4.0/getting-started/contents/

# [ ...document.querySelectorAll( ".answer-selection__text" ) ].map( x => x.innerText ).join( "\n" )

PUBLIC_CDN = {
	"jquery-ui.css": {
		"url": "https://cdn.jsdelivr.net/npm/jquery-ui-dist/jquery-ui.min.css" ,
		"integrity": ""
	} ,
	"jquery.js": {
		"url": "https://cdn.jsdelivr.net/npm/jquery@3.6.0/dist/jquery.min.js" ,
		"integrity": ""
	} ,
	"bootstrap.css": {
		"url": "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" ,
		"integrity": ""
	} ,
	"bootstrap.bundle.js": {
		"url": "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.min.js" ,
		# "url": "https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/5.0.0-alpha1/js/bootstrap.bundle.min.js" ,
		"integrity": ""
	} ,
	"jquery-ui.js": {
		"url": "https://cdn.jsdelivr.net/npm/jquery-ui-dist/jquery-ui.min.js" ,
		"integrity": ""
	} ,
	"katex.css": {
		"url": "https://cdn.jsdelivr.net/npm/katex@0.15.3/dist/katex.min.css" ,
		"integrity": ""
	} ,
	"katex.js": {
		"url": "https://cdn.jsdelivr.net/npm/katex@0.15.3/dist/katex.min.js" ,
		"integrity": ""
	} ,
	"mhchem.js": {
		"url": "https://cdn.jsdelivr.net/npm/katex@0.15.3/dist/contrib/mhchem.min.js" ,
		"integrity": ""
	} ,
	"auto-render.js": {
		"url": "https://cdn.jsdelivr.net/npm/katex@0.15.3/dist/contrib/auto-render.min.js" ,
		"integrity": ""
	} ,
	"markdown-it": {
		"url": "https://cdn.jsdelivr.net/npm/markdown-it@13.0.1/dist/markdown-it.min.js" ,
		"integrity": ""
	}
}

import private_cdn

if __name__ == "__main__":
	input_file_path = Path( sys.argv[ 1 ] )
	md_text = read_text( str( input_file_path ) )
	questions = parse_questions( md_text )
	html = html_generator.generate({
		"deck": {
			"title": input_file_path.stem ,
			"questions": questions
		} ,
		# "cdn": private_cdn.PRIVATE_CDN
		"cdn": PUBLIC_CDN

	})
	write_text( input_file_path.parent.joinpath( f"{input_file_path.stem}.html" ) , html )