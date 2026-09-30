from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys
root=Path('/private/tmp/skill-forward-20260930')
base=root/'recheck-fixtures'
base.mkdir()
results=[]
old_report=root/'report.md'
old_hash=hashlib.sha256(old_report.read_bytes()).hexdigest()
for index,skill in enumerate(('adaptive-model-orchestrator','deep-project-review')):
    original=Path('/Users/lxm/app1/github-preview')/skill
    area=base/skill
    source=area/'source'
    (source/'scripts').mkdir(parents=True)
    (source/'references').mkdir()
    entry=source/'SKILL.md'
    original_text='---\nname: synthetic\ndescription: Synthetic recheck.\n---\nOriginal rules\n'
    entry.write_text(original_text)
    (source/'references'/'rules.md').write_text('Original reference\n')
    helper=source/'scripts'/'freeze_run.py'
    shutil.copy2(original/'scripts'/'freeze_run.py',helper)
    def cli(label,*args,env=None,expected):
        cmd=[sys.executable,'-B',str(helper),*map(str,args)]
        p=subprocess.run(cmd,text=True,capture_output=True,env=env)
        item={'skill':skill,'case':label,'command':cmd,'exit_code':p.returncode,'stdout':p.stdout.strip(),'stderr':p.stderr.strip()}
        results.append(item)
        assert p.returncode==expected,item
        return p
    unsealed=area/'missing-release'
    cli('missing release', '--output',unsealed,expected=1)
    assert not unsealed.exists() and not (source/'runtime-manifest.json').exists()
    cli('intentional fixture seal once','--seal',expected=0)
    release_raw=(source/'runtime-manifest.json').read_bytes()
    plugin=area/'.codex'/'plugins'/'cache'/'plugin'/'skills'/'snapshot'
    cli('plugin discovery destination','--output',plugin,expected=1)
    assert not plugin.exists()
    env=dict(os.environ,CODEX_HOME=str(area/'custom-root'))
    custom=area/'custom-root'/'plugins'/'cache'/'plugin'/'skills'/'snapshot'
    cli('custom CODEX_HOME plugin destination','--output',custom,env=env,expected=1)
    assert not custom.exists()
    entry.write_text('Changed entry with original reference\n')
    partial=area/'partial'
    cli('stable partial source update','--output',partial,expected=1)
    assert not partial.exists()
    assert (source/'runtime-manifest.json').read_bytes()==release_raw
    entry.write_text(original_text)
    snapshot=area/'sealed-snapshot'
    first=cli('completed sealed freeze','--output',snapshot,expected=0)
    digest=json.loads(first.stdout)['digest']
    assert (snapshot/'runtime-manifest.json').read_bytes()==release_raw
    entry.write_text('New installation after frozen run\n')
    verified=cli('old snapshot after source change','--verify',snapshot,expected=0)
    assert json.loads(verified.stdout)['digest']==digest
    assert (snapshot/'SKILL.md').read_text()==original_text
    entry.write_text(original_text)
    for existing_type in ('empty','nonempty'):
        existing=area/f'existing-{existing_type}'
        existing.mkdir()
        if existing_type=='nonempty':
            (existing/'sentinel').write_text('preserve')
        cli(f'preserve existing {existing_type} output','--output',existing,expected=1)
        assert existing.exists()
        if existing_type=='nonempty':
            assert (existing/'sentinel').read_text()=='preserve'
    unit_temp=area/'unit-tmp'
    unit_temp.mkdir()
    unit_env=dict(os.environ,TMPDIR=str(unit_temp),PYTHONDONTWRITEBYTECODE='1')
    cmd=[sys.executable,'-B',str(original/'tests'/'test_freeze_run.py')]
    p=subprocess.run(cmd,text=True,capture_output=True,env=unit_env)
    results.append({'skill':skill,'case':'source test suite','command':cmd,'TMPDIR':str(unit_temp),'exit_code':p.returncode,'stdout':p.stdout.strip(),'stderr':p.stderr.strip()})
    assert p.returncode==0,results[-1]
assert hashlib.sha256(old_report.read_bytes()).hexdigest()==old_hash
results.append({'case':'first report unchanged','sha256':old_hash})
(root/'recheck-results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
