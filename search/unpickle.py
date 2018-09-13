import pickle
filename='dictionary1'

infile=open(filename,'rb')

new_dict=pickle.load(infile)

infile.close()
print(new_dict)