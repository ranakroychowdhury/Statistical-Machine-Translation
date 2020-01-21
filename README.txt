***[CSE 256 FA 19: Programming assignment 4: Machine Translation]***

You should be able to run:
 > python eval_alignment.py dev.key dev.out

***[ Files ]***

There are three python files in this folder and a README file:

- (IBM_Model1.py): This file implements the IBM Model 1. It saves the t parameter in t.json and generates the output in dev.out.

- (IBM_Model2.py): This file implements the IBM Model 2. It saves the t nd q parameter in t.json and q.json respectively. It generates the output in dev.out.

- (Growing_alignment.py): This file implements the growing alignment algorithm. It uses the dev1.out produced by IBM model 2 to translate Spanish to English and the dev2.out produced by IBM model 2 to translate English to Spanish. It generates the output in dev.out.

- (README): Contains all the necessary information about the file structure and information about each file. 

