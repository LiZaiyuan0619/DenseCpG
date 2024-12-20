# DenseCpG

DenseCpG: Single-Cell Methylome Imputation with Dense Block

# Data

> **Suggestions:**
>
> - Ensure at least 600GB of free space is available for each dataset. It is highly recommended to avoid using external hard drives as they have significant read/write speed limitations.
> - It is recommended to use a VPN to speed up the download. Each dataset download should ensure at least 100GB of traffic.
> - It is recommended to perform a backup right after downloading the dataset.
> - The downloaded `download*.py`, `untar*.py`, and `unzip*.py` scripts are equipped with interruption handling.You can interrupt and resume processing at any time.
> - To interrupt the `Encode.py` script, it must be done after processing each subdirectory and displaying the saved progress.
>
> **Notes:**
>
> - The `Combine*.py` scripts do not have interruption handling, but the combination process itself is quick.
> - The complete process for acquiring each dataset takes approximately 24 hours, depending on download speed, memory read/write, and other factors.
>
> For more information, see [CpG Trans](https://github.com/gdewael/cpg-transformer) and [GraphCpG](https://github.com/yuzhong-deng/graphcpg).

## Homo

First, download the raw cell archive of the new dataset from the link in the table:

```shell
python downloadHomoLuo.py
```

Extract the `.gz` files into directories by cell unit:

```
python untarHomoLuo.py
```

For each directory, extract the chromosome archives into `.tsv` format:

```
python unzipHomoLuo.py
```

Encode the loci for each cell:

```
python Encode.py
```

Combine all the cells together:

```
python CombineEncodedLabelsHomo.py
```

## Mouse

First, download the raw cell archive of the new dataset from the link in the table:

```
python downloadMouseLuo.py
```

Extract the `.gz` files into directories by cell unit:

```
python untarMouseLuo.py
```

For each directory, extract the chromosome archives into `.tsv` format:

```
python unzipMouseLuo.py
```

Encode the loci for each cell:

```
python Encode.py
```

Combine all the cells together:

```
python Combine.py
```

## Others

[CpG Trans](https://github.com/gdewael/cpg-transformer) 

# Environment

```shell
conda create -n DenseCpG python=3.8

conda activate DenseCpG

pip install torch==1.12.1+cu113 torchvision==0.13.1+cu113 torchaudio==0.12.1 --extra-index-url https://download.pytorch.org/whl/cu113
or
pip install torch==1.12.0+cu113 torchvision==0.13.0+cu113 torchaudio==0.12.0 --extra-index-url https://download.pytorch.org/whl/cu113

pip install torchmetrics==0.7.0

pip install transformers==4.29.2

pip install tabulate

pip install torch-scatter torch-sparse torch-cluster torch-spline-conv torch-geometric==2.1.0 -f https://data.pyg.org/whl/torch-1.12.1+cu113.html

pip install pip==23.1.2

pip install pytorch-lightning==1.8.0

pip install numpy==1.26.4

pip install einops
```
