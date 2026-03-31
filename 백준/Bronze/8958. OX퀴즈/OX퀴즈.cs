int times = int.Parse(Console.ReadLine());

for (int i = 0; i < times; i++)
{
    string input = Console.ReadLine();
    int total_score = 0;
    int score = 0;
    for (int j = 0; j < input.Length; j++)
    {
        if (input[j] == 'O')
        {
            score++;
            total_score += score;
        }
        else if (input[j] == 'X')
        {
            score = 0;
        }
    }
    Console.WriteLine($"{total_score}");
}
