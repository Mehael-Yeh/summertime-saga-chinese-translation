"""Align actually evaluated native RPY conditions with crawled source nodes."""
import argparse
import ast
import collections
import json
from pathlib import Path


def expression_key(expression):
    try:return ast.dump(ast.parse(expression,mode='eval'),include_attributes=False)
    except (SyntaxError,TypeError):return None


def align(source_report,response_report):
    if source_report['engine_version']!=response_report['version']:
        raise ValueError('Source engine and response versions differ')
    conditions=[row for row in source_report['graph']['statements'] if row['node']=='If']
    cases=response_report.get('native_cases',response_report.get('parameter_native_responses',[]))
    observations=[]
    for case in cases:
        if case.get('status')=='not_in_requested_parameter_segment':continue
        for receipt in case.get('native_script_continuations',()):
            for statement in receipt.get('statements',()):
                if statement['kind']!='If':continue
                location,line=statement['source'].rsplit(':',1)
                location=location.replace('\\','/')
                if location.startswith('game/'):location=location[5:]
                for observed in statement.get('native_evaluated_conditions',()):
                    key=expression_key(observed['expression'])
                    matches=[row for row in conditions if row['file'].replace('\\','/').endswith('/'+location)
                        and any(expression_key(expr)==key for expr in row['conditions']) and key is not None]
                    same_line=[row for row in matches if row['line']==int(line)]
                    if same_line:matches=same_line
                    status='source_condition_observed' if len(matches)==1 and observed.get('truth') is not None else (
                        'unknown_native_truth' if observed.get('truth') is None else 'source_ambiguous' if len(matches)>1 else 'source_not_matched')
                    observations.append({'gate':case['gate'],'source':statement['source'],
                        'parameter_index':case.get('parameter_index'),'inputs':case.get('native_menu_inputs',{}),
                        'expression':observed['expression'],'truth':observed.get('truth'),'status':status,
                        'source_rows':[row['id'] for row in matches],
                        'task_status':case['status'],'queue_drained':case.get('native_queue_drained',False),
                        'state_before_sha256':case.get('state_delta',{}).get('before_sha256'),
                        'state_after_sha256':case.get('state_delta',{}).get('after_sha256')})
    counts=dict(collections.Counter(row['status'] for row in observations))
    covered={row['source_rows'][0] for row in observations if row['status']=='source_condition_observed'}
    return {'engine_version':source_report['engine_version'],'response_version':response_report['version'],
        'observations':observations,'statuses':counts,'source_if_nodes':len(conditions),
        'observed_source_if_nodes':len(covered),
        'unobserved_source_if_nodes':[row['id'] for row in conditions if row['id'] not in covered],
        'validation_mode':'gate_only','route_endpoint_validation_required':False,
        'all_gates_passed':False,
        'scope':'Actual RPY If evaluations aligned to syntax only; not full prerequisites, all branch outcomes or terminal state acceptance'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source_report',type=Path)
    parser.add_argument('response_report',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    source=json.loads(args.source_report.read_text(encoding='utf8'))
    responses=json.loads(args.response_report.read_text(encoding='utf8'))
    if source['engine_version']!=responses['version']:raise ValueError('Source engine and response versions differ')
    result=align(source,responses)
    args.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf8',newline='\n')
    print(json.dumps({key:result[key] for key in ('statuses','source_if_nodes','observed_source_if_nodes','all_gates_passed')}))


if __name__=='__main__':main()
