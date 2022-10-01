from pathlib import Path

from .leavedonto.leavedonto import LeavedOnto


def parse_cfg_terminals():
    onto_path = Path(__file__).parent / 'resources' / 'A0_onto.yaml'
    onto = LeavedOnto(onto_path)

    comp_path = Path(__file__).parent / 'patterns' / 'components.txt'
    lines = comp_path.read_text(encoding='utf-8').splitlines()
    # remove comments
    lines = [l.split('#')[0] if '#' in l else l for l in lines]

    # parse lines
    parsed_lines = []
    for line in lines:
        if '»' in line:
            key, values = line.split(' » ')
            # get words from onto
            values = [[e for e in v.split('/') if e] for v in values.split(' ') if v]
            results = []
            for v in values:

                res = onto.ont.find_entries(prefix=v)
                for _, r in res:
                    for entry in r:
                        results.append(onto.get_field_value(entry, 'word'))

            # construct CFG line
            for r in results:
                parsed_lines.append(f"{key} -> '{r}'")

        else:
            parsed_lines.append(line)
    return '\n'.join(parsed_lines)

