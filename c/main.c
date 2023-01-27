#include <stdio.h>

int main(int argc, char *argv[])
{

    FILE *fp;
    int bufferLength = 255; 
    char buffer[bufferLength];
    
    /* opening file for reading */
    fp = fopen("../mazes/maze01.txt", "r");
    if(fp == NULL)
    {
        perror("Error opening file");
        return -1;
    }

    while (fgets(buffer, bufferLength, fp))
    {
        printf("%s\n", buffer);
    }
    fclose(fp);

    return 0;
}