# -*- coding: utf-8 -*-
from .aggregation import SequencePooling, SequenceAttention, SequenceGroupAggregating, ScalarMix
from .dropout import WordDropout, LockedDropout, CombinedDropout
from .crf import CRF
from .loss import SoftLabelCrossEntropyLoss, SmoothLabelCrossEntropyLoss, FocalLoss
