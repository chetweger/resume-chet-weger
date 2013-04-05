#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define TRUE 1
#define FALSE 0
//724

struct pair{
    int i;
    int j;
};

void makeBoard(int ** board, int dim){
    int i = 0;
    for(i;i<dim;i++){
        board[i] = (int *) malloc (sizeof(int)*dim);
    }
    i=0;
    int j = 0;
    for (i; i<dim; i++){
        j = 0;
        for (j; j<dim; j++){
            board[i][j] = 0;
        }
    }
}

void printBoard(int ** board, int dim){
    int i = 0;
    int j = 0;
    for (i; i<dim; i++){
        printf("[");
        j = 0;
        for (j; j+1<dim; j++){
            printf("%d,", board[i][j]);
        }
        printf("%d", board[i][j]);
        printf("]\n");
    }
}

struct pair nextify(int dim, struct pair pair){
    if (pair.i+1 == dim && pair.j+1 == dim){
        pair.i = -1;
        pair.j = -1;
        return pair;
    }
    if (pair.j+1 < dim){
        pair.j = pair.j + 1;
        return pair;
    }
    if (pair.j+1 == dim){
        pair.i = pair.i + 1;
        pair.j = 0;
        return pair;
    }
}

int rook(int ** board, int dim){
    int i = 0;
    int j = 0;
    int sum = 0;
    for (i;i<dim;i++){
        j = 0;
        sum = 0;
        for(j;j<dim;j++){
            sum = sum + board[i][j];
        }
        if (sum>1){ return FALSE; }
    }
    i=0;
    j=0;
    sum=0;
    for (j;j<dim;j++){
        i = 0;
        sum = 0;
        for(i;i<dim;i++){
            sum = sum + board[i][j];
        }
        if (sum>1){ return FALSE; }
    }
    return TRUE;
}

int bishop (int ** board, int dim){
    int a = 0;
    int sum1 = 0;
    int sum2 = 0;
    int sum3 = 0;
    int sum4 = 0;
    int i;
    int j;
    for (a; a<dim; a++){
        i = a;
        j = 0;
        sum1 = 0;
        while ( (i<dim) && (j<dim) ){
            sum1 = sum1 + board[i][j];
            i++; j++;
        }
        if (sum1>1){ return FALSE; }
        i = 0;
        j = a;
        sum2 = 0;
        while ( (i<dim) && (j<dim) ){
            sum2 = sum2 + board[i][j];
            i++; j++;
        }
        if (sum2>1){ return FALSE; }

        i = a;
        j = 0;
        sum3 = 0;
        while( (i>=0) && (j<dim) ) {
            sum3 = sum3 + board[i][j];
            i--; j++;
        }
        if (sum3>1){ return FALSE; }

        i = a;
        j = dim-1;
        sum4 = 0;
        while( (i<dim) && (j>=0) ) {
            sum4 = sum4 + board[i][j];
            i++; j--;
        }
        if (sum4>1){ return FALSE; }
    }
    return TRUE;
}

int queenTrue(int ** board, int dim){
    return bishop(board, dim) && rook(board, dim);//
}

void deepCopyBoard(int ** copy, int ** original, int dim){
    makeBoard(copy, dim);
    int i = 0;
    for(i; i<dim; i++){
        memcpy(copy[i], original[i], sizeof(original[i])*dim);
    }
}

void freeBoard(int ** board, int dim){
    int i = 0;
    for (i; i<dim; i++){
        free(board[i]);
    }
}

/*
We use lose it or use it approach with added prunning.
All branches are "queenTrue() true".  Branches that are
not 'queen true' are prunned/do not branch farther.
*/
int XQueens(int dim, int ** board, struct pair lastPair, int nuPlaced){
    int *useIt[dim];
    deepCopyBoard(useIt, board, dim);
    useIt[lastPair.i][lastPair.j] = useIt[lastPair.i][lastPair.j] + 1;
    if (queenTrue(useIt, dim) && dim == nuPlaced + 1){
        printf("Solution below:\n");
        printBoard(useIt, dim);
        return 1;
    }
    struct pair nextPair = nextify(dim, lastPair);
    if (nextPair.i == -1){ 
        freeBoard(board, dim);
        freeBoard(useIt, dim);
        return 0; 
    }
    
    if ( queenTrue(useIt, dim) ){
        return XQueens(dim, board, nextPair, nuPlaced) + XQueens(dim, useIt, nextPair, nuPlaced + 1);
    }
    else{
        freeBoard(useIt, dim);
        return XQueens(dim, board, nextPair, nuPlaced);
    }
}

int main(){
    printf("Please enter a positive integer.\n");
    char string [10];
    scanf("%s", string);
    int dim = atoi(string);
    int *board[dim];
    makeBoard(board, dim);
    struct pair start;
    start.i = 0;
    start.j = 0;
    int nuSolutions = XQueens(dim, board, start, 0);
    printf("The number of distinct solutions is %d (for n = %d).\n", nuSolutions, dim);
    return 1;
}
