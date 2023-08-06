fastanalizer - Fast protein domain analysis tool
=============================================

Installation
------------

You can install fastanalize like any other Python package,
using ``pip`` to download it from PyPI_::

    $ pip install fastanalize

or using ``setup.py`` if you have downloaded the source package locally::

    $ python setup.py build
    $ sudo python setup.py install


Usage
-----

After installation, to use `` fastanalizer`` just invoke it in the folder where the multifasta is located:

    $ fastanalizer myfasta.fa

You may also define a title to your job:

    $ fastanalizer --title "Example" myfasta.fa

It is possible to define the type of image output. Default is HTML.

    $ fastanalizer --output SVG myfasta.fa

Example
-------

Fastanalizer performs protein sequence analysis in 5 steps:


1. **Fasta sequences analysis:**

    The first step analyzes basic metrics of the delivered multifast, such as quantity and size of sequences, shortest and longest sequences, standard deviation between sequences size and the amino acid distribution of the sequences. The results are saved in the ``general`` folder.

.. image:: https://github.com/alezanatta/fastanalizer/blob/main/example/svg/general/metrics.svg
    :width: 1000
    :alt: Fasta metrics

.. image:: https://github.com/alezanatta/fastanalizer/blob/main/example/svg/general/aa.svg
    :width: 1000
    :alt: Amino acid distribution


2. **Functional domains analysis:**

    The second step is the search for functional domains in the delivered proteins. The analysis is done using the NCBI Batch Cd-Search. The results are saved in the ``domainsearch`` folder. Each file inside the folder has a maximum information of 2000 sequences. There is no limit to the total number of sequences and the execution time of this step varies according to the number of sequences provided.


3. **Sequence trimming**

    The search results from step 2 are used to select the function domain by parsimony: the domain with the highest amount of specific hits is used to cut the given sequences. Sequences with incomplete domain are discarded.

.. image:: https://github.com/alezanatta/fastanalizer/blob/main/example/svg/pdomain/pdomain.svg
    :width: 1000
    :alt: Protein domain specific hits


4. **Sequence alignment**

    The trimmed sequences are align. Fastanalizer utilizes MAFFT with automatic settings to align. The results are saved in the ``align`` folder. The sequences used for the alignment are in ``job.fasta``. The supplied multifasta is the ``base.fasta`` and the align sequences is ``align.fasta``. Sequences are rename for better presentation at the phylogenetic analysis. The file ``rename.txt`` has the from-to table. MAFFT output can be found in ``align-stderr.fasta``


5. **Phylogenetic analysis**

    A Neighboor joining tree created using BioPython Phylo module.

.. image:: https://github.com/alezanatta/fastanalizer/blob/main/example/svg/tree/tree.svg
    :width: 1000
    :alt: Phylogenetic tree as graph


Changelog
---------

    Under construction