#include <stdio.h>

int main(void) {
   int N, M;
   int arr[101] = {0};
   int i, j;
   int temp;

   scanf("%d %d", &N, &M);

   for(int num = 0; num < N; num ++) {
      arr[num] = num + 1;
   }

   for(int times = 0; times < M; times ++) {
      scanf("%d %d", &i, &j);
      for(int range = i - 1; range < j; range ++) {
         temp = arr[range];
         arr[range] = arr[j - 1];
         arr[j - 1] = temp;
         j --;
      }
   }
   for(int printnum = 0; printnum < N; printnum ++) {
      printf("%d ", arr[printnum]);
   }

   return 0;
}