string[] input = Console.ReadLine().Split(' ');
int num1 = int.Parse(input[0]);
int num2 = int.Parse(input[1]);
int num3 = int.Parse(input[2]);

int prize = 0;

if (num1 == num2 && num2 == num3)
{
    prize += 10000 + num1 * 1000;
}
else if (num1 == num2 || num2 == num3 || num1 == num3)
{
    int same_num = (num1 == num2 ? num1 : num3);
    prize += 1000 + same_num * 100;
}
else
{
    int high_num = (num1 > num2 ? (num1 > num3 ? num1 : num3) : (num2 > num3 ? num2 : num3));
    prize += high_num * 100;
}

Console.WriteLine(prize);
