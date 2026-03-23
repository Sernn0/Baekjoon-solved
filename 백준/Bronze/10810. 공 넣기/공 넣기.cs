string[] input = Console.ReadLine().Split(' ');
int N = int.Parse(input[0]);
int M = int.Parse(input[1]);

int[] bascket = new int[N];

for (int times = 0; times < M; times++)
{
    string[] range = Console.ReadLine().Split(' ');
    int i = int.Parse(range[0]) - 1;
    int j = int.Parse(range[1]) - 1;
    int k = int.Parse(range[2]);

    for (int fill_num = i; fill_num <= j; fill_num++)
    {
        bascket[fill_num] = k;
    }
}

Console.WriteLine(string.Join(" ", bascket));
