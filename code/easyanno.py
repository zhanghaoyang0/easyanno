import os
import sys
import time
import argparse
import subprocess
import pandas as pd
import numpy as np

start = time.time()
### flags parser
parser = argparse.ArgumentParser(description='easyanno')
parser.add_argument('--build', type=str, default='hg19')
parser.add_argument('--chr_col', type=str, default='CHR')
parser.add_argument('--pos_col', type=str, default='POS')
parser.add_argument('--ref_col', type=str, default='A2')
parser.add_argument('--alt_col', type=str, default='A1')
parser.add_argument('--file_in', type=str, default='./example/df_hg19.txt')
parser.add_argument('--file_out', type=str, default='./example/df_hg19_annoed.txt')
parser.add_argument('--only_find_gene', type=str, default='T')
parser.add_argument('--anno_dbnsfp', type=str, default='F')
args = parser.parse_args()

build = args.build
chr_col = args.chr_col; pos_col = args.pos_col; ref_col = args.ref_col; alt_col = args.alt_col
file_in = args.file_in; file_out = args.file_out
only_find_gene = args.only_find_gene; anno_dbnsfp = args.anno_dbnsfp

# # default setting
# build = 'hg19'
# chr_col = 'CHR'
# pos_col = 'POS'
# ref_col = 'A2'
# alt_col = 'A1'
# file_in = './example/df_hg19.txt'
# file_out = './example/df_hg19_annoed.txt'
# only_find_gene = 'F'
# anno_dbnsfp = 'F'

###
print('setting:')
print('build: '+ build)
print('chr_col: '+ chr_col); print('pos_col: '+ pos_col); print('ref_col: '+ ref_col); print('alt_col: '+ alt_col)
print('file_in: '+ file_in); print('file_out: '+ file_out)
print('only_find_gene: '+ only_find_gene)
print('anno_dbnsfp: '+ anno_dbnsfp)

only_find_gene = True if only_find_gene =='T' else False
# id for temp files
temp_id = hash(file_in)
temp_id = str(temp_id+sys.maxsize) if temp_id<0 else str(temp_id)
# read input
print(f'loading input...')
if file_in.endswith('.gz'): df = pd.read_csv(file_in, compression='gzip', sep='\t')
else: df = pd.read_csv(file_in, sep='\t')

df.replace(23, 'X', inplace=True)
df.replace(24, 'Y', inplace=True)
df['id'] = df.index
df['dot'] = '.'
# make vcf
vcf = df[[chr_col, pos_col, 'dot', ref_col, alt_col, 'dot', 'dot', 'id']].copy().dropna()
vcf[[pos_col]] = vcf[[pos_col]].astype(int)
vcf.to_csv('temp/'+temp_id+'.vcf', sep='\t', index=False, header = False)

# annovar
print(f'using annovar to annotate...')

if anno_dbnsfp == 'F':
    annovar_command = f'annovar/table_annovar.pl temp/{temp_id}.vcf annovar/humandb/ -buildver {build} --out temp/{temp_id} \
    -remove -protocol refGene -operation g -nastring . -vcfinput -polish'
else: 
    annovar_command = f'annovar/table_annovar.pl temp/{temp_id}.vcf annovar/humandb/ -buildver {build} --out temp/{temp_id} \
    -remove -protocol refGene,dbnsfp42c -operation g,f -nastring . -vcfinput -polish'

subprocess.Popen(annovar_command, shell=True).wait()


# add new pos
anno = pd.read_csv(f'temp/{temp_id}.{build}_multianno.txt', sep='\t')
anno = anno.rename(columns={anno.columns[-1]: 'id'})
map = anno.loc[:, ~anno.columns.str.contains('Otherinfo')]

if only_find_gene==True: map = map[['id', 'Func.refGene', 'Gene.refGene']]

res = df.merge(map, on='id', how='left').drop(['id', 'dot'], axis=1) 

# save
res.to_csv(file_out, sep='\t', index=False)
print(f'deleting temporary files...')
rm_command = f'rm -rf temp/{temp_id}*'
subprocess.Popen(rm_command, shell=True).wait()
nsnp = len([x for x in res['Gene.refGene'] if x not in ['NONE;NONE', '.']])
print(f'{nsnp} snp are annotated successfully')
print(f'done!')
end = time.time()
print (f'spend {time.strftime("%M min %S sec", time.gmtime(end-start))}')