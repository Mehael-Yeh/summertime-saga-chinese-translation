"""Correlate native observations with source branches without certifying gates."""
import argparse
import json
from collections import defaultdict


def correlate(inventory, reports):
    if not inventory.get('baseline_sha256'):
        raise ValueError('Inventory has no native baseline fingerprint')
    expected = defaultdict(set)
    for gate in inventory['gates']:
        for branch in gate['analysis']['branches']:
            identity = branch.get('code_identity_sha256')
            if not identity:
                raise ValueError('Native branch has no source identity')
            expected[(branch['module'], identity, branch['offset'])].add(gate['id'])
    observed = defaultdict(lambda: defaultdict(list))
    limitations = []
    for report_index, report in enumerate(reports):
        for field in ('version', 'baseline_sha256'):
            if report.get(field) != inventory[field]:
                raise ValueError('Native evidence mismatch: '+field)
        if report['status'] not in ('segment_complete', 'navigation_scan_complete'):
            raise ValueError('Failed or unfinished response report')
        limitations.append({'report_index':report_index, 'tick':report['tick'],
            'status':report['status'], 'pending':len(report['pending']),
            'unsupported_controls':len(report.get('unhandled_controls',{})),
            'unexplored_world_variants':len(report.get('unexplored_world_variants',{})),
            'temporal_exits':len(report.get('temporal_exits',[]))})
        for row_index, row in enumerate(report['rows']):
            trace=row.get('native_branch_trace') or {}
            if trace.get('truncated'):
                limitations.append({'report_index':report_index,'row_index':row_index,'trace_truncated':True})
            for branch in trace.get('observations',[]):
                identity=branch.get('code_identity_sha256')
                if not identity:raise ValueError('Trace lacks source identity')
                key=(branch['module'],identity,branch['offset'])
                observed[key][str(bool(branch['condition_truth'])).lower()].append(
                    {'report_index':report_index,'row_index':row_index,'bindings':branch['bindings']})
    rows=[]
    for key, gate_ids in sorted(expected.items()):
        outcomes=observed.get(key,{})
        rows.append({'module':key[0],'code_identity_sha256':key[1],'offset':key[2],
            'gate_ids':sorted(gate_ids),'native_observations':dict(outcomes),
            'unobserved_outcomes':[value for value in ('true','false') if value not in outcomes],
            'semantic_postconditions_validated':False})
    return {'version':inventory['version'],'baseline_sha256':inventory['baseline_sha256'],
        'branches':rows,'limitations':limitations,
        'unmapped_observed_branches':len(set(observed)-set(expected)),
        'all_gates_passed':False,
        'scope':'Executed branch observations only. Unvisited edges may be retired, temporal or unreachable; their classification and native postconditions require separate evidence.'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('inventory')
    parser.add_argument('reports',nargs='+')
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    def read(path):
        with open(path,encoding='utf8') as stream:return json.load(stream)
    result=correlate(read(args.inventory),[read(path) for path in args.reports])
    with open(args.output,'w',encoding='utf8',newline='\n') as stream:
        json.dump(result,stream,ensure_ascii=False,indent=2)
        stream.write('\n')


if __name__=='__main__':main()
