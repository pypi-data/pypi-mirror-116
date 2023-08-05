# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/08_dataloaders.ipynb (unless otherwise specified).

__all__ = ['batch_sequences', 'lm_collate', 'sequence_prediction_collate', 'vector_collate', 'vec_to_text_collate',
           'vector_prediction_collate', 'collate_ds', 'Base_Dataset', 'Text_Dataset', 'Text_Prediction_Dataset',
           'Vector_Dataset', 'Vec_To_Text_Dataset', 'Vec_Prediction_Dataset']

# Cell
from .imports import *
from .torch_imports import *
from .torch_core import *
from .vocab import *

# Cell

def batch_sequences(sequences, pad_idx):
    'Packs `sequences` into a dense tensor, using `pad_idx` for padding'
    max_len = max([len(i) for i in sequences])+1
    bs = len(sequences)

    batch_tensor = torch.zeros((bs, max_len)).long() + pad_idx

    for i,item in enumerate(sequences):
        batch_tensor[i,:item.shape[0]] = item

    return batch_tensor


def lm_collate(batch, pad_idx, batch_first=True):
    '''
    Collate function for language models. Returns packed
    batch for next-token prediction
    '''

    x_tensor = batch_sequences([i[0] for i in batch], pad_idx)

    if isinstance(batch[0][1], torch.Tensor):
        y_tensor = batch_sequences([i[1] for i in batch], pad_idx)
    else:
        y_tensor = x_tensor

    if batch_first:
        output = (x_tensor[:,:-1], y_tensor[:,1:])
    else:
        x_tensor = x_tensor.T
        y_tensor = y_tensor.T
        output = (x_tensor[:-1,:], y_tensor[1:,:])

    return output

def sequence_prediction_collate(batch, pad_idx, batch_first=True):
    '''
    Collate function for predicting some y value from a sequence
    '''
    batch_tensor = batch_sequences([i[0] for i in batch], pad_idx)
    y_vals = torch.stack([i[1] for i in batch])
    y_vals = y_vals.squeeze(-1)

    if not batch_first:
        batch_tensor = batch_tensor.T

    return (batch_tensor, y_vals)


# Cell

def vector_collate(batch):
    '''
    Collate function for vectors
    '''
    fps = torch.stack(batch)
    return fps

def vec_to_text_collate(batch, pad_idx, batch_first=True):
    '''
    Collate function for predicting a sequence from an input vector where
    `batch_tensor` is needed for input (ie predict SMILES from properties)
    '''
    fps = torch.stack([i[0] for i in batch])
    batch_tensor = batch_sequences([i[1] for i in batch], pad_idx)

    if batch_first:
        output = ((batch_tensor[:,:-1], fps), batch_tensor[:,1:])
    else:
        batch_tensor = batch_tensor.T
        output = ((batch_tensor[:-1,:], fps), batch_tensor[1:,:])

    return output

def vector_prediction_collate(batch):
    '''
    Collate function for predicting some y value from a vector
    '''
    fps = torch.stack([i[0] for i in batch])
    y_vals = torch.stack([i[1] for i in batch])
    y_vals = y_vals.squeeze(-1)
    return (fps, y_vals)

# Cell

def collate_ds(ds):
    batch = ds.collate_function([ds[i] for i in range(len(ds))])
    return batch

# Cell

class Base_Dataset(Dataset):
    '''
    BaseDataset - base dataset

    Inputs:

    - `collate_function Callable`: batch collate function for the particular dataset class
    '''
    def __init__(self, collate_function):
        self.collate_function = collate_function

    def __len__(self):
        raise NotImplementedError

    def __getitem__(self, idx):
        raise NotImplementedError

    def dataloader(self, bs, num_workers=-1, **dl_kwargs):
        if num_workers==-1:
            if 'ncpus' in os.environ.keys():
                num_workers = int(os.environ['ncpus'])
            else:
                num_workers=os.cpu_count()

        return DataLoader(self, batch_size=bs, num_workers=num_workers,
                          collate_fn=self.collate_function, **dl_kwargs)

    def new(self):
        raise NotImplementedError

    def split(self, percent_valid, seed=0):

        idxs = np.arange(self.__len__())
        np.random.seed(seed)
        np.random.shuffle(idxs)

