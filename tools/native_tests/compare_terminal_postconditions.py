"""Compare observed native frontiers with a freshly loaded constructed save.

This checks stored postconditions only, not full dialogue or UI coverage.
Missing frontiers, missing native data, or version mismatches fail explicitly.
"""
import argparse
import json
from pathlib import Path


def compare(reference, generated):
    errors=[]
    if reference.get('version')!=generated.get('version'):
        errors.append({'reason':'different_native_versions'})
    if reference.get('constructed_mod_save') is not False or reference.get('fabricated_quest_steps') is not False:
        errors.append({'reason':'reference_is_not_native_execution'})
    required={row[0] for row in generated.get('routes',[]) if isinstance(row,list) and row}
    observed=reference.get('terminal_observations',{})
    missing=sorted(required-set(observed))
    actual=generated.get('native_postconditions',{})
    if not actual:errors.append({'reason':'missing_loaded_native_postconditions'})
    comparisons=[]
    for route,observation in observed.items():
        for entity,fields in observation.get('postconditions',{}).items():
            final=dict(actual.get(entity,()))
            for field,expected in fields:
                # Encounter memories are monotone through later quest endings.
                # Stage and scalar values can be superseded by another route;
                # report these differences for review instead of auto-fixing.
                value=final.get(field)
                if field=='memo' and isinstance(expected,list) and isinstance(value,list):
                    match=all(item in value for item in expected)
                else:match=expected==value
                comparisons.append({'route':route,'entity':entity,'field':field,
                    'native_observed':expected,'generated':value,'matches':match})
    return {'version':generated.get('version'),'scope':'native frontier stored postcondition comparison',
        'missing_native_frontiers':missing,'errors':errors,'comparisons':comparisons,
        'differences_requiring_review':[row for row in comparisons if not row['matches']],
        'all_routes_verified':False,'full_dialogue_or_device_acceptance':False,
        'frontier_comparison_complete':bool(required) and not missing and not errors
            and bool(comparisons) and all(row['matches'] for row in comparisons)}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('reference',type=Path)
    parser.add_argument('generated',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    result=compare(json.loads(args.reference.read_text(encoding='utf8')),
        json.loads(args.generated.read_text(encoding='utf8')))
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps({key:result[key] for key in ('version','missing_native_frontiers','errors','frontier_comparison_complete')},ensure_ascii=False))
    return 0 if result['frontier_comparison_complete'] else 1


if __name__=='__main__':raise SystemExit(main())
