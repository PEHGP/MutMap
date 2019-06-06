
import os
import sys
import argparse
import configparser
from multiprocessing import Pool
import multiprocessing as multi
from utils import time_stamp


class Params(object):

    def __init__(self, program_name):
        self.program_name = program_name

    def set_options(self):
        if self.program_name == 'mutmap':
            parser = self.mutmap_options()
        elif self.program_name == 'mutplot':
            parser = self.mutplot_options()

        if len(sys.argv) == 1:
            args = parser.parse_args(['-h'])
        else:
            args = parser.parse_args()
        config = self.read_config()
        return args, config

    def mutmap_options(self):
        parser = argparse.ArgumentParser(description='MutMap version 2.0.3',
                                         formatter_class=argparse.RawTextHelpFormatter)
        parser.usage = ('mutmap -r <FASTA> -c <BAM | FASTQ> -b <BAM | FASTQ>\n'
                        '              -n <INT> -o <OUT_DIR> [-T] [-e <DATABASE>]')

        # set options
        parser.add_argument('-r',
                            '--ref',
                            action='store',
                            required=True,
                            type=str,
                            help='Reference fasta.',
                            metavar='')

        parser.add_argument('-c',
                            '--cultivar',
                            action='append',
                            required=True,
                            type=str,
                            help=('fastq or bam of cultivar. If you specify\n'
                                  'fastq, please separate pairs by commma,\n'
                                  'e.g. -c fastq1,fastq2. You can use this\n'
                                  'optiion multiple times'),
                            metavar='')

        parser.add_argument('-b',
                            '--bulk',
                            action='append',
                            required=True,
                            type=str,
                            help=('fastq or bam of mutnat bulk. If you specify\n'
                                  'fastq, please separate pairs by commma,\n'
                                  'e.g. -b fastq1,fastq2. You can use this\n'
                                  'optiion multiple times'),
                            metavar='')

        parser.add_argument('-n',
                            '--N-bulk',
                            action='store',
                            required=True,
                            type=int,
                            help='Number of individuals in mutant bulk.',
                            metavar='')

        parser.add_argument('-o',
                            '--out',
                            action='store',
                            required=True,
                            type=str,
                            help=('Output directory. Specified name must not\n'
                                  'exist.'),
                            metavar='')

        parser.add_argument('-t',
                            '--threads',
                            action='store',
                            default=2,
                            type=int,
                            help=('Number of threads. If you specify the number\n'
                                  'below one, then, MutMap will use the threads\n'
                                  'as many as possible. [2]'),
                            metavar='')

        parser.add_argument('-T',
                            '--trim',
                            action='store_true',
                            default=False,
                            help='Trim fastq by trimmomatic.')

        parser.add_argument('-e',
                            '--snpEff',
                            action='store',
                            type=str,
                            help=('Predicte causal variant by SnpEff. Please check\n'
                                  'available databases in SnpEff.'),
                            metavar='')

        # set version
        parser.add_argument('-v',
                            '--version',
                            action='version',
                            version='%(prog)s 0.0.2')

        return parser

    def mutplot_options(self):
        parser = argparse.ArgumentParser(description='MutPlot version 0.0.3',
                                         formatter_class=argparse.RawTextHelpFormatter)
        parser.usage = ('mutplot -v <VCF> -o <OUT_DIR> -n <INT> [-w <INT>] [-s <INT>]\n'
                        '               [-D <INT>] [-d <INT>] [-N <INT>] [-m <FLOAT>]\n'
                        '               [-S <INT>] [-e <DATABASE>] [--igv] [--indel]')

        # set options
        parser.add_argument('-v',
                            '--vcf',
                            action='store',
                            required=True,
                            type=str,
                            help='VCF which contains cultivar and mutant bulk.',
                            metavar='')

        parser.add_argument('-o',
                            '--out',
                            action='store',
                            required=True,
                            type=str,
                            help='Output directory. Specified name can exist.',
                            metavar='')

        parser.add_argument('-n',
                            '--N-bulk',
                            action='store',
                            required=True,
                            type=int,
                            help='Number of individuals in mutant bulk.',
                            metavar='')

        parser.add_argument('-w',
                            '--window',
                            action='store',
                            default=2000,
                            type=int,
                            help='Window size (kb). [2000]',
                            metavar='')

        parser.add_argument('-s',
                            '--step',
                            action='store',
                            default=100,
                            type=int,
                            help='Step size (kb). [100]',
                            metavar='')

        parser.add_argument('-D',
                            '--max-depth',
                            action='store',
                            default=250,
                            type=int,
                            help='Maximum depth of variants which will be used. [250]',
                            metavar='')

        parser.add_argument('-d',
                            '--min-depth',
                            action='store',
                            default=8,
                            type=int,
                            help='Minimum depth of variants which will be used. [8]',
                            metavar='')

        parser.add_argument('-N',
                            '--N-rep',
                            action='store',
                            default=10000,
                            type=int,
                            help=('Number of replicates for simulation to make \n'
                                  'null distribution. [10000]'),
                            metavar='')

        parser.add_argument('-m',
                            '--min-SNPindex',
                            action='store',
                            default=0.3,
                            type=float,
                            help='Cutoff of minimum SNP-index for clear results. [0.3]',
                            metavar='')

        parser.add_argument('-S',
                            '--strand-bias',
                            action='store',
                            default=7,
                            type=int,
                            help=('Filter spurious homo genotypes in cultivar using\n'
                                  'strand bias. If ADF (or ADR) is higher than this\n'
                                  'cutoff when ADR (or ADF) is 0, that SNP will be\n'
                                  'filtered out. If you want to supress this filtering,\n'
                                  'please set this cutoff to 0. [7]\n'),
                            metavar='')

        parser.add_argument('-e',
                            '--snpEff',
                            action='store',
                            type=str,
                            help=('Predicte causal variant by SnpEff. Please check\n'
                                  'available databases in SnpEff.'),
                            metavar='')

        parser.add_argument('--igv',
                            action='store_true',
                            default=False,
                            help='Output IGV format file to check results on IGV.')

        parser.add_argument('--indel',
                            action='store_true',
                            default=False,
                            help='Plot SNP-index with INDEL.')

        # set version
        parser.add_argument('--version',
                            action='version',
                            version='%(prog)s 0.0.1')

        return parser

    def read_config(self):
        config = configparser.ConfigParser()
        path_to_mutmap = os.path.realpath(__file__)
        mutmap_dir = os.path.dirname(path_to_mutmap)
        config.read('{}/../config/config.ini'.format(mutmap_dir))
        return config

    def check_max_threads(self, args):
        max_cpu = multi.cpu_count()
        print(time_stamp(),
              'max number of threads which you can use is {}.'.format(max_cpu),
              flush=True)
        if max_cpu <= args.threads:
            sys.stderr.write(('!!WARNING!! You can use up to {0} threads. '
                              'This program will use {0} threads.\n').format(max_cpu))
            sys.stderr.flush()
            args.threads = max_cpu
        elif args.threads < 1:
            args.threads = max_cpu
        return args

    def check_args(self, args):
        if os.path.isdir(args.out):
            sys.stderr.write(('  Output directory already exist.\n'
                              '  Please rename output directory or '
                                'remove existing directory\n\n'))
            sys.exit()

        N_cultivar_fastq = 0
        N_cultivar_bam = 0

        for input_name in  args.cultivar:
            n_comma = input_name.count(',')
            if n_comma == 0:
                root, ext = os.path.splitext(input_name)
                if ext != '.bam':
                    sys.stderr.write(('  Please check "{}".\n'
                                      '  The extension of this file is not "bam".\n'
                                      '  If you wanted to specify fastq, please '
                                        'input them as paired-end reads which is separated '
                                        'by comma. e.g. -c fastq1,fastq2\n\n').format(input_name))
                    sys.exit()
                N_cultivar_bam += 1
            elif n_comma == 1:
                fastqs = input_name.split(',')
                for fastq in fastqs:
                    root, ext = os.path.splitext(fastq)
                    if ext == '.bam':
                        sys.stderr.write(('  Please check "{}".\n'
                                          '  The extension must not be "bam".\n'
                                          '  If you wanted to specify bam, please '
                                            'input them separately. e.g. -c bam1 '
                                            '-c bam2\n\n').format(input_name))
                        sys.exit()
                N_cultivar_fastq += 1
            else:
                sys.stderr.write(('  Please check "{}".\n'
                                  '  You specified too much files, or '
                                    'your file name includes ",".\n\n').format(input_name))
                sys.exit()

        N_bulk_fastq = 0
        N_bulk_bam = 0

        for input_name in  args.bulk:
            n_comma = input_name.count(',')
            if n_comma == 0:
                root, ext = os.path.splitext(input_name)
                if ext != '.bam':
                    sys.stderr.write(('  Please check "{}".\n'
                                      '  The extension of this file is not "bam".\n'
                                      '  If you wanted to specify fastq, please '
                                        'input them as paired-end reads which is separated '
                                        'by comma. e.g. -b fastq1,fastq2\n\n').format(input_name))
                    sys.exit()
                N_bulk_bam += 1
            elif n_comma == 1:
                fastqs = input_name.split(',')
                for fastq in fastqs:
                    root, ext = os.path.splitext(fastq)
                    if ext == '.bam':
                        sys.stderr.write(('  Please check "{}".\n'
                                          '  The extension must not be "bam".\n'
                                          '  If you wanted to specify bam, please '
                                            'input them separately. e.g. -b bam1 '
                                            '-b bam2\n\n').format(input_name))
                        sys.exit()
                N_bulk_fastq += 1
            else:
                sys.stderr.write(('  Please check "{}".\n'
                                  '  You specified too much files, or '
                                    'your file name includes ",".\n\n').format(input_name))
                sys.exit()

        N_fastq = N_cultivar_fastq + N_bulk_fastq
        if N_fastq == 0 and args.trim:
            sys.stderr.write(('  You can specify "--trim" only when '
                                 'you input fastq.\n\n'))
            sys.exit()

        return N_cultivar_fastq, N_cultivar_bam, N_bulk_fastq, N_bulk_bam
