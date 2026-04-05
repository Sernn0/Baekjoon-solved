string[] input = Console.ReadLine().Split(' ');
int N = int.Parse(input[0]);
int M = int.Parse(input[1]);

int[,] matrix = new int[N, M];

for (int i = 0; i < N; i++)
{
    string[] element = Console.ReadLine().Split(' ');
    for (int j = 0; j < M; j++)
    {
        matrix[i, j] = int.Parse(element[j]);
    }
}

for (int a = 0; a < N; a++)
{
    string[] sum = Console.ReadLine().Split(' ');
    for (int b = 0; b < M; b++)
    {
        matrix[a, b] += int.Parse(sum[b]);
    }
}

for (int c = 0; c < N; c++)
{
    int[] row = new int[M];
    for (int d = 0; d < M; d++)
    {
        row[d] = matrix[c, d];
    }
    Console.WriteLine(string.Join(' ', row));
}
