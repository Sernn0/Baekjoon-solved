class Program
{
    static void Main(string[] args)
    {
        string input = Console.ReadLine();
        int counter = 0;

        for (int i = 0; i < input.Length; i++)
        {
            if (
                input[i] == 'a'
                || input[i] == 'i'
                || input[i] == 'u'
                || input[i] == 'e'
                || input[i] == 'o'
            )
                counter++;
        }

        Console.WriteLine(counter);
    }
}
