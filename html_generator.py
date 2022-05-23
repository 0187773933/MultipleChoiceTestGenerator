from box import Box
import json
import base64

def base64_encode( message ):
	try:
		message_bytes = message.encode( 'utf-8' )
		base64_bytes = base64.b64encode( message_bytes )
		base64_message = base64_bytes.decode( 'utf-8' )
		return base64_message
	except Exception as e:
		print( e )
		return False

def generate_passage_version( options ):
	options = Box( options )
	return f'''<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>{options.deck.title}</title>
	<link rel="stylesheet" href="{options.cdn.jquery_ui_css.url}" integrity="{options.cdn.jquery_ui_css.integrity}" >
	<script src="{options.cdn.jquery_js.url}" integrity="{options.cdn.jquery_js.integrity}"></script>
	<link rel="stylesheet" href="{options.cdn.bootstrap_css.url}" integrity="{options.cdn.bootstrap_css.integrity}">
	<script src="{options.cdn.bootstrap_bundle_js.url}" integrity="{options.cdn.bootstrap_bundle_js.integrity}"></script>
	<script src="{options.cdn.jquery_ui_js.url}" integrity="{options.cdn.jquery_ui_js.integrity}" ></script>
	<link rel="stylesheet" href="{options.cdn.katex_css.url}" integrity="{options.cdn.katex_css.integrity}">
	<script src="{options.cdn.katex_js.url}" integrity="{options.cdn.katex_js.integrity}"></script>
	<script src="{options.cdn.mhchem_js.url}" integrity="{options.cdn.mhchem_js.integrity}"></script>
	<script src="{options.cdn.auto_render_js.url}" integrity="{options.cdn.auto_render_js.integrity}"></script>
	<script src="{options.cdn.markdown_it.url}" integrity="{options.cdn.markdown_it.integrity}"></script>
	<style type="text/css">
		body {{
			background-color: #2E3033;
			// color: #b8bfc6;
		}}
		.next-button {{
			text-decoration: none;
			display: inline-block;
			padding: 8px 16px;
			border-radius: 50%;
			background-color: #b7b7b7;
			color: white;
		}}
		.previous-button {{
			text-decoration: none;
			display: inline-block;
			padding: 8px 16px;
			border-radius: 50%;
			background-color: #b7b7b7;
			color: white;
		}}
		.our-no-gutter {{
			margin-left: 0;
			margin-right: 0;
			padding-left: 0;
			padding-right: 0;
		}}
		.slimmed-padding {{
			margin-left: 0 !important;
			margin-right: 0 !important;
			padding-left: 1 !important;
			padding-right: 1 !important;
		}}
		.correct {{
			border: 2px solid green;
		}}
		.tg {{border-collapse:collapse;border-spacing:0;}}
		.tg td{{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
		overflow:hidden;padding:10px 5px;word-break:normal;}}
		.tg th{{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
		font-weight:normal;overflow:hidden;padding:10px 5px;word-break:normal;}}
		.tg .tg-0lax{{text-align:left;vertical-align:top}}
		p {{
  			margin-top: 0;
  			margin-bottom: 0rem !important;
		}}
	</style>
</head>
<body>

	<div class="container-fluid" style="padding-right: var(--bs-gutter-x,.5rem); padding-left: var(--bs-gutter-x,.5rem);" >
		<div class="row g-0">
			<div class="col-6" style="background-color: #61cc9e;">
				<div class="sidebar mw-100" style="padding-top: 1em; padding-left: 1em; padding-right: 3em;">
					<div id="passage"></div>
				</div>
			</div>
			<div class="col-6">
				<div class="main-content mh-100 mw-100">
					<div class="row justify-content-center">
						<div class="col-xs-12 col-sm-12 col-md-12 col-lg-12 ">
							<div class="card" style="background-color: #EFA9AE;">
								<div class="card-header text-center">
									<div id="card-title-content"></div>
								</div>
								<div class="card-body slimmed-padding" id="card-body-container">
									<div id="card-body-content"></div>
								</div>
								<div class="card-body slimmed-padding" id="card-explanation-container">
									<div id="card-explanation-content"></div>
								</div>
							</div>
						</div>
					</div>
					<br></br>
					<div class="row justify-content-center fixed-row-bottom" id="row-navigation">
						<div class="col text-center" style="color: #b8bfc6;">
							<div>
								<span id="current-card-number"></span>&nbsp;&nbsp;&nbsp;
								<span id="previous-button" class="previous-button">&#8249;</span>&nbsp;&nbsp;&nbsp;
								<span id="next-button" class="next-button">&#8250;</span>&nbsp;&nbsp;&nbsp;
								<span id="total-cards"></span>
							</div>
						</div>
					</div>
					<div class="row justify-content-center">
						<div class="col-xs-12 col-sm-12 col-md-12 col-lg-12 our-no-gutter">
							<div id="row-extra-space" style="height: 80vh;"></div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>

	<script type="text/javascript">
		let passage_json_b64_string = "{base64_encode( json.dumps( options.passage ) )}"
		let passage_json_string = window.atob( passage_json_b64_string );
		window.PASSAGE = JSON.parse( passage_json_string );
		let deck_json_b64_string = "{base64_encode( json.dumps( options.deck ) ) }";
		let deck_json_string = window.atob( deck_json_b64_string );
		window.DECK = JSON.parse( deck_json_string );
	</script>

	<script type="text/javascript">
		function setup_hooks() {{
			$( "#previous-button" ).on( "click" , previous_card );
			$( "#next-button" ).on( "click" , next_card );
			$( document ).keydown( function( event ) {{
				switch ( event.keyCode ) {{
					case 32:
						next_card();
						setTimeout( () => {{
							window.scrollTo( 0 , 0 );
						}} , 100 );
						break; // space
					case 37: previous_card(); break; // left arrow
					case 39: next_card(); break; // right arrow
				}}
			}});
		}}
		function previous_card() {{
			let url;
			if ( window.ACTIVE_INDEX === 0 ) {{
				url = window.location.href.split( ".html" )[ 0 ] + ".html" + "#" + ( window.DECK.questions.length ).toString();
			}} else {{
				url = window.location.href.split( ".html" )[ 0 ] + ".html" + "#" + ( window.ACTIVE_INDEX ).toString();
			}}
			window.location.href = url;
			window.ACTIVE_INDEX = ( window.ACTIVE_INDEX - 1 );
			if ( window.ACTIVE_INDEX < 0 ) {{ window.ACTIVE_INDEX = ( window.DECK.questions.length - 1 ); }}
			render_active_card();
		}}
		function next_card() {{
			if ( window.BACK_IS_RENDERED === false ) {{
				render_correct_answers();
				render_explanation();
				render_katex();
				window.BACK_IS_RENDERED = true;
			}} else {{
				window.BACK_IS_RENDERED = false;
				window.ACTIVE_INDEX = ( window.ACTIVE_INDEX + 1 );
				if ( window.ACTIVE_INDEX > ( window.DECK.questions.length - 1 ) ) {{ window.ACTIVE_INDEX = 0; }}
				let url;
				if ( window.ACTIVE_INDEX === ( window.DECK.questions.length ) ) {{
					url = window.location.href.split( ".html" )[ 0 ] + ".html" + "#" + ( window.DECK.questions.length ).toString();
				}} else {{
					url = window.location.href.split( ".html" )[ 0 ] + ".html" + "#" + ( window.ACTIVE_INDEX + 1 ).toString();
				}}
				window.location.href = url;
				render_active_card();
			}}
		}}
		function render_katex() {{
			renderMathInElement( document.body , {{
				strict: "ignore" ,
				delimiters: [ // https://stackoverflow.com/a/45301641
					{{ left: "$$" , right: "$$" , display: true }} ,
					{{ left: "\\[" , right: "\\]" , display: true }} ,
					{{ left: "$" , right: "$" , display: false }} ,
					// {{ left: "\\(" , right: "\\)" , display: false }}
				]
			}});
		}}

		function render_markdown( element_id , markdown_string ) {{
			$( element_id ).empty();
			//$( element_id ).html( markdown_string );
			//render_katex();
			let md = new markdownit( {{ typographer: true , html: true }} )
				//.disable( [ "escape" , "emphasis" ] )
				.disable( [ "escape" ] )
				.enable( [ "image" ] )
				// .disable( [ "escape" ] )
				// .use( markdownItMark )
			;
			let converted_html = md.render( markdown_string );
			$( element_id ).html( converted_html );
		}}


		/*
		// https://github.com/jonschlinkert/remarkable
		var HTML_ESCAPE_TEST_RE = /[&<>"]/;
		var HTML_ESCAPE_REPLACE_RE = /[&<>"]/g;
		// https://github.com/jonschlinkert/remarkable/blob/58b6945f203ca7a0bb5a0785df90a3a6a8b9e59c/lib/common/utils.js#L114
		var HTML_REPLACEMENTS = {{
			'&': '&amp;' ,
  			'"': '&quot;'
		}};
		remarkable.utils.escapeHtml = function(str) {{
			if (HTML_ESCAPE_TEST_RE.test(str)) {{
				return str.replace(HTML_ESCAPE_REPLACE_RE, HTML_REPLACEMENTS[ch]);
			}}
			return str;
		}}
		function render_markdown( element_id , markdown_string ) {{
			$( element_id ).empty();
			$( element_id ).html( markdown_string );
			render_katex();
			const md = new remarkable.Remarkable({{
				html:true
			}});
			// https://github.com/jonschlinkert/remarkable/blob/master/docs/parser.md
			// md.core.ruler.disable([ 'replacements' ]);
			// md.block.ruler.disable([ 'replacements' ]);
			md.inline.ruler.disable([ 'replacements' ]);
			let converted_html = md.render( markdown_string );
			$( element_id ).html( converted_html );
		}}
		*/

		let CHOICES_ENUM = {{}}; [ ...Array( 26 ).keys() ].forEach( i => CHOICES_ENUM[ i ] = String.fromCharCode( i + 65 ) );
		let CHOICES_ENUM_REVERSE_UPPER = {{}}; [ ...Array( 26 ).keys() ].forEach( i => CHOICES_ENUM_REVERSE_UPPER[ String.fromCharCode( i + 65 ) ] = i );
		let CHOICES_ENUM_REVERSE_LOWER = {{}}; [ ...Array( 26 ).keys() ].forEach( i => CHOICES_ENUM_REVERSE_LOWER[ String.fromCharCode( i + 97 ) ] = i );

		function render_correct_answers() {{
			$( "input[type=radio]" ).each( function( element ) {{
				for ( let i = 0; i < window.DECK.questions[ window.ACTIVE_INDEX ].correct_answer_indexes.length; ++i ) {{
					if ( this.value === CHOICES_ENUM[ window.DECK.questions[ window.ACTIVE_INDEX ].correct_answer_indexes[ i ] ] ) {{
						$( this ).next().addClass( "correct" );
					}}
				}}
			}});
		}}
		function render_explanation() {{
			// $( "#card-explanation-content" ).html( `${{window.DECK.questions[ window.ACTIVE_INDEX ].explanation}}` );
			render_markdown( "#card-explanation-content" , window.DECK.questions[ window.ACTIVE_INDEX ].explanation );
		}}
		function render_active_card() {{
			if ( !window.ACTIVE_INDEX ) {{ window.ACTIVE_INDEX = 0; }}

			// build indexes if correct answers sent as letters instead of index numbers
			if ( !window.DECK.questions[ window.ACTIVE_INDEX ].correct_answer_indexes ) {{
				if ( window.DECK.questions[ window.ACTIVE_INDEX ].correct_answers ) {{
					window.DECK.questions[ window.ACTIVE_INDEX ].correct_answer_indexes = [];
					for ( let i = 0; i < window.DECK.questions[ window.ACTIVE_INDEX ].correct_answers.length; ++i ) {{
						if ( window.DECK.questions[ window.ACTIVE_INDEX ].correct_answers[ i ] in CHOICES_ENUM_REVERSE_UPPER ) {{
							window.DECK.questions[ window.ACTIVE_INDEX ].correct_answer_indexes.push( CHOICES_ENUM_REVERSE_UPPER[ window.DECK.questions[ window.ACTIVE_INDEX ].correct_answers[ i ] ] )
						}}
						else if ( window.DECK.questions[ window.ACTIVE_INDEX ].correct_answers[ i ] in CHOICES_ENUM_REVERSE_LOWER ) {{
							window.DECK.questions[ window.ACTIVE_INDEX ].correct_answer_indexes.push( CHOICES_ENUM_REVERSE_LOWER[ window.DECK.questions[ window.ACTIVE_INDEX ].correct_answers[ i ] ] )
						}}
						else if ( isNaN( window.DECK.questions[ window.ACTIVE_INDEX ].correct_answers[ i ] ) === false ) {{
							window.DECK.questions[ window.ACTIVE_INDEX ].correct_answer_indexes.push( ( parseInt( window.DECK.questions[ window.ACTIVE_INDEX ].correct_answers[ i ] ) - 1 ) )
						}}
					}}
				}}
			}}
			$( "#card-explanation-content" ).empty();
			$( "#card-title-content" ).empty();
			// $( "#card-title-content" ).html( `<h3>${{window.DECK.questions[ window.ACTIVE_INDEX ].prompt}}</h3>` );
			render_markdown( "#card-title-content" , window.DECK.questions[ window.ACTIVE_INDEX ].prompt );
			let choices_html_prefix = `<div><form class="input">`;
			let choices_html_body = "";
			for ( let i = 0; i < window.DECK.questions[ window.ACTIVE_INDEX ].choices.length; ++i ) {{
				choices_html_body += `${{CHOICES_ENUM[i]}}.) <input type="radio" name="answer_choice" value="${{CHOICES_ENUM[ i ]}}">&nbsp;<span class="choice_text">${{window.DECK.questions[ window.ACTIVE_INDEX ].choices[ i ]}}</span><br>`;
			}}
			let choices_html_suffix = `</form></div>`;
			let choices_html = choices_html_prefix + choices_html_body + choices_html_suffix;
			$( "#card-body-content" ).html( choices_html );
			$( "input[type=radio]" ).change( function( element ) {{
				for ( let i = 0; i < window.DECK.questions[ window.ACTIVE_INDEX ].correct_answer_indexes.length; ++i ) {{
					if ( this.value === CHOICES_ENUM[ window.DECK.questions[ window.ACTIVE_INDEX ].correct_answer_indexes[ i ] ] ) {{
						$( this ).next().addClass( "correct" );
					}}
				}}
				// if all correct selected , make back rendered true , to avoid double clicking arrows
				let total_correct_answered = 0;
				let input_children = $( "input[type=radio]" ).parent().children();
				for ( let i = 0; i < input_children.length; ++i ) {{
					if ( $( input_children[ i ] ).hasClass( "correct" ) ) {{
						total_correct_answered += 1;
					}}
				}}
				if ( total_correct_answered === window.DECK.questions[ window.ACTIVE_INDEX ].correct_answer_indexes.length ) {{
					window.BACK_IS_RENDERED = true;
					render_explanation();
					render_katex();
				}}
			}});
			$( "#current-card-number" ).text( `${{( window.ACTIVE_INDEX + 1 )}}` );
			render_katex();
			$( window ).scrollTop( 0 );
		}}
		function get_url_question_number() {{
			window.URL_INDEX = window.location.href.split( "#" );
			if ( window.URL_INDEX.length > 0 ) {{
				window.URL_INDEX = window.location.href.split( ".html" )[ 1 ].split( "#" );
				if ( window.URL_INDEX.length > 0 ) {{
					window.URL_INDEX = window.URL_INDEX[ 1 ];
					return window.URL_INDEX;
				}}
			}}
			return false;
		}}
		function init() {{
			$( "#row-grading" ).hide();
			window.ACTIVE_INDEX = 0;
			if ( get_url_question_number() !== false ) {{
				if ( window.URL_INDEX !== window.ACTIVE_INDEX ) {{
					window.ACTIVE_INDEX = ( parseInt( window.URL_INDEX ) - 1 );
				}}
			}}
			window.DOCUMENT_CLICKED = false;
			window.BACK_IS_RENDERED = false;
			setup_hooks();
			// Setup First Card
			$( "#total-cards" ).text( `${{window.DECK.questions.length}}` );
			render_active_card();
			try {{
				render_markdown( "#passage" , window.PASSAGE );
			}} catch( e ) {{}}
			render_katex();
		}}
		document.addEventListener( "DOMContentLoaded" , init );
	</script>
</body>
</html>
'''

