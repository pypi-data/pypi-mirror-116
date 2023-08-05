# -*- coding: utf-8 -*-
import torch


def seq_lens2mask(seq_lens: torch.LongTensor, max_len: int=None):
    """
    Convert `seq_lens` to `mask`. 
    
    Parameters
    ----------
    seq_lens : torch.LongTensor (batch, )
    max_len : int, optional
    
    Returns
    -------
    mask : torch.BoolTensor (batch, step)
        The positions with values of True are MASKED, while the others are NOT MASKED. 
    """
    max_len = seq_lens.max().item() if max_len is None else max_len
    steps = torch.arange(max_len, device=seq_lens.device).expand(seq_lens.size(0), -1)
    return (steps >= seq_lens.unsqueeze(1))



def mask2seq_lens(mask: torch.BoolTensor):
    """
    Convert `mask` to `seq_lens`. 
    """
    return mask.size(1) - mask.sum(dim=1)



def sequence_pooling(x: torch.FloatTensor, 
                     mask: torch.BoolTensor, 
                     weight: torch.FloatTensor=None, 
                     mode: str='mean'):
    """
    Pooling values over steps. 
    
    Parameters
    ----------
    x: torch.FloatTensor (batch, step, hid_dim)
    mask: torch.BoolTensor (batch, step)
    weight: torch.FloatTensor (batch, step)
    mode: str
        'mean', 'max', 'min', 'wtd_mean'
    """
    if mode.lower() == 'mean':
        x_masked = x.masked_fill(mask.unsqueeze(-1), 0)
        seq_lens = mask2seq_lens(mask)
        return x_masked.sum(dim=1) / seq_lens.unsqueeze(1)
    elif mode.lower() == 'max':
        x_masked = x.masked_fill(mask.unsqueeze(-1), float('-inf'))
        return x_masked.max(dim=1).values
    elif mode.lower() == 'min':
        x_masked = x.masked_fill(mask.unsqueeze(-1), float('inf'))
        return x_masked.min(dim=1).values
        
    elif mode.lower() == 'wtd_mean':
        weight_masked = weight.masked_fill(mask, 0)
        weight_masked_norm = torch.nn.functional.normalize(weight_masked.type(torch.float), p=1, dim=1)
        # x_wtd_mean: (batch, hid_dim)
        return weight_masked_norm.unsqueeze(1).bmm(x).squeeze(1)
        
    else:
        raise ValueError(f"Invalid pooling mode {mode}")
        
        
        
def sequence_group_aggregating(x: torch.FloatTensor, group_by: torch.LongTensor, agg_mode: str='mean', agg_step: int=None):
    """
    Aggregating values over steps by groups. 
    
    Parameters
    ----------
    x : torch.FloatTensor (batch, ori_step, hidden)
        The tensor to be aggregate. 
    group_by : torch.LongTensor (batch, ori_step)
        The tensor indicating the positions after aggregation. 
        The values of `x` with corresponding `group_by` being NEGATIVE are NOT used in aggregation. 
        The after-aggregation positions NOT covered by `group_by` are ZEROS.
        
    agg_mode: str
        'mean', 'max', 'min', 'first', 'last'
    agg_step: int
    """
    if agg_mode.lower() not in ('mean', 'max', 'min', 'first', 'last'):
        raise ValueError(f"Invalid aggregation mode {agg_mode}")
    
    agg_step = (group_by.max().item() + 1) if agg_step is None else agg_step
    
    # pos_proj: (agg_step, ori_step)
    pos_proj = torch.arange(agg_step, device=group_by.device).unsqueeze(1).expand(-1, group_by.size(1))
    
    # pos_proj: (batch, agg_step, ori_step)
    pos_proj = (pos_proj.unsqueeze(0) == group_by.unsqueeze(1))
    
    if agg_mode.lower() in ('mean', 'first', 'last'):
        pos_proj_weight = _make_pos_proj_weight(pos_proj, agg_mode=agg_mode)
        
        # agg_tensor: (batch, agg_step, hidden)
        return pos_proj_weight.bmm(x)
    
    else:
        return _execute_pos_proj(x, pos_proj, agg_mode=agg_mode)
    
    
def _make_pos_proj_weight(pos_proj: torch.BoolTensor, agg_mode='mean'):
    if agg_mode.lower() == 'mean':
        return torch.nn.functional.normalize(pos_proj.type(torch.float), p=1, dim=2)
    elif agg_mode.lower() == 'first':
        pos_proj_weight = pos_proj & (pos_proj.cumsum(dim=-1) == 1)
        return pos_proj_weight.type(torch.float)
    elif agg_mode.lower() == 'last':
        pos_proj_weight = pos_proj & (pos_proj.cumsum(dim=-1) == pos_proj.sum(dim=-1, keepdim=True))
        return pos_proj_weight.type(torch.float)
    
    
