int count = int.Parse(Console.ReadLine());
string[] input = Console.ReadLine().Split(' ');
int isPossible = 1;

for (int i = 0; i < count - 1; i++)
{
    string curWord = input[i];
    string nextWord = input[i + 1];
    if (curWord[curWord.Length - 1] == nextWord[0])
    {
        isPossible = 1;
    }
    else
    {
        isPossible = 0;
        break;
    }
}

Console.WriteLine(isPossible);
