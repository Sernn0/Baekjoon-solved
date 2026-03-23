string[] input = Console.ReadLine().Split(' ');
int N = int.Parse(input[0]);
int M = int.Parse(input[1]);

int[] bascket = new int[N];
for (int i = 0; i < N; i++)
{
    bascket[i] = i + 1;
}

for (int times = 0; times < M; times++)
{
    string[] range = Console.ReadLine().Split(' ');
    int i = int.Parse(range[0]) - 1;
    int j = int.Parse(range[1]) - 1;

    while (i < j)
    {
        int temp = bascket[i];
        bascket[i] = bascket[j];
        bascket[j] = temp;
        i++;
        j--;
    }
}

Console.WriteLine(string.Join(" ", bascket));
