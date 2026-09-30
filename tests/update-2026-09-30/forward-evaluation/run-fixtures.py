from pathlib import Path
import hashlib, importlib.util, json, shutil, subprocess, sys
root = Path('/private/tmp/skill-forward-20260930')
results=[]
sources=[Path('/Users/lxm/app1/github-preview/adaptive-model-orchestrator/scripts/freeze_run.py'), Path('/Users/lxm/app1/github-preview/deep-project-review/scripts/freeze_run.py')]
for idx, original in enumerate(sources):
    area=root/f'fixture-{idx}'
    source=area/'source'
    (source/'scripts').mkdir(parents=True)
    (source/'references').mkdir()
    (source/'tests').mkdir()
    (source/'docs').mkdir()
    (source/'SKILL.md').write_text('---\nname: synthetic\ndescription: Synthetic freeze validation.\n---\nVersion A\n')
    (source/'references'/'rule.md').write_text('Rule A\n')
    (source/'README.md').write_text('Runtime introduction\n')
    (source/'tests'/'history.txt').write_text('Excluded historical fixture\n')
    (source/'docs'/'maintenance.txt').write_text('Excluded maintenance fixture\n')
    script=source/'scripts'/'freeze_run.py'
    shutil.copy2(original,script)
    def command(*args):
        cmd=[sys.executable,str(script),*map(str,args)]
        p=subprocess.run(cmd,text=True,capture_output=True)
        record={'command':cmd,'exit_code':p.returncode,'stdout':p.stdout.strip(),'stderr':p.stderr.strip()}
        results.append(record)
        return p
    snapshot=area/'snapshot'
    command('--output',snapshot)
    command('--verify',snapshot)
    (source/'SKILL.md').write_text('---\nname: synthetic\ndescription: Synthetic freeze validation.\n---\nVersion B\n')
    p=command('--verify',snapshot)
    results.append({'case':'source updated after freeze','skill':str(original),'snapshot_has_A': 'Version A' in (snapshot/'SKILL.md').read_text(),'source_has_B':'Version B' in (source/'SKILL.md').read_text(),'verification_exit_code':p.returncode,'historical_test_copied':(snapshot/'tests').exists(),'maintenance_docs_copied':(snapshot/'docs').exists()})
    existing=area/'existing'
    existing.mkdir()
    (existing/'sentinel').write_text('preserve')
    p=command('--output',existing)
    results.append({'case':'pre-existing nonempty output','exit_code':p.returncode,'sentinel_preserved':(existing/'sentinel').read_text()=='preserve'})
    empty=area/'empty'
    empty.mkdir()
    p=command('--output',empty)
    results.append({'case':'pre-existing empty output','exit_code':p.returncode,'directory_preserved':empty.is_dir()})
    (snapshot/'references'/'rule.md').write_text('Tampered rule\n')
    command('--verify',snapshot)
    (snapshot/'references'/'rule.md').write_text('Rule A\n')
    (snapshot/'unexpected-root.txt').write_text('not in runtime inventory\n')
    p=command('--verify',snapshot)
    results.append({'case':'extra file outside runtime allowlist','verification_exit_code':p.returncode})
    spec=importlib.util.spec_from_file_location(f'freeze{idx}',script)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    original_copy=mod.shutil.copy2
    mutation={'done':False}
    def changing_copy(src,dst,*args,**kwargs):
        copied=original_copy(src,dst,*args,**kwargs)
        if not mutation['done']:
            mutation['done']=True
            (source/'references'/'rule.md').write_text('Source changed during copying\n')
        return copied
    mod.shutil.copy2=changing_copy
    during=area/'during-copy'
    try:
        mod.freeze(source,during)
        results.append({'case':'source change during copy','outcome':'unexpected success'})
    except Exception as exc:
        results.append({'case':'source change during copy','error':str(exc),'output_removed':not during.exists()})
    finally:
        mod.shutil.copy2=original_copy
    path=area/'.codex'/'plugins'/'cache'/'plugin'/'skills'/'snapshot'
    results.append({'case':'plugin-style installation path recognizer','path':str(path),'is_discovery_path':mod.is_discovery_path(path.resolve())})
results.append({'case':'source helpers equal','sha256':[hashlib.sha256(p.read_bytes()).hexdigest() for p in sources]})
(root/'results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
