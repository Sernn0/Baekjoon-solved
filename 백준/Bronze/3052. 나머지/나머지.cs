int[] odds = new int[42];
int counter = 0;

for (int i = 0; i < 10; i++)
{
    int odd = int.Parse(Console.ReadLine()) % 42;
    odds[odd] = 1;
}

for (int i = 0; i < 42; i++)
{
    if (odds[i] == 1)
    {
        counter++;
    }
}

Console.WriteLine(counter);
