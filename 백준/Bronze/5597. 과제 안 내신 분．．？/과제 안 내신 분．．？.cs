int[] student = new int[30];

for (int i = 0; i < 28; i++)
{
    int student_num = int.Parse(Console.ReadLine()) - 1;
    student[student_num] = 1;
}

for (int i = 0; i < 30; i++)
{
    if (student[i] != 1)
    {
        Console.WriteLine(i + 1);
    }
}