def _execute_pos_proj(x: torch.FloatTensor, pos_proj: torch.BoolTensor, agg_mode='max'):
    proj_values = []
    for k in range(pos_proj.size(0)):
        curr_proj_values = []
        for curr_pos_proj in pos_proj[k]:
            if curr_pos_proj.sum() == 0:
                # Set non-covered positions as zeros
                curr_proj_values.append(torch.zeros(x.size(-1)))
            elif agg_mode.lower() == 'max':
                curr_proj_values.append(x[k, curr_pos_proj].max(dim=0).values)
            elif agg_mode.lower() == 'min':
                curr_proj_values.append(x[k, curr_pos_proj].min(dim=0).values)
        proj_values.append(torch.stack(curr_proj_values))
    return torch.stack(proj_values)




def _reduce_losses(losses: torch.Tensor, sample_weight: torch.Tensor=None, reduction: str='none'):
    if reduction.lower() == 'sum':
        return losses.sum()
    elif reduction.lower() == 'mean' and sample_weight is None:
        return losses.mean()
    elif reduction.lower() == 'mean' and sample_weight is not None:
        return losses.sum() / sample_weight.sum()
    else:
        return losses


def soft_label_cross_entropy(logits: torch.Tensor, soft_target: torch.Tensor, weight: torch.Tensor=None, reduction: str='none'):
    """Soft label cross entropy loss.
    
    Parameters
    ----------
    logits : torch.Tensor (num_entries, logit_dim)
        Logits before softmax. 
    soft_target : torch.Tensor (num_entries, logit_dim)
        `target.sum(dim=-1)` should equal 1 in all entries.
    weight : torch.Tensor (logit_dim, )
        A manual rescaling weight given to each class. 
    """
    log_prob = torch.nn.functional.log_softmax(logits, dim=-1)
    if weight is not None:
        log_prob = log_prob * weight
    
    losses = -(log_prob * soft_target).sum(dim=-1)
    return _reduce_losses(losses, sample_weight=None, reduction=reduction)


def smooth_label_cross_entropy(logits: torch.Tensor, target: torch.LongTensor, 
                               epsilon: float=0.1, weight: torch.Tensor=None, ignore_index: int=-100, reduction: str='none'):
    """Smooth label cross entropy loss.
    
    Parameters
    ----------
    logits : torch.Tensor (num_entries, logit_dim)
        Logits before softmax. 
    target : torch.LongTensor (num_entries, )
        `target` is the index of ground truth. 
    epsilon : float
    weight : torch.Tensor (logit_dim, )
        A manual rescaling weight given to each class. 
    """
    if weight is None:
        sample_weight = (target != ignore_index).type(torch.float)
    else:
        sample_weight = weight.gather(dim=0, index=target) * (target != ignore_index).type(torch.float)
    
    log_prob = torch.nn.functional.log_softmax(logits, dim=-1)
    target_wo_ignore_index = target.masked_fill(target==ignore_index, 0)
    smooth_target = torch.where(torch.nn.functional.one_hot(target_wo_ignore_index, num_classes=logits.size(dim=-1)).type(torch.bool), 
                                1 - epsilon, 
                                epsilon / (logits.size(dim=-1) - 1))
    losses = -(log_prob * smooth_target).sum(dim=-1)
    
    losses = losses * sample_weight
    return _reduce_losses(losses, sample_weight=sample_weight, reduction=reduction)


def focal_loss(logits: torch.Tensor, target: torch.LongTensor, 
               gamma: float=0.0, weight: torch.Tensor=None, ignore_index: int=-100, reduction: str='none'):
    """Multi-class focal loss. 
    
    Parameters
    ----------
    logits : torch.Tensor (num_entries, logit_dim)
        Logits before softmax. 
    target : torch.LongTensor (num_entries, )
        `target` is the index of ground truth. 
    gamma : float
        \mathrm{FocalLoss}(p_t) = -\alpha_t (1-p_t)^{\gamma} \log (p_t)
    weight : torch.Tensor (logit_dim, )
        A manual rescaling weight given to each class. 
        `weight` is referred as `alpha` in Lin et al. (2017). 
    
    References
    ----------
    [1] Lin et al. (2017). Focal Loss for Dense Object Detection. ICCV 2017. 
    """
    if weight is None:
        sample_weight = (target != ignore_index).type(torch.float)
    else:
        sample_weight = weight.gather(dim=0, index=target) * (target != ignore_index).type(torch.float)
    
    log_prob = torch.nn.functional.log_softmax(logits, dim=-1)
    target_wo_ignore_index = target.masked_fill(target==ignore_index, 0)
    log_prob_t = log_prob.gather(dim=1, index=target_wo_ignore_index.unsqueeze(-1)).squeeze(-1)
    
    prob_t = log_prob_t.exp()
    losses = -log_prob_t * torch.pow(1 - prob_t, gamma)
    
    losses = losses * sample_weight
    return _reduce_losses(losses, sample_weight=sample_weight, reduction=reduction)