#         torch.manual_seed(seed)
#         idxs = torch.randperm(self.__len__()).numpy()
        train_length = int(self.__len__()*(1-percent_valid))

        train_idxs = idxs[:train_length]
        valid_idxs = idxs[train_length:]

        return self.split_on_idxs(train_idxs, valid_idxs)

    def split_on_idxs(self, train_idxs, valid_idxs):
        raise NotImplementedError

# Cell

class Text_Dataset(Base_Dataset):
    '''
    Text_Dataset - base dataset for language modes

    Inputs:

    - `sequences [list[str], list[tuple]]`: list of text sequences or text tuples (source, target)

    - `vocab Vocab`: vocabuary for tokenization/numericaization

    - `collate_function Callable`: batch collate function. If None, defauts to `lm_collate`

    If `sequences` is a list of strings, `__getitem__` returns a tuple of `(sequence_ints, None)`.
    This is suitable for language modeling where the goal is to predict the input sequence.

    If `sequences` is a list of tuples, `__getitem__` returns a tuple of
    `(input_sequence_ints, output_sequence_ints)`. This is suitable for seq-to-seq tasks where
    the predicted sequence is different from the input sequence
    '''
    def __init__(self, sequences, vocab, collate_function=None):
        self.sequences = sequences
        self.vocab = vocab
        if collate_function is None:
            collate_function = partial(lm_collate, pad_idx=self.vocab.stoi['pad'])

        super().__init__(collate_function)

    def __len__(self):
        return len(self.sequences)

    def numericalize(self, sequence):
        tokens = self.vocab.tokenize(sequence)
        ints = self.vocab.numericalize(tokens)
        ints = torch.LongTensor(ints)
        return ints

    def __getitem__(self, idx):
        sequence = self.sequences[idx]

        if type(sequence)==tuple:
            outputs = (self.numericalize(sequence[0]),
                       self.numericalize(sequence[1]))
        else:
            outputs = (self.numericalize(sequence), None)

        return outputs

    def new(self, sequences):
        return self.__class__(sequences, self.vocab, self.collate_function)

    def split_on_idxs(self, train_idxs, valid_idxs):

        train_ds = self.new([self.sequences[i] for i in train_idxs])
        valid_ds = self.new([self.sequences[i] for i in valid_idxs])
        return (train_ds, valid_ds)


# Cell

class Text_Prediction_Dataset(Text_Dataset):
    '''
    Text_Prediction_Dataset - base dataset for predicting from text strings

    Inputs:

    - `sequences list[str]`: list of text sequences

    - `y_vals list[int, float]`: list of paired output values

    - `vocab Vocab`: vocabuary for tokenization/numericaization

    - `collate_function Callable`: batch collate function. If None, defauts to `sequence_prediction_collate`

    `__getitem__` returns a tuple of `(sequence_ints, y_vals)` suitable for predicting
    regressions or classifications from the sequence
    '''
    def __init__(self, sequences, y_vals, vocab, collate_function=None):

        if collate_function is None:
            collate_function = partial(sequence_prediction_collate, pad_idx=vocab.stoi['pad'])

        super().__init__(sequences, vocab, collate_function)

        self.y_vals = y_vals

    def __getitem__(self, idx):
        ints = super().__getitem__(idx)[0]
        y_val = torch.Tensor([self.y_vals[idx]]).float()
        return (ints, y_val)

    def new(self, sequences, y_vals):
        return self.__class__(sequences, y_vals, self.vocab, self.collate_function)

    def split_on_idxs(self, train_idxs, valid_idxs):

        train_ds = self.new([self.sequences[i] for i in train_idxs],
                            [self.y_vals[i] for i in train_idxs])
        valid_ds = self.new([self.sequences[i] for i in valid_idxs],
                            [self.y_vals[i] for i in valid_idxs])

        return (train_ds, valid_ds)


# Cell