def generate( options ):
	options = Box( options )
	return f'''<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>{options.deck.title}</title>
	<link rel="stylesheet" href="{options.cdn.jquery_ui_css.url}" integrity="{options.cdn.jquery_ui_css.integrity}" >
	<script src="{options.cdn.jquery_js.url}" integrity="{options.cdn.jquery_js.integrity}"></script>
	<link rel="stylesheet" href="{options.cdn.bootstrap_css.url}" integrity="{options.cdn.bootstrap_css.integrity}">
	<script src="{options.cdn.bootstrap_bundle_js.url}" integrity="{options.cdn.bootstrap_bundle_js.integrity}"></script>
	<script src="{options.cdn.jquery_ui_js.url}" integrity="{options.cdn.jquery_ui_js.integrity}" ></script>
	<link rel="stylesheet" href="{options.cdn.katex_css.url}" integrity="{options.cdn.katex_css.integrity}">
	<script src="{options.cdn.katex_js.url}" integrity="{options.cdn.katex_js.integrity}"></script>
	<script src="{options.cdn.mhchem_js.url}" integrity="{options.cdn.mhchem_js.integrity}"></script>
	<script src="{options.cdn.auto_render_js.url}" integrity="{options.cdn.auto_render_js.integrity}"></script>
	<script src="{options.cdn.markdown_it.url}" integrity="{options.cdn.markdown_it.integrity}"></script>
	<style type="text/css">
		body {{
			background-color: #2E3033;
			color: #b8bfc6;
		}}
		.next-button {{
			text-decoration: none;
			display: inline-block;
			padding: 8px 16px;
			border-radius: 50%;
			background-color: #b7b7b7;
			color: white;
		}}
		.previous-button {{
			text-decoration: none;
			display: inline-block;
			padding: 8px 16px;
			border-radius: 50%;
			background-color: #b7b7b7;
			color: white;
		}}
		.our-no-gutter {{
			margin-left: 0;
			margin-right: 0;
			padding-left: 0;
			padding-right: 0;
		}}
		.slimmed-padding {{
			margin-left: 0 !important;
			margin-right: 0 !important;
			padding-left: 1 !important;
			padding-right: 1 !important;
		}}
		.correct {{
			border: 2px solid green;
		}}
		.tg {{border-collapse:collapse;border-spacing:0;}}
		.tg td{{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
		overflow:hidden;padding:10px 5px;word-break:normal;}}
		.tg th{{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
		font-weight:normal;overflow:hidden;padding:10px 5px;word-break:normal;}}
		.tg .tg-0lax{{text-align:left;vertical-align:top}}
		p {{
  			margin-top: 0;
  			margin-bottom: 0rem !important;
		}}
	</style>
</head>
<body>
	<div class="container">
		<!-- <div class="row justify-content-center" style="border: 1px solid red"> -->
		<div class="row justify-content-center">
			<div class="col-xs-12 col-sm-12 col-md-12 col-lg-12 our-no-gutter">
				<div class="card" style="background-color: #363B40;">
					<div class="card-header text-center">
						<div id="card-title-content"></div>
					</div>
					<div class="card-body slimmed-padding" id="card-body-container">
						<div id="card-body-content"></div>
					</div>
					<div class="card-body slimmed-padding" id="card-explanation-container">
						<div id="card-explanation-content"></div>
					</div>
				</div>
			</div>
		</div>
		<br></br>
		<div class="row justify-content-center fixed-row-bottom" id="row-navigation">
			<div class="col text-center">
				<div>
					<span id="current-card-number"></span>&nbsp;&nbsp;&nbsp;
					<span id="previous-button" class="previous-button">&#8249;</span>&nbsp;&nbsp;&nbsp;
					<span id="next-button" class="next-button">&#8250;</span>&nbsp;&nbsp;&nbsp;
					<span id="total-cards"></span>
				</div>
			</div>
		</div>
		<div class="row justify-content-center">
			<div class="col-xs-12 col-sm-12 col-md-12 col-lg-12 our-no-gutter">
				<div id="row-extra-space" style="height: 80vh;"></div>
			</div>
		</div>
	</div>

	<script type="text/javascript">
		let deck_json_b64_string = "{base64_encode( json.dumps( options.deck ) ) }";
		let deck_json_string = window.atob( deck_json_b64_string );
		window.DECK = JSON.parse( deck_json_string );
	</script>

	<script type="text/javascript">
		function setup_hooks() {{
			$( "#previous-button" ).on( "click" , previous_card );
			$( "#next-button" ).on( "click" , next_card );
			$( document ).keydown( function( event ) {{
				switch ( event.keyCode ) {{
					case 32:
						next_card();
						break; // space
					case 37:
						previous_card();
						break; // left arrow
					case 39:
						next_card();
						break; // right arrow
				}}
			}});
		}}
		function previous_card() {{
			let url;
			if ( window.ACTIVE_INDEX === 0 ) {{
				url = window.location.href.split( ".html" )[ 0 ] + ".html" + "#" + ( window.DECK.questions.length ).toString();
			}} else {{
				url = window.location.href.split( ".html" )[ 0 ] + ".html" + "#" + ( window.ACTIVE_INDEX ).toString();
			}}
			window.location.href = url;
			window.ACTIVE_INDEX = ( window.ACTIVE_INDEX - 1 );
			if ( window.ACTIVE_INDEX < 0 ) {{ window.ACTIVE_INDEX = ( window.DECK.questions.length - 1 ); }}
			render_active_card();
		}}
		function next_card() {{
			if ( window.BACK_IS_RENDERED === false ) {{
				render_correct_answers();
				render_explanation();
				render_katex();
				window.BACK_IS_RENDERED = true;
			}} else {{
				window.BACK_IS_RENDERED = false;
				window.ACTIVE_INDEX = ( window.ACTIVE_INDEX + 1 );
				if ( window.ACTIVE_INDEX > ( window.DECK.questions.length - 1 ) ) {{ window.ACTIVE_INDEX = 0; }}
				let url;
				if ( window.ACTIVE_INDEX === ( window.DECK.questions.length ) ) {{
					url = window.location.href.split( ".html" )[ 0 ] + ".html" + "#" + ( window.DECK.questions.length ).toString();
				}} else {{
					url = window.location.href.split( ".html" )[ 0 ] + ".html" + "#" + ( window.ACTIVE_INDEX + 1 ).toString();
				}}
				window.location.href = url;
				render_active_card();
			}}
		}}
		function render_katex() {{
			renderMathInElement( document.body , {{
				strict: "ignore" ,
				delimiters: [ // https://stackoverflow.com/a/45301641
					{{ left: "$$" , right: "$$" , display: true }} ,
					{{ left: "\\[" , right: "\\]" , display: true }} ,
					{{ left: "$" , right: "$" , display: false }} ,
					// {{ left: "\\(" , right: "\\)" , display: false }}
				]
			}});
		}}

		function render_markdown( element_id , markdown_string ) {{
			$( element_id ).empty();
			//$( element_id ).html( markdown_string );
			//render_katex();
			let md = new markdownit( {{ typographer: true , html: true }} )
				.disable( [ "escape" , "emphasis" ] )
				.enable( [ "image" ] )
				// .disable( [ "escape" ] )
				// .use( markdownItMark )
			;
			let converted_html = md.render( markdown_string );
			$( element_id ).html( converted_html );
		}}


		/*
		// https://github.com/jonschlinkert/remarkable
		var HTML_ESCAPE_TEST_RE = /[&<>"]/;
		var HTML_ESCAPE_REPLACE_RE = /[&<>"]/g;
		// https://github.com/jonschlinkert/remarkable/blob/58b6945f203ca7a0bb5a0785df90a3a6a8b9e59c/lib/common/utils.js#L114
		var HTML_REPLACEMENTS = {{
			'&': '&amp;' ,
  			'"': '&quot;'
		}};
		remarkable.utils.escapeHtml = function(str) {{
			if (HTML_ESCAPE_TEST_RE.test(str)) {{
				return str.replace(HTML_ESCAPE_REPLACE_RE, HTML_REPLACEMENTS[ch]);
			}}
			return str;
		}}
		function render_markdown( element_id , markdown_string ) {{
			$( element_id ).empty();
			$( element_id ).html( markdown_string );
			render_katex();
			const md = new remarkable.Remarkable({{
				html:true
			}});
			// https://github.com/jonschlinkert/remarkable/blob/master/docs/parser.md
			// md.core.ruler.disable([ 'replacements' ]);
			// md.block.ruler.disable([ 'replacements' ]);
			md.inline.ruler.disable([ 'replacements' ]);
			let converted_html = md.render( markdown_string );
			$( element_id ).html( converted_html );
		}}
		*/

		let CHOICES_ENUM = {{}}; [ ...Array( 26 ).keys() ].forEach( i => CHOICES_ENUM[ i ] = String.fromCharCode( i + 65 ) );
		let CHOICES_ENUM_REVERSE_UPPER = {{}}; [ ...Array( 26 ).keys() ].forEach( i => CHOICES_ENUM_REVERSE_UPPER[ String.fromCharCode( i + 65 ) ] = i );
		let CHOICES_ENUM_REVERSE_LOWER = {{}}; [ ...Array( 26 ).keys() ].forEach( i => CHOICES_ENUM_REVERSE_LOWER[ String.fromCharCode( i + 97 ) ] = i );

		function render_correct_answers() {{
			$( "input[type=radio]" ).each( function( element ) {{
				for ( let i = 0; i < window.DECK.questions[ window.ACTIVE_INDEX ].correct_answer_indexes.length; ++i ) {{
					if ( this.value === CHOICES_ENUM[ window.DECK.questions[ window.ACTIVE_INDEX ].correct_answer_indexes[ i ] ] ) {{
						$( this ).next().addClass( "correct" );
					}}
				}}
			}});
		}}
		function render_explanation() {{
			// $( "#card-explanation-content" ).html( `${{window.DECK.questions[ window.ACTIVE_INDEX ].explanation}}` );
			render_markdown( "#card-explanation-content" , window.DECK.questions[ window.ACTIVE_INDEX ].explanation );
		}}
		function render_active_card() {{
			if ( !window.ACTIVE_INDEX ) {{ window.ACTIVE_INDEX = 0; }}

			// build indexes if correct answers sent as letters instead of index numbers
			if ( !window.DECK.questions[ window.ACTIVE_INDEX ].correct_answer_indexes ) {{
				if ( window.DECK.questions[ window.ACTIVE_INDEX ].correct_answers ) {{
					window.DECK.questions[ window.ACTIVE_INDEX ].correct_answer_indexes = [];
					for ( let i = 0; i < window.DECK.questions[ window.ACTIVE_INDEX ].correct_answers.length; ++i ) {{
						if ( window.DECK.questions[ window.ACTIVE_INDEX ].correct_answers[ i ] in CHOICES_ENUM_REVERSE_UPPER ) {{
							window.DECK.questions[ window.ACTIVE_INDEX ].correct_answer_indexes.push( CHOICES_ENUM_REVERSE_UPPER[ window.DECK.questions[ window.ACTIVE_INDEX ].correct_answers[ i ] ] )
						}}
						else if ( window.DECK.questions[ window.ACTIVE_INDEX ].correct_answers[ i ] in CHOICES_ENUM_REVERSE_LOWER ) {{
							window.DECK.questions[ window.ACTIVE_INDEX ].correct_answer_indexes.push( CHOICES_ENUM_REVERSE_LOWER[ window.DECK.questions[ window.ACTIVE_INDEX ].correct_answers[ i ] ] )
						}}
						else if ( isNaN( window.DECK.questions[ window.ACTIVE_INDEX ].correct_answers[ i ] ) === false ) {{
							window.DECK.questions[ window.ACTIVE_INDEX ].correct_answer_indexes.push( ( parseInt( window.DECK.questions[ window.ACTIVE_INDEX ].correct_answers[ i ] ) - 1 ) )
						}}
					}}
				}}
			}}

			$( "#card-explanation-content" ).empty();
			$( "#card-title-content" ).empty();
			// $( "#card-title-content" ).html( `<h3>${{window.DECK.questions[ window.ACTIVE_INDEX ].prompt}}</h3>` );
			render_markdown( "#card-title-content" , window.DECK.questions[ window.ACTIVE_INDEX ].prompt );
			let choices_html_prefix = `<div><form class="input">`;
			let choices_html_body = "";
			for ( let i = 0; i < window.DECK.questions[ window.ACTIVE_INDEX ].choices.length; ++i ) {{
				choices_html_body += `${{CHOICES_ENUM[i]}}.) <input type="radio" name="answer_choice" value="${{CHOICES_ENUM[ i ]}}">&nbsp;<span class="choice_text">${{window.DECK.questions[ window.ACTIVE_INDEX ].choices[ i ]}}</span><br>`;
			}}
			let choices_html_suffix = `</form></div>`;
			let choices_html = choices_html_prefix + choices_html_body + choices_html_suffix;
			$( "#card-body-content" ).html( choices_html );
			$( "input[type=radio]" ).change( function( element ) {{
				for ( let i = 0; i < window.DECK.questions[ window.ACTIVE_INDEX ].correct_answer_indexes.length; ++i ) {{
					if ( this.value === CHOICES_ENUM[ window.DECK.questions[ window.ACTIVE_INDEX ].correct_answer_indexes[ i ] ] ) {{
						$( this ).next().addClass( "correct" );
					}}
				}}
				// if all correct selected , make back rendered true , to avoid double clicking arrows
				let total_correct_answered = 0;
				let input_children = $( "input[type=radio]" ).parent().children();
				for ( let i = 0; i < input_children.length; ++i ) {{
					if ( $( input_children[ i ] ).hasClass( "correct" ) ) {{
						total_correct_answered += 1;
					}}
				}}
				if ( total_correct_answered === window.DECK.questions[ window.ACTIVE_INDEX ].correct_answer_indexes.length ) {{
					window.BACK_IS_RENDERED = true;
					render_explanation();
					render_katex();
				}}
			}});
			$( "#current-card-number" ).text( `${{( window.ACTIVE_INDEX + 1 )}}` );
			render_katex();
			$( window ).scrollTop( 0 );
		}}
		function get_url_question_number() {{
			window.URL_INDEX = window.location.href.split( "#" );
			if ( window.URL_INDEX.length > 0 ) {{
				window.URL_INDEX = window.location.href.split( ".html" )[ 1 ].split( "#" );
				if ( window.URL_INDEX.length > 0 ) {{
					window.URL_INDEX = window.URL_INDEX[ 1 ];
					return window.URL_INDEX;
				}}
			}}
			return false;
		}}
		function init() {{
			render_katex();
			$( "#row-grading" ).hide();
			window.ACTIVE_INDEX = 0;
			if ( get_url_question_number() !== false ) {{
				if ( window.URL_INDEX !== window.ACTIVE_INDEX ) {{
					window.ACTIVE_INDEX = ( parseInt( window.URL_INDEX ) - 1 );
				}}
			}}
			window.DOCUMENT_CLICKED = false;
			window.BACK_IS_RENDERED = false;
			setup_hooks();
			// Setup First Card
			$( "#total-cards" ).text( `${{window.DECK.questions.length}}` );
			render_active_card();
		}}
		document.addEventListener( "DOMContentLoaded" , init );
	</script>
</body>
</html>
'''