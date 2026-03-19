string[] input = Console.ReadLine().Split(' ');
int input1 = int.Parse(input[0]);
int input2 = int.Parse(input[1]);

if (input1 < input2)
{
    Console.WriteLine("<");
}
else if (input1 > input2)
{
    Console.WriteLine(">");
}
else
{
    Console.WriteLine("==");
}
