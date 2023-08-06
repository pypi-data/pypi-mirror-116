# pmc-mapper

A Python Library that map PubMed Central XML to Python object.

## installation

```
pip install pmc-mapper
```

## usage

### library

```python
from pmc_mapper import Article


# parse file
at1 = Article.from_file('PMC8353774.nxml')
at2 = Article.from_pmc_id('PMC8353774')


# journal
print(at2.journal.title)
# output
# BMC Bioinformatics

# article ids
for at_id in at2.ids:
    print(f'type: {at_id.type}, value: {at_id.value}')
# output:
# type: pmid, value: 34376148
# type: pmc, value: 8353774
# type: publisher-id, value: 4312
# type: doi, value: 10.1186/s12859-021-04312-3
```

### command line

```
pmc-mapper -i PMC8353774.nxml -o PMC8353774.jl
```