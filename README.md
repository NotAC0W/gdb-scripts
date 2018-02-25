# Various GDB Scripts





### wasm.py
Write assembler on the fly into memory
```
wasm                              - Shows context used
wasm <assembler code ... >        - Write at current $pc
wasm <addr> <assembler code ... > - Write at address <addr>
wasm context <context>            - Set context for pwntools asm to <context>. no argument unsets context
```
Requires pwnlib / pwntools to be installed


```GDB
$ gdb ./a.out 
Reading symbols from ./a.out...done.
(gdb) source wasm.py 
(gdb) b 8
Breakpoint 1 at 0x6b4: file lol.c, line 8.
(gdb) r
Starting program: /home/user/gdb-scripts/a.out 

Breakpoint 1, main (argc=1, argv=0x7fffffffe2d8) at lol.c:8
8		a += a*a*a*a*a;
(gdb) x/6i $pc
=> 0x5555555546b4 <main+42>:	mov    -0x4(%rbp),%eax
   0x5555555546b7 <main+45>:	imul   -0x4(%rbp),%eax
   0x5555555546bb <main+49>:	imul   -0x4(%rbp),%eax
   0x5555555546bf <main+53>:	imul   -0x4(%rbp),%eax
   0x5555555546c3 <main+57>:	lea    0x1(%rax),%edx
   0x5555555546c6 <main+60>:	mov    -0x4(%rbp),%eax
(gdb) wasm mov eax, [rbp-4]; jmp $+12;
(gdb) x/6i $pc
=> 0x5555555546b4 <main+42>:	mov    -0x4(%rbp),%eax
   0x5555555546b7 <main+45>:	jmp    0x5555555546c3 <main+57>
   0x5555555546b9 <main+47>:	rex.RB cld 
   0x5555555546bb <main+49>:	imul   -0x4(%rbp),%eax
   0x5555555546bf <main+53>:	imul   -0x4(%rbp),%eax
   0x5555555546c3 <main+57>:	lea    0x1(%rax),%edx
(gdb) 

```

