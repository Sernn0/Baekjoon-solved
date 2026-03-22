int size = int.Parse(Console.ReadLine());
string[] num = Console.ReadLine().Split(' ');
int target_num = int.Parse(Console.ReadLine());
int counter = 0;

for (int i = 0; i < size; i++)
{
    if (int.Parse(num[i]) == target_num)
    {
        counter++;
    }
}

Console.WriteLine(counter);
