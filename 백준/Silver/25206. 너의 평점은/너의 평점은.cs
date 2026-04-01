double total_score = 0;
double total_grade = 0;

for (int i = 0; i < 20; i++)
{
    string[] input = Console.ReadLine().Split(' ');
    double score = double.Parse(input[1]);
    total_score += score;

    string grade = input[2];
    switch (grade)
    {
        case "A+":
            total_grade += score * 4.5;
            break;
        case "A0":
            total_grade += score * 4.0;
            break;
        case "B+":
            total_grade += score * 3.5;
            break;
        case "B0":
            total_grade += score * 3.0;
            break;
        case "C+":
            total_grade += score * 2.5;
            break;
        case "C0":
            total_grade += score * 2.0;
            break;
        case "D+":
            total_grade += score * 1.5;
            break;
        case "D0":
            total_grade += score * 1.0;
            break;
        case "F":
            total_grade += score * 0.0;
            break;
        case "P":
            total_score -= score;
            break;
    }
}

double avg_score = total_grade / total_score;
Console.WriteLine($"{avg_score}");
