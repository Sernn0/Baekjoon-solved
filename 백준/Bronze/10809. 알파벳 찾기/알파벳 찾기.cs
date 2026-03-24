string input = Console.ReadLine();
int[] alphabet = new int[26];

for (int i = 0; i < 26; i++)
{
    alphabet[i] = -1;
}

for (int i = 0; i < input.Length; i++)
{
    int ascii = (int)input[i];
    if (alphabet[ascii - 97] == -1)
    {
        alphabet[ascii - 97] = i;
    }
}

Console.WriteLine(string.Join(" ", alphabet));
