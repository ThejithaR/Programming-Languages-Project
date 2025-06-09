# Programming-Languages-Project

This project is a compiler built in Python for the RPAL language.

## Usage

- `input.rpal` is at the root
- `./test/ex7.rpal` is the path to other test programs file 
- To run other test programs replace `input.rpal` with `./test/ex7.rpal` in each command

To compile and run an RPAL program, use the following command in `Programming-Languages-Project>` directory:

```bash
 python .\myrpal.py input.rpal
```

To print the Abstract syntax tree of the program, use the following command in `Programming-Languages-Project>` directory:

```bash
 python .\myrpal.py input.rpal -ast
```

To print the Standardized Abstract syntax tree of the program, use the following command in `Programming-Languages-Project>` directory:

```bash
 python .\myrpal.py input.rpal -st
```

`input.rpal` is the example program in the project description and there are other test programs in `test` folder named as `ex1.rpal`,`ex2.rpal`...etc.