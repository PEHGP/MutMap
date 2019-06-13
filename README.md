# MutMap User Guide
#### version 2.0.6

## Table of contents
- [What is MutMap?](#What-is-MutMap)
- [Installation](#Installation)
  + [Dependencies](#Dependencies)
  + [Installation using bioconda](#Installation-using-bioconda)
  + [Manual Installation](#Manual-Installation)
- [Usage](#Usage)
  + [Example 1 : run MutMap from FASTQ without trimming](#Example-1--run-MutMap-from-FASTQ-without-trimming)
  + [Example 2 : run MutMap from FASTQ with trimming](#Example-2--run-MutMap-from-FASTQ-with-trimming)
  + [Example 3 : run MutMap from BAM](#Example-3--run-MutMap-from-BAM)
  + [Example 4 : run MutMap from multiple FASTQs and BAMs](#Example-4--run-MutMap-from-multiple-FASTQs-and-BAMs)
  + [Example 5 : run MutPlot from VCF](#Example-5--run-MutPlot-from-VCF)
- [Outputs](#Outputs)
- [Advanced usage](#Advanced-usage)
  + [Detect causal variant using SnpEff](#Detect-causal-variant-using-SnpEff)
  + [Change trimming parameters for Trimmomatic](#Change-trimming-parameters-for-Trimmomatic)

## What is MutMap?

Now MutMap is updated for easier installation and utilization using Python platform.

**Citation: Abe, A. et al. (2012) Genome sequencing reveals agronomically important loci in rice using MutMap. Nature Biotechnol. 30:174-179.**

## Installation
### Dependencies
#### Softwares
- [BWA](http://bio-bwa.sourceforge.net/)
- [SAMtools](http://samtools.sourceforge.net/)
- [BCFtools](http://samtools.github.io/bcftools/)
- [SnpEff](http://snpeff.sourceforge.net/)
- [Trimmomatic](http://www.usadellab.org/cms/?page=trimmomatic)

#### Python libraries
- matplotlib
- numpy
- pandas
- seaborn (optional)

### Installation using bioconda
You can install MutMap using [bioconda](https://bioconda.github.io/index.html).
```
$ conda install -c bioconda mutmap
```

### Mannual Installation
If you got a error during installation, you can install MutMap, manually.
```
$ git clone https://github.com/YuSugihara/MutMap.git
$ cd MutMap
$ pip install -e .
```
Then you have to install other dependencies by yourself. We highly recommend you to install SnpEff and Trimmomatic using bioconda.
```
$ conda install -c bioconda snpeff
$ conda install -c bioconda triimomatic
```
After installation, please check whether SnpEff and Trimmomatic work through the commands below.
```
$ snpEff --help
$ trimmomatic --help
```

## Usage
```
$ mutmap -h

usage: mutmap -r <FASTA> -c <BAM | FASTQ> -b <BAM | FASTQ>
              -n <INT> -o <OUT_DIR> [-T] [-e <DATABASE>]

MutMap version 2.0.3

optional arguments:
  -h, --help        show this help message and exit
  -r , --ref        Reference fasta.
  -c , --cultivar   fastq or bam of cultivar. If you specify
                    fastq, please separate pairs by commma,
                    e.g. -c fastq1,fastq2. You can use this
                    optiion multiple times
  -b , --bulk       fastq or bam of mutnat bulk. If you specify
                    fastq, please separate pairs by commma,
                    e.g. -b fastq1,fastq2. You can use this
                    optiion multiple times
  -n , --N-bulk     Number of individuals in mutant bulk.
  -o , --out        Output directory. Specified name must not
                    exist.
  -t , --threads    Number of threads. If you specify the number
                    below one, then, MutMap will use the threads
                    as many as possible. [2]
  -T, --trim        Trim fastq by trimmomatic.
  -e , --snpEff     Predicte causal variant by SnpEff. Please check
                    available databases in SnpEff.
  -v, --version     show program's version number and exit
```

MutMap can run from FASTQ (without or with trimming) and BAM. If you want to run MutMap from VCF, please use MutPlot (example 5). Once you run MutMap, MutMap automatically complete the subprocesses.

+ [Example 1 : run MutMap from FASTQ without trimming](#Example-1--run-MutMap-from-FASTQ-without-trimming)
+ [Example 2 : run MutMap from FASTQ with trimming](#Example-2--run-MutMap-from-FASTQ-with-trimming)
+ [Example 3 : run MutMap from BAM](#Example-3--run-MutMap-from-BAM)
+ [Example 4 : run MutMap from multiple FASTQs and BAMs](#Example-4--run-MutMap-from-multiple-FASTQs-and-BAMs)
+ [Example 5 : run MutPlot from VCF](#Example-5--run-MutPlot-from-VCF)



### Example 1 : run MutMap from FASTQ without trimming
```
$ mutmap -r reference.fasta \
         -c cultivar.1.fastq,cultivar.2.fastq \
         -b bulk.1.fastq,bulk.2.fastq \
         -n 20 \
         -o example_dir
```

`-r` : reference fasta

`-c` : FASTQs of cultivar. Please input pair-end reads separated by comma. FASTQs can be gzipped.

`-b` : FASTQs of bulk. Please input pair-end reads separated by comma. FASTQs can be gzipped.

`-n` : number of individuals in mutant bulk.

`-o` : name of output directory. Specified name cannot exist.

### Example 2 : run MutMap from FASTQ with trimming
```
$ mutmap -r reference.fasta \
         -c cultivar.1.fastq,cultivar.2.fastq \
         -b bulk.1.fastq,bulk.2.fastq \
         -n 20 \
         -o example_dir \
         -T
```

`-r` : reference fasta

`-c` : FASTQs of cultivar. Please input pair-end reads separated by comma. FASTQs can be gzipped.

`-b` : FASTQs of bulk. Please input pair-end reads separated by comma. FASTQs can be gzipped.

`-n` : number of individuals in mutant bulk.

`-o` : name of output directory. Specified name cannot exist.

`-T` : trim your reads by triimomatic.

### Example 3 : run MutMap from BAM
```
$ mutmap -r reference.fasta \
         -c cultivar.bam \
         -b bulk.bam \
         -n 20 \
         -o example_dir
```

`-r` : reference fasta

`-c` : BAM of cultivar.

`-b` : BAM of bulk.

`-n` : number of individuals in mutant bulk.

`-o` : name of output directory. Specified name cannot exist.

### Example 4 : run MutMap from multiple FASTQs and BAMs
```
$ mutmap -r reference.fasta \
         -c cultivar_1.1.fastq,cultivar_1.2.fastq \
         -c cultivar_1.bam \
         -b bulk_1.1.fastq,bulk_1.2.fastq \
         -b bulk_2.bam \
         -b bulk_3.bam \
         -n 20 \
         -o example_dir
```

MutMap can automatically merge multiple FASTQs and BAMs. Of course, you can merge FASTQs or BAMs using `cat` or `samtools merge` before input them to MutMap. If you specify `-c` multiple times, please make sure that those files include only 1 individual. On the other hand, `-b` can include more than 1 individuals because those are bulked samples. MutMap can automatically classify FASTQs and BAMs from whether comma exits or not. 

### Example 5 : run MutPlot from VCF
```
$ mutplot -h

usage: mutplot -v <VCF> -o <OUT_DIR> -n <INT> [-w <INT>] [-s <INT>]
               [-D <INT>] [-d <INT>] [-N <INT>] [-m <FLOAT>]
               [-S <INT>] [-e <DATABASE>] [--igv] [--indel]

MutPlot version 0.0.3

optional arguments:
  -h, --help            show this help message and exit
  -v , --vcf            VCF which contains cultivar and mutant bulk.
  -o , --out            Output directory. Specified name can exist.
  -n , --N-bulk         Number of individuals in mutant bulk.
  -w , --window         Window size (kb). [2000]
  -s , --step           Step size (kb). [100]
  -D , --max-depth      Maximum depth of variants which will be used. [250]
  -d , --min-depth      Minimum depth of variants which will be used. [8]
  -N , --N-rep          Number of replicates for simulation to make
                        null distribution. [10000]
  -m , --min-SNPindex   Cutoff of minimum SNP-index for clear results. [0.3]
  -S , --strand-bias    Filter spurious homo genotypes in cultivar using
                        strand bias. If ADF (or ADR) is higher than this
                        cutoff when ADR (or ADF) is 0, that SNP will be
                        filtered out. If you want to supress this filtering,
                        please set this cutoff to 0. [7]
  -e , --snpEff         Predicte causal variant by SnpEff. Please check
                        available databases in SnpEff.
  --igv                 Output IGV format file to check results on IGV.
  --indel               Plot SNP-index with INDEL.
  --version             show program's version number and exit
```
MutPlot is included in MutMap. MutMap run MutPlot after making VCF. Then, MutPlot will work with default parameters. If you want to change some parameters, you can use VCF inside of `(OUT_DIR/30_vcf/mutmap.vcf.gz)` to retry plotting process like below.

```
$ mutplot -v OUT_DIR/30_vcf/mutmap.vcf.gz \
          -o ANOTHER_DIR_NAME \
          -n 20 \
          -w 2000 \
          -s 100
```

#### Use MutPlot for VCF which was made by yourself
In this case, please make sure that:
1. Your VCF include AD format.
2. Your VCF include two columns of cultivar and mutant bulk in this order.

If you got a error, please try to run MutMap from FASTQ or BAM before asking in issues.

## Outputs
Inside of `OUT_DIR` is like below.
```
|-- 10_ref
|   |-- reference.fasta
|   |-- reference.fasta.amb
|   |-- reference.fasta.ann
|   |-- reference.fasta.bwt
|   |-- reference.fasta.fai
|   |-- reference.fasta.pac
|   `-- reference.fasta.sa
|-- 20_bam
|   |-- bulk.filt.bam
|   |-- bulk.filt.bam.bai
|   |-- cultivar.filt.bam
|   `-- cultivar.filt.bam.bai
|-- 30_vcf
|   |-- mutmap.vcf.gz
|   `-- mutmap.vcf.gz.tbi
|-- 40_mutmap
|   |-- snp_index.tsv
|   |-- sliding_window.tsv
|   `-- mutmap_plot.png
`-- log
    |-- bcftools.log
    |-- bgzip.log
    |-- bwa.log
    |-- mutplot.log
    |-- samtools.log
    `-- tabix.log
```
- If you run MutMap with trimming, you will get the directory of `00_fastq` which includes FASTQs after trimming.
- You can check the results in `40_mutmap`.
  + `snp_index.tsv` : columns in this order.
    - **CHROM** : chromosome name
    - **POSI** : position in chromosome
    - **VARIANT** : SNP or INDEL
    - **DEPTH** : depth of bulk
    - **p99** : 99% confidence interval of simulated SNP-index
    - **p95** : 95% confidence interval of simulated SNP-index
    - **SNP-index** : real SNP-index
  + `sliding_window.tsv` : columns in this order.
    - **CHROM** : chromosome name
    - **POSI** : central position of window
    - **MEAN p99** : mean of p99
    - **MEAN p95** : mean of p95
    - **MEAN SNP-index** : mean SNP-index
  + `mutmap_plot.png` : resulting plot
    - **<span style="color: blue; ">BLUE dot</span>** : variant
    - **<span style="color: red; ">RED line</span>** : mean SNP-index
    - **<span style="color: orange; ">ORANGE line</span>** : mean p99
    - **<span style="color: green; ">GREEN line</span>** : mean p95

## Advanced usage
### Detect causal variant using SnpEff
preparing now...
### Change trimming parameters for Trimmomatic
preparing now...
