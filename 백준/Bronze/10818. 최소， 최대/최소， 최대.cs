int size = int.Parse(Console.ReadLine());
string[] num = Console.ReadLine().Split(' ');
int max_num = int.MinValue;
int min_num = int.MaxValue;

for (int i = 0; i < size; i++)
{
    if (int.Parse(num[i]) > max_num)
    {
        max_num = int.Parse(num[i]);
    }
    if (int.Parse(num[i]) < min_num)
    {
        min_num = int.Parse(num[i]);
    }
}

Console.WriteLine($"{min_num} {max_num}");
