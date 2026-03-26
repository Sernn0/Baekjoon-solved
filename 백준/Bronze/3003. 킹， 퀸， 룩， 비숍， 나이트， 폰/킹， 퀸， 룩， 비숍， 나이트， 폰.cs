int[] piece = {1, 1, 2, 2, 2, 8};

string[] input = Console.ReadLine().Split(' ');

for (int i = 0; i < 6; i++)
{
    if (int.Parse(input[i]) != piece[i])
    {
        input[i] = (piece[i] - int.Parse(input[i])).ToString();
    }
    else
        input[i] = "0";
}

Console.WriteLine(string.Join(' ', input));
