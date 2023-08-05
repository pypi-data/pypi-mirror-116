# -*- coding: utf-8 -*-
import logging

from ..metrics import precision_recall_f1_report
from ..dataset import Dataset
from .trainer import Trainer


logger = logging.getLogger(__name__)


def evaluate_text_classification(trainer: Trainer, dataset: Dataset):
    set_labels_pred = trainer.predict(dataset)
    set_labels_gold = [ex['label'] for ex in dataset.data]
    
    acc = trainer.model.decoder.evaluate(set_labels_gold, set_labels_pred)
    logger.info(f"TC Accuracy: {acc*100:2.3f}%")


def disp_prf(ave_scores: dict, task: str='ER'):
    for key_text, key in zip(['Precision', 'Recall', 'F1-score'], ['precision', 'recall', 'f1']):
        logger.info(f"{task} Micro {key_text}: {ave_scores['micro'][key]*100:2.3f}%")
    for key_text, key in zip(['Precision', 'Recall', 'F1-score'], ['precision', 'recall', 'f1']):
        logger.info(f"{task} Macro {key_text}: {ave_scores['macro'][key]*100:2.3f}%")


def evaluate_entity_recognition(trainer: Trainer, dataset: Dataset):
    set_chunks_pred = trainer.predict(dataset)
    set_chunks_gold = [ex['chunks'] for ex in dataset.data]
    
    scores, ave_scores = precision_recall_f1_report(set_chunks_gold, set_chunks_pred)
    disp_prf(ave_scores, task='ER')


def evaluate_attribute_extraction(trainer: Trainer, dataset: Dataset):
    set_attributes_pred = trainer.predict(dataset)
    set_attributes_gold = [ex['attributes'] for ex in dataset.data]

    scores, ave_scores = precision_recall_f1_report(set_attributes_gold, set_attributes_pred)
    disp_prf(ave_scores, task='AE')


def evaluate_relation_extraction(trainer: Trainer, dataset: Dataset, eval_chunk_type_for_relation: bool=True):
    set_relations_pred = trainer.predict(dataset)
    set_relations_gold = [ex['relations'] for ex in dataset.data]
    
    if not eval_chunk_type_for_relation:
        set_relations_gold = [[(rel_type, head[1:], tail[1:]) for rel_type, head, tail in relations] for relations in set_relations_gold]
        set_relations_pred = [[(rel_type, head[1:], tail[1:]) for rel_type, head, tail in relations] for relations in set_relations_pred]
    
    scores, ave_scores = precision_recall_f1_report(set_relations_gold, set_relations_pred)
    disp_prf(ave_scores, task='RE')


def evaluate_joint_er_re(trainer: Trainer, dataset: Dataset, eval_chunk_type_for_relation: bool=True):
    set_chunks_pred, set_relations_pred = trainer.predict(dataset)
    set_chunks_gold = [ex['chunks'] for ex in dataset.data]
    set_relations_gold = [ex['relations'] for ex in dataset.data]
    
    if not eval_chunk_type_for_relation:
        set_relations_gold = [[(rel_type, head[1:], tail[1:]) for rel_type, head, tail in relations] for relations in set_relations_gold]
        set_relations_pred = [[(rel_type, head[1:], tail[1:]) for rel_type, head, tail in relations] for relations in set_relations_pred]
    
    scores, ave_scores = precision_recall_f1_report(set_chunks_gold, set_chunks_pred)
    disp_prf(ave_scores, task='ER')
    
    scores, ave_scores = precision_recall_f1_report(set_relations_gold, set_relations_pred)
    disp_prf(ave_scores, task='RE')
