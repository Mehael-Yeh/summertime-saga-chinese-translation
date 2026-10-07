"""Advance native gates in one disposable world and compare observed effects.

Adapters must select the next gate from the native task/dependency state, not
from file line order or an actor-specific list. This module does not execute
Ren'Py itself and does not certify adapters that have not been native-tested.
"""
import copy
import hashlib
import json


def fingerprint(snapshot):
    return hashlib.sha256(json.dumps(snapshot,sort_keys=True,ensure_ascii=True,
        separators=(',',':')).encode('ascii')).hexdigest()


def at_path(value,path):
    for key in path:
        if not isinstance(value,dict) or key not in value:
            return False,None
        value=value[key]
    return True,value


def compare_effects(reference,generated,effects):
    """Compare final native facts; later effects supersede earlier values.

    No temporal or task field is silently excluded. Any exclusions must be
    handled explicitly by the adapter's declared semantic contract.
    """
    if reference.get('unknown') or generated.get('unknown'):
        return {'status':'unknown_snapshot','differences':[]}
    paths=sorted({tuple(row['path']) for row in effects},key=lambda path:json.dumps(path,ensure_ascii=True))
    differences=[]
    for path in paths:
        found,wanted=at_path(reference,path)
        present,actual=at_path(generated,path)
        if found!=present or (found and actual!=wanted):
            differences.append({'path':list(path),'reference_present':found,
                'generated_present':present,'expected':wanted,'actual':actual})
    return {'status':'state_mismatch' if differences else 'observed_effects_match',
        'compared_paths':len(paths),'differences':differences,
        'scope':'Observed native effects and declared postcondition paths only'}


def run_sequence(select_next,solve,execute,observe,generated_snapshot,max_steps=128,checkpoint=None):
    """Keep state across gates, solve only the current gate, stop on unknown.

    execute must retain inputs/native effects in the same isolated world.
    select_next must provide source-backed final-gate completion evidence;
    an empty candidate list, no witness or a repeated reminder is not success.
    generated_snapshot must read the actual loaded Mod-generated save.
    """
    rows=[]
    effects=[]
    seen=set()
    result={'validation_mode':'sequential_gate_only','all_gates_passed':False,
        'steps':rows,'route_endpoint_replay_required':False}
    for index in range(max_steps):
        before_selection=copy.deepcopy(observe())
        selected=select_next()
        if selected.get('status')=='native_final_gate_completed':
            if not rows or not selected.get('source') or not selected.get('native_completion_evidence'):
                return dict(result,status='unverified_final_gate')
            reference=copy.deepcopy(observe())
            result['reference_sha256']=fingerprint(reference)
            result['completion']=selected
            comparison=compare_effects(reference,generated_snapshot(),effects)
            result['comparison']=comparison
            # Matching observations alone do not certify complete prerequisites.
            result['all_gates_passed']=(comparison['status']=='observed_effects_match'
                and bool(effects) and all(row.get('native_postconditions_validated') is True for row in rows))
            return dict(result,status='sequence_verified' if result['all_gates_passed'] else 'sequence_not_accepted')
        if selected.get('status')!='native_gate' or not selected.get('source'):
            return dict(result,status='next_gate_unresolved',selection=selected)
        identity=(selected['source'],selected.get('gate'),fingerprint(before_selection))
        if identity in seen:return dict(result,status='no_progress_cycle',selection=selected)
        seen.add(identity)
        # Recompute against accumulated state. Never concatenate constraints
        # from already completed gates or reset to the generated Mod state.
        witness=solve(selected)
        if witness.get('status')!='parameter_witness':
            return dict(result,status='prerequisite_unresolved',selection=selected,witness=witness)
        receipt=execute(selected,witness)
        row=dict(receipt,gate=selected.get('gate'),source=selected['source'],index=index,
            witness=copy.deepcopy(witness))
        rows.append(row)
        if checkpoint is not None:checkpoint(copy.deepcopy(row))
        trace=row.get('native_branch_trace',{})
        if (row.get('status')!='native_dispatch_observed' or row.get('native_queue_drained') is not True
                or row.get('native_task_completed') is not True
                or trace.get('truncated') or row.get('error')
                or not (row.get('target_entry_observed') or row.get('target_branch_observed'))):
            return dict(result,status='native_gate_incomplete')
        if row.get('before',{}).get('unknown') or row.get('after',{}).get('unknown'):
            return dict(result,status='unknown_snapshot')
        effects.extend(row.get('state_delta',{}).get('changes',()))
        effects.extend({'path':path} for path in row.get('native_postcondition_paths',()))
    return dict(result,status='sequence_budget_exhausted')
