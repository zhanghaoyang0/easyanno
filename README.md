
# About easyanno
`easyanno` is a simple tool to do gene-based annotation (based on refGene) with genomic position.

# Why easyanno 
I make minor efforts to omit some laborious steps (i.e., prepare annovar input, annotate, and then map back to your files) in the use of `ANNOVAR`.
With `easyanno`, you can use a (tab separated) file (e.g., gwas summary) as input and obtain an output with annotations.

# Requirements 
- `Linux` 
- `ANNOVAR`
- `Python3` (3.9.6) with `pandas` (1.4.3), `numpy` (1.20.3), `argparse`, `os`, `sys`, `time`, `subprocess`  
  
Versions I used are in bracket

# Getting Started
Clone this repository via the commands:
```  
git clone https://github.com/zhanghaoyang0/easyanno.git
cd easyanno
```

Fill the form (https://www.openbioinformatics.org/annovar/annovar_download_form.php), open your email, find the download link (like http://xxx/annovar.latest.tar.gz).

Download ANNOVAR and hg38 refGene:
```
wget -c http://xxx/annovar.latest.tar.gz
tar zxvf annovar.latest.tar.gz
annovar/annotate_variation.pl -buildver hg38 -downdb -webfrom annovar refGene annovar/humandb/
```

Download dbnsfp if you need (they are LARGE):
```
annovar/annotate_variation.pl -buildver hg19 -downdb -webfrom annovar dbnsfp42c annovar/humandb/
annovar/annotate_variation.pl -buildver hg38 -downdb -webfrom annovar dbnsfp42c annovar/humandb/
```

Once the above has completed, you can try to annotate by specifying:  
`--build` hg19 or hg38, default is hg19   
`--only_find_gene` only find Func.refGene and Gene.refGene, T or F, default is T  
`--anno_dbnsfp` annotate dbnsfp, T or F, default is F  
`--chr_col` field name of CHR, default is CHR   
`--pos_col` field name of POS, default is POS   
`--ref_col` field name of REF, default is A2   
`--alt_col` field name of ALT, default is A1   
`--file_in` tab[\t] separated input file, gzip (file_in end with '.gz') input can also be recongized  
`--file_out` output file  

Two examples (one for hg19 and one for hg38):

```
python ./code/easyanno.py \
--build hg19 \
--only_find_gene F \
--anno_dbnsfp T \
--chr_col CHR --pos_col POS --ref_col A2 --alt_col A1 \
--file_in ./example/df_hg19.txt \
--file_out ./example/df_hg19_annoed.txt

python ./code/easyanno.py \
--build hg38 \
--only_find_gene T \
--anno_dbnsfp F \
--chr_col chrom --pos_col pos --ref_col ref --alt_col alt \
--file_in ./example/df_hg38.txt \
--file_out ./example/df_hg38_annoed.txt
```

gzip (file_in end with '.gz') input can be recongized: 
```
python ./code/easyanno.py \
--build hg19 \
--only_find_gene T \
--anno_dbnsfp F \
--chr_col CHR --pos_col POS --ref_col A2 --alt_col A1 \
--file_in ./example/df_hg19.txt.gz \
--file_out ./example/df_hg19_annoed.txt
```

The input file is like:
```
CHR     POS     A1      A2      FRQ     BETA    SE      P
2       48543917        A       G       0.4673  0.0045  0.0088  0.6101
5       87461867        A       G       0.7151  0.0166  0.0096  0.08397
14      98165673        T       C       0.1222  -0.0325 0.014   0.02035
12      104289454       T       C       0.534   0.0085  0.0088  0.3322
11      26254654        T       C       0.0765  0.0338  0.0167  0.04256
4       163471758       T       C       0.612   0.0119  0.0094  0.2057
```

If `easyanno` is running, you will see:
```
setting:
build: hg19
chr_col: CHR
pos_col: POS
ref_col: A2
alt_col: A1
file_in: ./example/df_hg19.txt
file_out: ./example/df_hg19_annoed.txt
only_find_gene: F
anno_dbnsfp: T
loading input...
using annovar to annotate...

...

deleting temporary files...
2000 snp are annotated (i.e., found Gene.refGene) successfully
done!
spend 00 min 05 sec
```

If you set `only_find_gene` as T, The output file is like:
```
CHR     POS     A1      A2      FRQ     BETA    SE      P       Func.refGene    Gene.refGene
2       48543917        A       G       0.4673  0.0045  0.0088  0.6101  intronic        FOXN2
5       87461867        A       G       0.7151  0.0166  0.0096  0.08397 intergenic      LINC02488;TMEM161B
14      98165673        T       C       0.1222  -0.0325 0.014   0.02035 intergenic      LINC02291;LINC02312
12      104289454       T       C       0.534   0.0085  0.0088  0.3322  ncRNA_intronic  TTC41P
11      26254654        T       C       0.0765  0.0338  0.0167  0.04256 intronic        ANO3
4       163471758       T       C       0.612   0.0119  0.0094  0.2057  intergenic      FSTL5;MIR4454
```

If you set `only_find_gene` as F, you get more information in refgene database:
```
CHR     POS     A1      A2      FRQ     BETA    SE      P       Func.refGene    Gene.refGene    GeneDetail.refGene      ExonicFunc.refGene      AAChange.refGene
2       48543917        A       G       0.4673  0.0045  0.0088  0.6101  intronic        FOXN2   .       .       .
5       87461867        A       G       0.7151  0.0166  0.0096  0.08397 intergenic      LINC02488;TMEM161B      dist=486641;dist=22266  .       .
14      98165673        T       C       0.1222  -0.0325 0.014   0.02035 intergenic      LINC02291;LINC02312     dist=12678;dist=49928   .       .
12      104289454       T       C       0.534   0.0085  0.0088  0.3322  ncRNA_intronic  TTC41P  .       .       .
11      26254654        T       C       0.0765  0.0338  0.0167  0.04256 intronic        ANO3    .       .       .
4       163471758       T       C       0.612   0.0119  0.0094  0.2057  intergenic      FSTL5;MIR4454   dist=386572;dist=542968 .       .
```

If you set `anno_dbnsfp` as T, you get much more information in refgene and dbnsfp database:
```
CHR     POS     A1      A2      FRQ     BETA    SE      P       Chr     Start   End     Ref     Alt     Func.refGene    Gene.refGene    GeneDetail.refGene       ExonicFunc.refGene      AAChange.refGene        SIFT_score      SIFT_converted_rankscore        SIFT_pred       SIFT4G_score    SIFT4G_converted_rankscore       SIFT4G_pred     LRT_score       LRT_converted_rankscore LRT_pred        MutationTaster_score    MutationTaster_converted_rankscore      MutationTaster_pred     MutationAssessor_score  MutationAssessor_rankscore      MutationAssessor_pred   FATHMM_score    FATHMM_converted_rankscore       FATHMM_pred     PROVEAN_score   PROVEAN_converted_rankscore     PROVEAN_pred    MetaSVM_score   MetaSVM_rankscoreMetaSVM_pred    MetaLR_score  MetaLR_rankscore        MetaLR_pred     MetaRNN_score   MetaRNN_rankscore       MetaRNN_pred    M-CAP_score     M-CAP_rankscore  M-CAP_pred      MutPred_score   MutPred_rankscore       MVP_score       MVP_rankscore   MPC_score       MPC_rankscore   PrimateAI_score  PrimateAI_rankscore     PrimateAI_pred  DEOGEN2_score   DEOGEN2_rankscore       DEOGEN2_pred    BayesDel_addAF_score    BayesDel_addAF_rankscore BayesDel_addAF_pred     BayesDel_noAF_score     BayesDel_noAF_rankscore BayesDel_noAF_pred      ClinPred_score  ClinPred_rankscore      ClinPred_pred    LIST-S2_score   LIST-S2_rankscore  LIST-S2_pred    Aloft_pred      Aloft_Confidence        DANN_score      DANN_rankscore  fathmm-MKL_coding_score  fathmm-MKL_coding_rankscore     fathmm-MKL_coding_pred  fathmm-XF_coding_score  fathmm-XF_coding_rankscore      fathmm-XF_coding_pred    Eigen-raw_coding        Eigen-raw_coding_rankscore      Eigen-PC-raw_coding     Eigen-PC-raw_coding_rankscore   integrated_fitCons_score integrated_fitCons_rankscore    integrated_confidence_valueGERP++_NR       GERP++_RS       GERP++_RS_rankscore     phyloP100way_vertebrate  phyloP100way_vertebrate_rankscore       phyloP30way_mammalian   phyloP30way_mammalian_rankscore phastCons100way_vertebrate      phastCons100way_vertebrate_rankscore     phastCons30way_mammalian        phastCons30way_mammalian_rankscore      SiPhy_29way_logOdds     SiPhy_29way_logOdds_rankscore    Interpro_domain GTEx_V8_gene    GTEx_V8_tissue
2       48543917        A       G       0.4673  0.0045  0.0088  0.6101  2       48543917        48543917        G       A       intronic        FOXN2  .       .       .       .       .       .       .       .       .       .       .       .       .       .       .       .       .       ..       .    .       .       .       .       .       .       .       .       .       .       .       .       .       .       .       .       ..       .       .      .       .       .       .       .       .       .       .       .       .       .       .       .       .       .       ..       .       ..       .       .       .       .       .       .       .       .       .       .       .       .       .       .       ..       .       .       .  .       .       .       .       .       .       .       .       .       .       .       .       .       .
5       87461867        A       G       0.7151  0.0166  0.0096  0.08397 5       87461867        87461867        G       A       intergenic      LINC02488;TMEM161B       dist=486641;dist=22266  .       .       .       .       .       .       .       .       .       .       .       .       ..       .    .       .       .       .       .       .       .       .       .       .       .       .       .       .       .       .       ..       .       .      .       .       .       .       .       .       .       .       .       .       .       .       .       .       .       ..       .       ..       .       .       .       .       .       .       .       .       .       .       .       .       .       .       ..       .       .       .  .       .       .       .       .       .       .       .       .       .       .       .       .       .       ..       .       .
```


# Acknowledgement
`easyanno` is based on `ANNOVAR`, please cite [ANNOVAR paper](https://academic.oup.com/nar/article/38/16/e164/1749458) if you use it.

# Feedback and comments
Add an issue or send email to zhanghaoyang0@hotmail.com