class Vector_Dataset(Base_Dataset):
    '''
    Vector_Dataset - base dataset for molecule-derived vectors

    Inputs:

    - `sequences list[str]`: list of text sequences

    - `vec_function Callable`: function to convert sequence to a vector

    - `collate_function Callable`: batch collate function. If None, defauts to `vector_collate`
    '''
    def __init__(self, sequences, vec_function, collate_function=None):
        if collate_function is None:
            collate_function = vector_collate
        super().__init__(collate_function)

        self.sequences = sequences
        self.vec_function = vec_function

    def __len__(self):
        return len(self.sequences)

    def __getitem__(self, idx):
        sequence = self.sequences[idx]
        vec = self.vec_function(sequence)
        vec = torch.FloatTensor(vec)
        return vec

    def new(self, sequences):
        return self.__class__(sequences, self.vec_function, self.collate_function)

    def split_on_idxs(self, train_idxs, valid_idxs):

        train_ds = self.new([self.sequences[i] for i in train_idxs])
        valid_ds = self.new([self.sequences[i] for i in valid_idxs])

        return (train_ds, valid_ds)


# Cell

class Vec_To_Text_Dataset(Vector_Dataset):
    '''
    Vec_To_Text_Dataset - base dataset for predicting text sequences from vectors

    Inputs:

    - `sequences [list[str], list[tuple]]`: list of text sequences or text tuples (source, target)

    - `vocab Vocab`: vocabuary for tokenization/numericaization

    - `vec_function Callable`: function to convert a sequence to a vector

    - `collate_function Callable`: batch collate function. If None, defauts to `vec_to_text_collate`

    `__getitem__` returns a tuple of `(sequence_vector, sequence_ints)`.

    If `sequences` is a list of strings, both `sequence_vector` and `sequence_ints`
    will be derived from the same sequence.

    If `sequences` is a list of tuples, `sequence_vector` will be derived from the first sequence
    and `sequence_ints` will be derived from the second sequence
    '''
    def __init__(self, sequences, vocab, vec_function, collate_function=None):

        if collate_function is None:
            collate_function = partial(vec_to_text_collate, pad_idx=vocab.stoi['pad'])

        super().__init__(sequences, vec_function, collate_function)
        self.vocab = vocab

    def __getitem__(self, idx):
        sequence = self.sequences[idx]

        if type(sequence)==tuple:
            source_sequence = sequence[0]
            target_sequence = sequence[1]
        else:
            source_sequence = sequence
            target_sequence = sequence

        vec = self.vec_function(source_sequence)
        vec = torch.FloatTensor(vec)

        tokens = self.vocab.tokenize(target_sequence)
        ints = self.vocab.numericalize(tokens)
        ints = torch.LongTensor(ints)

        return (vec, ints)

    def new(self, sequences):
        return self.__class__(sequences, self.vocab, self.vec_function, self.collate_function)

    def split_on_idxs(self, train_idxs, valid_idxs):

        train_ds = self.new([self.sequences[i] for i in train_idxs])
        valid_ds = self.new([self.sequences[i] for i in valid_idxs])

        return (train_ds, valid_ds)


# Cell

class Vec_Prediction_Dataset(Vector_Dataset):
    '''
    Vec_Prediction_Dataset - base dataset for predicting y_vals from vectors

    Inputs:

    - `sequences list[str]`: list of text sequences

    - `y_vals list[int, float]`: list of paired output values

    - `vec_function Callable`: function to convert a sequence to a vector

    - `collate_function Callable`: batch collate function. If None, defauts to `vector_prediction_collate`
    '''
    def __init__(self, sequences, y_vals, vec_function, collate_function=None):
        if collate_function is None:
            collate_function = vector_prediction_collate
        super().__init__(sequences, vec_function, collate_function)

        self.y_vals = y_vals

    def __getitem__(self, idx):
        fp = super().__getitem__(idx)
        y_val = torch.FloatTensor([self.y_vals[idx]]).squeeze()
        return (fp, y_val)

    def new(self, sequences, y_vals):
        return self.__class__(sequences, y_vals, self.vec_function, self.collate_function)


    def split_on_idxs(self, train_idxs, valid_idxs):

        train_ds = self.new([self.sequences[i] for i in train_idxs],
                            [self.y_vals[i] for i in train_idxs])
        valid_ds = self.new([self.sequences[i] for i in valid_idxs],
                            [self.y_vals[i] for i in valid_idxs])

        return (train_ds, valid_ds)
