from textgenrnn import textgenrnn
import os


textgen_trainer = textgenrnn()
textgen_trainer.train_from_file(os.path.join('scraper', 'medium.txt'), num_epochs=4)

textgen = textgenrnn("textgenrnn_weights.hdf5")
lyrics = textgen.generate(n=20, return_as_list=True)
for row in lyrics:
    print(row)