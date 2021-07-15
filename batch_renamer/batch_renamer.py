import  os

#to be replaced string and file extension filter

search = "file"
replace = "document"

dir_content = os.listdir('.')

docs = [doc for doc in dir_content if os.path.isfile(doc)]
renamed = 0

print(f"{len(docs)} of {len(dir_content)} elements are files.")

# go through all teh files and check if they match the search pattern
for doc in docs:
    # check kif search text is doc name
    if search in doc:

        # replace with given text
        new_name = doc.replace(search, replace)
        os.rename(doc, new_name)
        renamed += 1
        
        print (f"Renamed {doc} to {new_name}")
print(f"Renamed {renamed} of {len(docs)}  files.")
