#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <pthread.h>
  
#define eps 1e-15
#define NTHREADS 2

int global = 1;

pthread_mutex_t mutex;

double Bailey(int k) {
    double retorno = (4 / (8*k + 1) -
                      2 / (8*k + 4) -
                      1 / (8*k + 5) -
                      1 / (8*k + 6)
                      ) / pow(16, k);
    return retorno;
}

void *Tarefa(void *tid){
  long int id = (long int) tid;
  double pi1=0;
  double pi2=1;
  int k = 0;
  long int cont = 0;
  long int cont2 = 0;
  long int *ret;
  while (global){
    while (fabs(pi1-pi2)>eps){
      pi2=pi1;
      pi1 += Bailey(k);
      k++;
    }
    cont++;
    pi1=0;
    pi2=1;
    if (cont == 100000000){
      cont2++;
      printf("Thread %li: Calculei pi %li vezes\n", id+1, cont2*100000000);
      cont = 0;
    }
  }
  ret = malloc(sizeof(long int));
  if(ret!=NULL){*ret = cont2*100000000 + cont;}
  else {printf("Erro de alocação\n");}

  pthread_exit((void*) ret);
}

void *jogo(void * arg){
  system("python server/server.py");
  pthread_mutex_lock(&mutex);
  global = 0;
  pthread_mutex_unlock(&mutex);
  pthread_exit(NULL);}


int main() {
    long int cont3 = 0;

    pthread_mutex_init(&mutex, NULL);
    
    pthread_t tid[NTHREADS + 1];
  //tid = (pthread_t *) malloc(sizeof(pthread_t) * 2);
    //if(tid==NULL){printf("Erro malloc do tid_sistema\n"); exit(-1);}
    long int *ret;
    for(long int i = 0; i < NTHREADS; i++){
      if(pthread_create(&tid[i], NULL, Tarefa, (void*) i)){
        printf("Erro no pthread_create"); exit(-1);}
    }
    
    if(pthread_create(&tid[NTHREADS + 1], NULL, jogo, NULL)){
      printf("Erro no pthread_create"); exit(-1);}
    
    for(int i =  0; i< NTHREADS; i++){
      if(pthread_join(tid[i], (void*) &ret)){
        printf("Erro no join\n"); exit(-1);}
      cont3 += *ret;
    }
    
    if(pthread_join(tid[NTHREADS + 1], NULL)){
      printf("Erro no join\n"); exit(-1);}
      
    printf("Durante essa partida pi foi calculado %li vezes", cont3);
    
    return 0;
}

