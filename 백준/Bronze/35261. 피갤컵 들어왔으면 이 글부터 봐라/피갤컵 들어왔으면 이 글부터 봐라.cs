class Program
{
    static void Main(string[] args)
    {
        int size = int.Parse(Console.ReadLine());
        string input = Console.ReadLine();

        int result = int.MaxValue;

        for (int i = 0; i < size - 4; i++)
        {
            int counter = 5;
            counter = input[i] == 'e' ? counter - 1 : counter;
            counter = input[i + 1] == 'a' ? counter - 1 : counter;
            counter = input[i + 2] == 'g' ? counter - 1 : counter;
            counter = input[i + 3] == 'l' ? counter - 1 : counter;
            counter = input[i + 4] == 'e' ? counter - 1 : counter;
            result = counter < result ? counter : result;
        }
        Console.WriteLine(result);
    }
}
