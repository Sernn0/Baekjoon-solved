int N = int.Parse(Console.ReadLine());

int line = N * 2 - 1;

for (int i = 0; i < line / 2; i++)
{
    string print_line = "";
    // 각 라인 공백 갯수
    for (int j = 0; j < N - 1 - i; j++)
    {
        print_line += " ";
    }

    // 각 라인 별 갯수
    for (int k = 0; k < i * 2 + 1; k++)
    {
        print_line += "*";
    }
    Console.WriteLine(print_line);
}

for (int i = line / 2; i >= 0; i--)
{
    string print_line = "";
    // 각 라인 공백 갯수
    for (int j = 0; j < N - 1 - i; j++)
    {
        print_line += " ";
    }

    // 각 라인 별 갯수
    for (int k = 0; k < i * 2 + 1; k++)
    {
        print_line += "*";
    }
    Console.WriteLine(print_line);
}
