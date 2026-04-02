string[] input = Console.ReadLine().Split(' ');
int bread = int.Parse(input[0]);
int meat = int.Parse(input[1]);
int counter = 0;

while (true)
{
    bread -= 2;
    meat -= 1;
    if (bread < 0 || meat < 0)
        break;
    counter += 1;
}

Console.WriteLine($"{counter}");
