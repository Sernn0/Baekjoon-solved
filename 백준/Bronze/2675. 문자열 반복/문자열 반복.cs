int T = int.Parse(Console.ReadLine());

for (int i = 0; i < T; i++)
{
    string[] input = Console.ReadLine().Split(' ');
    int R = int.Parse(input[0]);
    string S = input[1];
    string result = "";

    for (int j = 0; j < S.Length; j++)
    {
        for (int k = 0; k < R; k++)
        {
            result += S[j];
        }
    }
    Console.WriteLine(result);
}
