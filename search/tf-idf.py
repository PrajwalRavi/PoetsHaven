import pickle
filename='freq_doc'

infile=open(filename,'rb')

term_dict=pickle.load(infile)

infile.close()
for key in term_dict.keys():
    for value in term_dict[key]:
