class Program
{
    static void Main(string[] args)
    {
        int N = int.Parse(Console.ReadLine());
        int[] input = Array.ConvertAll(Console.ReadLine().Split(' '), int.Parse);
        Array.Sort(input);
        List<int> odd = new List<int>();

        int sum = 0;

        for (int i = 0; i < N; i++)
        {
            if (input[i] % 2 == 0)
                sum += input[i];
            else
            {
                sum += input[i];
                odd.Add(input[i]);
            }
        }

        if (sum % 2 == 1)
        {
            sum -= odd[0];
        }

        Console.WriteLine(sum);
    }
}
