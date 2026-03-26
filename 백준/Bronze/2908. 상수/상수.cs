string[] input = Console.ReadLine().Split(' ');
int num1 = int.Parse(new string(input[0].Reverse().ToArray()));
int num2 = int.Parse(new string(input[1].Reverse().ToArray()));

if (num1 > num2)
{
    Console.WriteLine(num1);
}
else
    Console.WriteLine(num2);
