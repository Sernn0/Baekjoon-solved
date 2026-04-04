string[] input = Console.ReadLine().Split(' ');
int costs = int.Parse(input[0]);
int count = int.Parse(input[1]);

int[] cost_arr = new int[costs];
string[] value = Console.ReadLine().Split(' ');
int pos = 0;
foreach (var cost in value)
{
    cost_arr[pos] = int.Parse(value[pos]);
    pos++;
}

int min_value = int.MaxValue;
int index_counter = 0;

for (int i = 0; i < costs - 1; i++)
{
    if (cost_arr[i] + cost_arr[i + 1] < min_value)
    {
        min_value = cost_arr[i] + cost_arr[i + 1];
        index_counter = i;
    }
}

Console.WriteLine($"{cost_arr[index_counter] * count + cost_arr[index_counter + 1] * count}");
