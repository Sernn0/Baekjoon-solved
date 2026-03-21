string[] input = Console.ReadLine().Split(' ');
int dan_num = int.Parse(input[0]);

for (int i = 1; i < 10; i++)
{
    Console.WriteLine($"{dan_num} * {i} = " + dan_num * i);
}
