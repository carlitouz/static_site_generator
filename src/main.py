from textnode import TextNode, TextType
import os
import shutil

def copy_static_to_public(source_path, destination_path):
	if os.path.exists(destination_path):
		print(f"Clearing destination path: {destination_path}")
		shutil.rmtree(destination_path)



def main():

if __name__ == "__main__":
	main()
