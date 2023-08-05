# -*- coding: utf-8 -*-
import numpy

from ..utils import ChunksTagsTranslator
from .base import IO


class ConllIO(IO):
    """An IO interface of CoNLL-format files. 
    
    Parameters
    ----------
    line_sep_starts: list of str
        For Conll2003, `line_sep_starts` should be `["-DOCSTART-"]`
        For OntoNotes5 (i.e., Conll2012), `line_sep_starts` should be `["#begin", "#end", "pt/"]`
    """
    def __init__(self, 
                 text_col_id=0, 
                 tag_col_id=1, 
                 sep=None, 
                 scheme='BIO1', 
                 tag_sep='-',
                 breaking_for_types=True, 
                 additional_col_id2name=None, 
                 line_sep_starts=None, 
                 encoding=None, 
                 verbose: bool=True, 
                 **token_kwargs):
        self.text_col_id = text_col_id
        self.tag_col_id = tag_col_id
        self.sep = sep
        
        self.tags_translator = ChunksTagsTranslator(scheme=scheme, sep=tag_sep, breaking_for_types=breaking_for_types)
        if additional_col_id2name is None:
            self.additional_col_id2name = {}
        else:
            assert all(isinstance(col_id, int) for col_id in additional_col_id2name.keys())
            assert all(isinstance(col_name, str) for col_name in additional_col_id2name.values())
            self.additional_col_id2name = additional_col_id2name
            
        if line_sep_starts is None:
            self.line_sep_starts = []
        else:
            assert all(isinstance(start, str) for start in line_sep_starts)
            self.line_sep_starts = line_sep_starts
            
        super().__init__(is_tokenized=True, encoding=encoding, verbose=verbose, **token_kwargs)
        
        
    def read(self, file_path):
        data = []
        with open(file_path, 'r', encoding=self.encoding) as f:
            text, tags = [], []
            additional = {col_id: [] for col_id in self.additional_col_id2name.keys()}
            
            for line in f:
                line = line.strip()
                
                if self._is_line_seperator(line):
                    if len(text) > 0:
                        additional_tags = {self.additional_col_id2name[col_id]: atags for col_id, atags in additional.items()}
                        tokens = self._build_tokens(text, additional_tags=additional_tags)
                        chunks = self.tags_translator.tags2chunks(tags)
                        data.append({'tokens': tokens, 'chunks': chunks})
                        
                        text, tags = [], []
                        additional = {col_id: [] for col_id in self.additional_col_id2name.keys()}
                else:
                    line_seperated = line.split(self.sep)
                    text.append(line_seperated[self.text_col_id])
                    tags.append(line_seperated[self.tag_col_id])
                    for col_id in self.additional_col_id2name.keys():
                        additional[col_id].append(line_seperated[col_id])
                        
            if len(text) > 0:
                additional_tags = {self.additional_col_id2name[col_id]: atags for col_id, atags in additional.items()}
                tokens = self._build_tokens(text, additional_tags=additional_tags)
                chunks = self.tags_translator.tags2chunks(tags)
                data.append({'tokens': tokens, 'chunks': chunks})
            
        return data
    
    
    def _is_line_seperator(self, line: str):
        if line.strip() == "":
            return True
        
        for start in self.line_sep_starts:
            if line.startswith(start):
                return True
            
        return False
    
    
    def flatten_to_characters(self, data: list):
        additional_keys = [key for key in data[0]['tokens'][0].__dict__.keys() if key not in ('text', 'raw_text')]
        
        new_data = []
        for entry in data:
            tokenized_raw_text = entry['tokens'].raw_text
            char_seq_lens = [len(tok) for tok in tokenized_raw_text]
            cum_char_seq_lens = [0] + numpy.cumsum(char_seq_lens).tolist()
            
            flattened_tokenized_raw_text = [char for tok in tokenized_raw_text for char in tok]
            # Repeat additional-tags for every character in a token
            flattened_additional_tags = {key: [atag for atag, tok in zip(getattr(entry['tokens'], key), tokenized_raw_text) for char in tok] 
                                             for key in additional_keys}
            flattened_tokens = self._build_tokens(flattened_tokenized_raw_text, additional_tags=flattened_additional_tags)
            flattened_chunks = [(label, cum_char_seq_lens[start], cum_char_seq_lens[end]) for label, start, end in entry['chunks']]
            new_data.append({'tokens': flattened_tokens, 'chunks': flattened_chunks})
            
        return new_data
