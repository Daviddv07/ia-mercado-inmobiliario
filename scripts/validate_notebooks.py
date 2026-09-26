"""Static publication checks; never executes training or accesses AWS."""
import ast
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN = [r"(?:AKIA|ASIA)[A-Z0-9]{16}", r"arn:aws:[^\s\"']+", r"https?://(?:www\.)?idealista\.com/[^\s]+", r"hito4-david-diaz", r"autopilot-sagemaker-daviddiaz", r"/content/", r"aws_secret_access_key\s*=", r"\bRequestId\b", r"\bHostId\b"]


def main():
    files = sorted((ROOT / 'notebooks').glob('*.ipynb'))
    assert len(files) == 4, 'Expected four milestones'
    code_cells = 0
    for path in files:
        raw = path.read_text(encoding='utf-8')
        notebook = json.loads(raw)
        assert notebook['nbformat'] == 4
        for pattern in FORBIDDEN:
            assert not re.search(pattern, raw), f'{path.name}: prohibited content ({pattern})'
        for i, cell in enumerate(notebook['cells']):
            assert cell['cell_type'] in ('code', 'markdown')
            source = ''.join(cell['source'])
            if cell['cell_type'] == 'code':
                ast.parse(source, filename=f'{path.name}:cell-{i}')
                code_cells += 1
                for output in cell.get('outputs', []):
                    assert output['output_type'] != 'error'
                    assert not (set(output.get('data', {})) - {'text/plain', 'image/png'})
        try:
            import nbformat
        except ImportError:
            pass
        else:
            nbformat.validate(nbformat.from_dict(notebook))
    print(f'PASS: {len(files)} notebooks, {code_cells} Python cells; static publication checks')


if __name__ == '__main__':
    main()
