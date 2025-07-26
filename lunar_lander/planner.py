import subprocess
from tqdm import tqdm

DOMAINS = ['simplified']#['novelocity', 'mini', 'simplified']
INITS = {
    'novelocity' : [(-4,4), (5,10), (-2,2)],
    'mini' : [(-1,1), (1,2), (-1,1), (-2,0)],
    'simplified' : [(0,2), (1,3), (0,0), (-2,0)]#[(-2,2), (1,3), (-1,1), (-2,0)]
    }

def plan_and_write(domain : str, values : list):
    init = 5
    with open(f'{domain}/template.pddl', 'r') as re:
        with open(f'{domain}/temp_prob.pddl', 'w') as wr:
            lines = re.readlines()
            for i, line in enumerate(lines):
                if i == init:
                    line = line.replace('(current_x x_0)', f'(current_x x_{values[0]})')
                    line = line.replace('(current_y y_0)', f'(current_y y_{values[1]})')
                    line = line.replace('(current_t t_0)', f'(current_t t_{values[2]})')
                    if domain in ['mini', 'simplified']:
                        line = line.replace('(current_vy vy_0)', f'(current_vy vy_{values[3]})')
                wr.write(line)
    command = ['./../../prp/prp', './domain.pddl', './temp_prob.pddl', '--jic-limit', '10', '--dump-policy', '2']
    process = subprocess.Popen(command, shell=False, cwd=f'{domain}', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    process.wait()

    with open(f'{domain}/policy.txt', 'r+') as wr, open(f'{domain}/policy.out', 'r') as re:
        lines_out = re.readlines()
        for i, line_out in enumerate(lines_out):
            if line_out.startswith('If'):
                wr.seek(0)
                found = False
                lines_txt = wr.readlines()
                for j, line_txt in enumerate(lines_txt):
                    if line_out == line_txt:
                        found = True
                        break
                if not found:
                    wr.writelines([lines_out[i-1], lines_out[i], lines_out[i+1]])

if __name__ == '__main__':
    for domain in tqdm(DOMAINS, desc='Domain: '):
        for x in tqdm(range(INITS[domain][0][0], INITS[domain][0][1]+1), desc='x: ', leave=False):
            for y in tqdm(range(INITS[domain][1][0], INITS[domain][1][1]+1), desc='y: ', leave=False):
                for t in tqdm(range(INITS[domain][2][0], INITS[domain][2][1]+1), desc='t: ', leave=False):
                    if domain in ['mini', 'simplified']:
                        for vy in tqdm(range(INITS[domain][3][0], INITS[domain][3][1]+1), desc='vy: ', leave=False):
                            if x == 0 and y == 1 and vy == -2:
                                continue
                            else:
                                plan_and_write(domain, [x,y,t,vy])
                    else:
                        plan_and_write(domain, [x,y,t])

