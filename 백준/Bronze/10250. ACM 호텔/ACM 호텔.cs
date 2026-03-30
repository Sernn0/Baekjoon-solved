int T = int.Parse(Console.ReadLine());

for (int i = 0; i < T; i++)
{
    string[] input = Console.ReadLine().Split(' ');
    int H = int.Parse(input[0]);
    int W = int.Parse(input[1]);
    int N = int.Parse(input[2]);

    int counter = 0;
    int pos_W = 0;
    int pos_H = 0;

    for (int j = 0; j < W; j++)
    {
        for (int k = 0; k < H; k++)
        {
            pos_W = j;
            pos_H = k;
            counter++;
            if (counter == N)
                goto Print;
        }
    }
    Print:
    pos_H += 1;
    pos_W += 1;
    if (pos_W > 9)
        Console.WriteLine($"{pos_H}{pos_W}");
    else
        Console.WriteLine($"{pos_H}0{pos_W}");
}
