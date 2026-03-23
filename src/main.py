from copystatic import copy_static
from generate_page import generate_page_recursive
import sys


def main():
	basepath = sys.argv
	if len(basepath) > 1:
		basepath = basepath[1]
	else:
		basepath = "/"
	
	copy_static("static", "docs")
	generate_page_recursive(basepath, "content", "template.html", "docs")

if __name__ == "__main__":
	main()
