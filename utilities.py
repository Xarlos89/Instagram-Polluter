import os
import secret
import shutil


def grabAllPictures(): # Confirms data folder is there, makes new folder in path, moves all photos there, renames all photos. 
	picDir = os.getcwd() + '/Instagram Pictures'
	os.mkdir(picDir) # Make a new directory called '/Instagram Pictures' in the working dir.

	pics = []

	# Get the names of all pictures in every folder
	subfolders = [ f.path for f in os.scandir(os.getcwd()) if f.is_dir() ]
	for folder in subfolders:
		if secret.username in folder:
			i = subfolders.index(folder)
			picFolder = subfolders[i] + '/media/posts/'
			subfolders2 = [ f.name for f in os.scandir(str(picFolder)) if f.is_dir() ]
			for i in subfolders2:
				i = picFolder + i
				# print(i)
				filenames = [ f.name for f in os.scandir(str(i)) if f.is_file() ]
				for name in filenames:
					name = i +'/'+ name
					# print(name)
					pics.append(name)

	# Move files to new dir
	for picture in pics:
		shutil.move(picture, picDir)

	# Rename photos from 1 to x
	newDir = [ f.name for f in os.scandir(str(picDir)) if f.is_file() ]
	count = 1
	for pic in newDir:
		picOld = picDir + '/' + pic
		picNew = picDir + '/' + str(count) + '.jpg'
		count += 1
		os.rename(picOld, picNew)
		print('Your photos can now be found in: ' + picDir)




