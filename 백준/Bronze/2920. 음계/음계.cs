int[] input = Array.ConvertAll(Console.ReadLine().Split(' '), int.Parse);

int[] ascending = (int[])input.Clone();
Array.Sort(ascending);
int[] descending = ascending.Reverse().ToArray();

if (input.SequenceEqual(ascending) == true)
    Console.WriteLine("ascending");
else if (input.SequenceEqual(descending) == true)
    Console.WriteLine("descending");
else
    Console.WriteLine("mixed");
