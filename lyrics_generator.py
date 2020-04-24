from textgenrnn import textgenrnn
import os


model_cfg = {
    'rnn_size': 500,
    'rnn_layers': 12,
    'rnn_bidirectional': True,
    'max_length': 15,
    'max_words': 10000,
    'dim_embeddings': 100,
    'word_level': False,
}
train_cfg = {
    'line_delimited': True,
    'num_epochs': 100,
    'gen_epochs': 25,
    'batch_size': 750,
    'train_size': 0.8,
    'dropout': 0.0,
    'max_gen_length': 300,
    'validation': True,
    'is_csv': False
}

textgen_trainer = textgenrnn()
textgen_trainer.train_from_file(os.path.join('scraper', 'combined_files.txt'))
