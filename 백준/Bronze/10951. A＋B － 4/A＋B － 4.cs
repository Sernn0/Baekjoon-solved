string line;
while ((line = Console.ReadLine()) != null)
{
    string[] input = line.Split(' ');
    int num1 = int.Parse(input[0]);
    int num2 = int.Parse(input[1]);
    Console.WriteLine(num1 + num2);
}
