string[] input = Console.ReadLine().Split(' ');
int hour = int.Parse(input[0]);
int min = int.Parse(input[1]);

int new_min = min - 45;
int new_hour = hour;

if (new_min < 0)
{
    if (new_hour == 0)
    {
        new_hour = 23;
    }
    else
    {
        new_hour -= 1;
    }
    new_min += 60;
}

Console.WriteLine($"{new_hour} {new_min}");
