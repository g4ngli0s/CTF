
## **Enunciado**

Te daban el binario de 64 bits de un servicio corriendo en una máquina remota para que le pases un shellcode y puedes explotarlo para conseguir una shell y poder leer la flag.

## **Solución**

Hay que pasarle un shellcode de 24 bytes donde no se repita ningún opcode. No vale pasar el filtro de superar esos 24 bytecode que sean diferentes y luego poner detrás tu shellcode clásico de msfvenom. 
