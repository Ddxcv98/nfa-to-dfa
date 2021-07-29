# NFA to DFA

Conversion of NFA into DFA, minimization of DFA.

## Installing dependencies

```
pip install tabulate
```

## Help command

```
$ python main.py -h
usage: main.py [-h] [--nfa] [--dfa] [--preserve-nfa-sets] [--preserve-dfa-sets] [--minimize] input

positional arguments:
  input                File to parse

optional arguments:
  -h, --help           show this help message and exit
  --nfa                flag used when the input is a NFA
  --dfa                flag used when the input is a DFA
  --preserve-nfa-sets  keep the original sets when converting to a DFA
  --preserve-dfa-sets  keep the original sets when minimizing the DFA
  --minimize           get the minimized dfa; not needed when the input is a DFA
```

## Usage

First, you will always need an input JSON file, which may represent a NFA or a DFA. If the given input is a NFA it will
be converted into a DFA. In addition, you have the possibility to minimize the DFA. In case of a DFA, it will simply be
minimized. Find examples of files in the [examples](examples) folder.

### Converting a NFA into a DFA

The following command converts the NFA represented in [this](examples/nfa_example.json) example into a DFA.

```
$ python main.py --nfa --preserve-nfa-sets examples/nfa_example.json
+------------------+--------------+------+----------+
|                  |      a       |  b   |    c     |
+------------------+--------------+------+----------+
|    -> {q0}       |   {q1, q2}   |  -   |    -     |
|     {q1, q2}     | {q2, q3, q4} | {q1} | {q1, q2} |
| * {q2, q3, q4}   | {q2, q4, q5} | {q1} |   {q2}   |
|       {q1}       |     {q3}     | {q1} |   {q1}   |
| * {q2, q4, q5}   | {q2, q4, q5} | {q1} |   {q2}   |
|       {q2}       |   {q2, q4}   | {q1} |   {q2}   |
|       {q3}       |     {q5}     |  -   |    -     |
|   * {q2, q4}     | {q2, q4, q5} | {q1} |   {q2}   |
|     * {q5}       |      -       |  -   |    -     |
+------------------+--------------+------+----------+
```

Or, you can also have a simplified version, translating the original sets to letters.

```
$ python main.py --nfa examples/nfa_example.json 
+---------+---+---+---+
|         | a | b | c |
+---------+---+---+---+
| -> A    | B | - | - |
|    B    | C | D | B |
|  * C    | E | D | F |
|    D    | G | D | D |
|  * E    | E | D | F |
|    F    | H | D | F |
|    G    | I | - | - |
|  * H    | E | D | F |
|  * I    | - | - | - |
+---------+---+---+---+
```

### Minimizing a DFA

Using the same file, it is also possible to minimize the converted DFA.

```
$ python main.py --nfa --minimize examples/nfa_example.json
+---------+---+---+---+
|         | a | b | c |
+---------+---+---+---+
| -> A    | B | - | - |
|    B    | C | D | B |
|    D    | E | D | D |
|    E    | F | - | - |
|  * C    | C | D | B |
|  * F    | - | - | - |
+---------+---+---+---+
```

Or, you can input a DFA directly, represented in [this](examples/dfa_example.json) example.

```
$ python main.py --dfa --preserve-dfa-sets examples/dfa_example.json
+----------------+----------+----------+
|                |    0     |    1     |
+----------------+----------+----------+
| -> {q0, q4}    | {q1, q7} | {q3, q5} |
|    {q1, q7}    |   {q6}   |   {q2}   |
|      {q6}      |   {q6}   | {q0, q4} |
|    {q3, q5}    |   {q2}   |   {q6}   |
|    * {q2}      | {q0, q4} |   {q2}   |
+----------------+----------+----------+
```
