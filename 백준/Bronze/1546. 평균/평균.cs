int subject = int.Parse(Console.ReadLine());
string[] input = Console.ReadLine().Split(' ');

float[] score = new float[subject];
float high_score = float.MinValue;
float total_score = 0;

for (int i = 0; i < subject; i++)
{
    score[i] = float.Parse(input[i]);
    if (score[i] > high_score)
    {
        high_score = score[i];
    }
}

for (int i = 0; i < subject; i++)
{
    score[i] = score[i] / high_score * 100;
    total_score += score[i];
}

float result = total_score / subject;
Console.WriteLine(result);
