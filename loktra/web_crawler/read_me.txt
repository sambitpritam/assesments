Description:
	- cree.py will take a keyword or a keyword and a page number as arguments.
	- Even if more arguments are provided while calling the script, it will ignore the arguments that are not required, provided the first argument passed is the page no and second argument passed is the keyword.
	- If the result is more than certain value, say for example, showing items 1-40 of 900+, then the output will be 900. As the web page is able to show only the 900 items.

-----------------------------------------------------------------------------------
packages used:
	sys
	resources
	BeautifulSoup

-----------------------------------------------------------------------------------
Example 1: when only 1 argument is passed
	--python <fileName> <keyword>
	python cree.py shoes


Example 2: when 2 arguments are passed
	--python <fileName> <page_no> <keyword>
	python cree.py 24 shoes