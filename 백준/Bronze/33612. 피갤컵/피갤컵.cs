int year = 2024;
int month = 8;

int input = (int.Parse(Console.ReadLine()) - 1) * 7;
month += input;

while (month > 12)
{
    month -= 12;
    year += 1;
}

Console.WriteLine($"{year} {month}");
