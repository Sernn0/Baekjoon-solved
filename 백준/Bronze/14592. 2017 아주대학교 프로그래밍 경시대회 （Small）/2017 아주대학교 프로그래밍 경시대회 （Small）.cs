using System.Net;

int N = int.Parse(Console.ReadLine());
int[,] info = new int[N, 3];

for (int i = 0; i < N; i++)
{
    int[] input = Array.ConvertAll(Console.ReadLine().Split(' '), int.Parse);
    info[i, 0] = input[0];
    info[i, 1] = input[1];
    info[i, 2] = input[2];
}

int winner = 0;

for (int i = 1; i < N; i++)
{
    if (info[i, 0] > info[winner, 0])
    {
        winner = i;
    }
    else if (info[i, 0] == info[winner, 0])
    {
        if (info[i, 1] < info[winner, 1])
        {
            winner = i;
        }
        else if (info[i, 1] == info[winner, 1])
        {
            if (info[i, 2] < info[winner, 2])
                winner = i;
        }
    }
}

Console.WriteLine($"{winner + 1}");
