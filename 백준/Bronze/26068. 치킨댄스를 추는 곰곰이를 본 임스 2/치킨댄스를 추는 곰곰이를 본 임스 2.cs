int times = int.Parse(Console.ReadLine());
int count = 0;

for (int i = 0; i < times; i++)
{
    string input = Console.ReadLine();
    string result = "";
    for (int j = 2; j < input.Length; j++)
    {
        result += input[j].ToString();
    }
    if (int.Parse(result) <= 90)
    {
        count++;
    }
}

Console.WriteLine($"{count}");
